"""The Capon beamformer running on GPU.
"""
import logging
import numpy as np

from .beamformer import Beamformer
from ultraspy.utils.beamformers import get_axes_to_reduce

from ultraspy.cpu.kernels.numba_cores import capon as numba_capon

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    from ultraspy.gpu import gpu_utils
    from ultraspy.gpu.kernels.beamformers_kernels import k_capon, k_packet_capon


logger = logging.getLogger(__name__)


class Capon(Beamformer):
    """The Capon class, inherit from the Beamformer class (which deals with the
    beamforming setups) and performs the beamforming itself. The class is
    working on either Cupy (CUDA, GPU) or Numba (CPU) depending on the selected
    mode (check the doc and the ULTRASPY_CPU_LIB environment variable for more
    information).

    :ivar str name: The name of the Beamforming method
    :ivar bool is_iq: If set to True, will perform the beamforming expecting
        I/Qs
    :ivar bool on_gpu: If set to True, will perform the beamforming on GPU
    :ivar bool is_same_probe: If set to True, the emission sequences and the
        reception sequences are the same (mostly standard plane waves),
        else case, both sequences are different (mostly STA)
    :ivar list transmissions_indices: The list of the transmissions indices to
        select
    :ivar dict setup: The characteristics of the beamformer, see the getter to
        have the list of the parameters
    :ivar dict options: The options of the beamformer, see the getter to have
        the list of the parameters
    :ivar numpy.ndarray delays: The delays applied to each element, for each
        transmission, of shape (nb_transmission, nb_emitted_elements)
    :ivar numpy.ndarray emitted_probe: The 3D position of each of the element
        of the emitted probe, per transmission, of shape (nb_transmission,
        nb_emitted_elements)
    :ivar numpy.ndarray received_probe: The 3D position of each of the element
        of the received probe, per transmission, of shape (nb_transmission,
        nb_received_elements)
    :ivar numpy.ndarray emitted_thetas: The thetas of each of the element
        of the emitted probe, per transmission, of shape (nb_transmission,
        nb_emitted_elements). Only used for convex probes
    :ivar numpy.ndarray received_thetas: The 3D position of each of the element
        of the received probe, per transmission, of shape (nb_transmission,
        nb_received_elements). Only used for convex probes
    :param bool diagonal_loading_mode: If set to True, will perform the diagonal
        loading mode instead of standard (default) forward / backward
    :param float l_prop: The proportion of the delays to use to constitute one
        window, should be ]0, 0.5]
    :param float delta_l: The delta factor to enhance the diagonal loading,
        should be [1, 1000]
    """

    def __init__(self, is_iq=False, on_gpu=True, diagonal_loading_mode=False,
                 l_prop=0.2, delta_l=100):
        """Initializes the Beamformer parent first, then set the options for
        Capon.

        :param bool is_iq: If set to True, the beamformer expects to process
            I/Qs data
        :param bool on_gpu: If True, all the setups are defined on GPU
        :param bool diagonal_loading_mode: If set to True, will perform the
            diagonal loading mode instead of standard (default) forward /
            backward
        :param float l_prop: The proportion of the delays to use to constitute
            one window, should be ]0, 0.5]
        :param float delta_l: The delta factor to enhance the diagonal loading,
            should be [1, 1000]
        """
        super().__init__(is_iq=is_iq, on_gpu=on_gpu)
        self._name = 'capon'
        self._diagonal_loading_mode = diagonal_loading_mode
        self._l_prop = l_prop
        self._delta_l = delta_l

    @property
    def diagonal_loading_mode(self):
        """Get the Capon mode.
        """
        return self._diagonal_loading_mode

    @property
    def l_prop(self):
        """Get the proportion of the elements to use as a window.
        """
        return self._l_prop

    @property
    def delta_l(self):
        """Get the delta to use to enhance the diagonal loading.
        """
        return self._delta_l

    def set_diagonal_loading_mode(self, diagonal_loading_mode):
        """Updates the diagonal_loading_mode value.

        :param bool diagonal_loading_mode: The new Capon mode
        """
        self._diagonal_loading_mode = diagonal_loading_mode

    def set_l_prop(self, l_prop):
        """Updates the l_prop value.

        :param float l_prop: The new l_prop
        """
        self._l_prop = l_prop

    def set_delta_l(self, delta_l):
        """Updates the delta_l value.

        :param float delta_l: The new delta_l
        """
        self._delta_l = delta_l

    def beamform_gpu(self, d_data, scan):
        """Runs the Capon beamformer using cupy (CUDA kernel on GPU).

        :param cupy.array d_data: The cupy.array data to beamform, stored on
            GPU, either in float or complex, based on the beamforming mode. The
            shape should be (nb_transmissions, nb_emitted_elements,
            nb_time_samples)
        :param Scan scan: The scan to beamform, with the pixels we are willing
            to process

        :returns: The beamformed data. Its shape depends on the beamforming
            options, but its last dimensions will be the one requested in
            scan.shape. If compound option is set to False, it will preserve
            the transmissions and look like (nb_transmissions, \\*scan.shape)
        :return type: cupy.array
        """
        # Shortcuts
        ss = self.setups
        so = self.options

        if self.emitted_probe.shape[-1] > 128:
            logger.warning("Capon needs to pre-allocate memory for its "
                           "correlation matrix. Actually defined to max 128 "
                           "elements. The current configuration might lead to "
                           "invalid memory access.")

        # If the coordinates are on CPU, send them to GPU
        if not scan.on_gpu:
            scan.set_on_gpu(True)

        _, nb_re, nb_ts = d_data.shape
        nb_t, nb_ee = self.delays.shape
        d_xx, d_yy, d_zz = scan.ravel_pixels()
        nb_pixels = d_xx.size
        dim_nb_t = nb_t if so['compound'] == 0 else 1
        dim_nb_re = nb_re if so['reduce'] == 0 else 1
        d_grid = gpu_utils.send_to_gpu(
            np.zeros((dim_nb_t, dim_nb_re, nb_pixels)), np.complex64)
        d_focused_data = gpu_utils.send_to_gpu(
            np.zeros((nb_pixels, nb_re)), np.complex64)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels)
        k_capon(g_dim, b_dim,
                (d_data, np.uint32(self.is_iq),
                 self.emitted_probe, self.received_probe,
                 self.emitted_thetas, self.received_thetas, self.delays,
                 np.uint32(nb_t), np.uint32(nb_ee), np.uint32(nb_re),
                 np.uint32(nb_ts),
                 ss['sampling_freq'], ss['central_freq'], np.float32(self.t0),
                 ss['sound_speed'], ss['f_number'],
                 d_xx, d_yy, d_zz,
                 np.uint32(dim_nb_t), np.uint32(dim_nb_re),
                 d_focused_data, d_grid, np.uint32(nb_pixels),
                 np.uint32(self.diagonal_loading_mode),
                 np.float32(self.l_prop), np.float32(self.delta_l),
                 so['interpolation'], so['reduction'], so['rx_apodization'],
                 so['rx_apodization_alpha'], so['emitted_aperture'],
                 so['compound'], so['reduce']))

        axes = get_axes_to_reduce(so['compound'], so['reduce'])
        d_grid = gpu_utils.squeeze_axes(d_grid, axes=axes)
        return gpu_utils.reshape(d_grid, d_grid.shape[:-1] + scan.shape)

    def beamform_cpu(self, data, scan):
        """Runs the Capon beamformer using the no-python iterative mode of
        Numba.

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param Scan scan: the scan to beamform, with the pixels we are willing
            to process

        :returns: The beamformed data. Its shape depends on the beamforming
            options, but its last dimensions will be the one requested in
            scan.shape. If compound option is set to False, it will preserve
            the transmissions and look like (nb_transmissions, \\*scan.shape)
        :return type: numpy.ndarray
        """
        core = self._beamform_numba

        # If the coordinates are on GPU, send them back to CPU
        if scan.on_gpu:
            scan.set_on_gpu(False)

        # Calls the beamformer
        xx, yy, zz = scan.ravel_pixels()
        grid = core(data, xx, yy, zz, self.setups, self.options)
        return np.reshape(grid, grid.shape[:-1] + scan.shape)

    def beamform_packet_gpu(self, d_data, scan):
        """Runs the Capon beamformer on a packet of data using cupy (CUDA
        kernel on GPU).

        :param cupy.array d_data: The cupy.array data to beamform, stored on
            GPU, either in float or complex, based on the beamforming mode. The
            shape should be (nb_frames, nb_transmissions, nb_emitted_elements,
            nb_time_samples)
        :param Scan scan: The scan to beamform, with the pixels we are willing
            to process

        :returns: The beamformed data. Its shape depends on the beamforming
            options, but if compound and reduce are set to True, its shape
            would be (\\*scan.shape, nb_frames). If reduce or compound are set
            to False, their respective dimensions will be preserved in the first
            dimensions as for the ::code::`beamform` method above
        :return type: cupy.array
        """
        # Shortcuts
        ss = self.setups
        so = self.options

        # If the coordinates are on CPU, send them to GPU
        if not scan.on_gpu:
            scan.set_on_gpu(True)

        nb_f, _, nb_re, nb_ts = d_data.shape
        nb_t, nb_ee = self.delays.shape
        d_xx, d_yy, d_zz = scan.ravel_pixels()
        nb_pixels = d_xx.size
        dim_nb_t = nb_t if so['compound'] == 0 else 1
        dim_nb_re = nb_re if so['reduce'] == 0 else 1
        d_grid = gpu_utils.send_to_gpu(
            np.zeros((dim_nb_t, dim_nb_re, nb_pixels, nb_f)), np.complex64)
        d_delays = gpu_utils.send_to_gpu(
            np.zeros((nb_pixels, nb_f, nb_re)), np.complex64)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels * nb_f)
        k_packet_capon(g_dim, b_dim,
                       (d_data, np.uint32(self.is_iq),
                        self.emitted_probe, self.received_probe,
                        self.emitted_thetas, self.received_thetas, self.delays,
                        np.uint32(nb_f), np.uint32(nb_t),
                        np.uint32(nb_ee), np.uint32(nb_re), np.uint32(nb_ts),
                        ss['sampling_freq'], ss['central_freq'],
                        np.float32(self.t0), ss['sound_speed'], ss['f_number'],
                        d_xx, d_yy, d_zz,
                        np.uint32(dim_nb_t), np.uint32(dim_nb_re),
                        d_delays, d_grid, np.uint32(nb_pixels * nb_f),
                        np.uint32(self.diagonal_loading_mode),
                        np.float32(self.l_prop), np.float32(self.delta_l),
                        so['interpolation'], so['reduction'],
                        so['rx_apodization'], so['rx_apodization_alpha'],
                        so['emitted_aperture'], so['compound'], so['reduce']))

        axes = get_axes_to_reduce(so['compound'], so['reduce'])
        d_grid = gpu_utils.squeeze_axes(d_grid, axes=axes)
        return gpu_utils.reshape(
            d_grid, d_grid.shape[:-2] + scan.shape + d_grid.shape[-1:])

    def beamform_packet_cpu(self, data, scan):
        """Runs the Capon beamformer on a packet of data using the no-python
        iterative mode of Numba.

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_frames, nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param Scan scan: the scan to beamform, with the pixels we are willing
            to process

        :returns: The beamformed data. Its shape depends on the beamforming
            options, but if compound and reduce are set to True, its shape
            would be (\\*scan.shape, nb_frames). If compound is set to False,
            the transmissions will be preserved in the first dimension as for
            the ::code::`beamform` method above
        :return type: numpy.ndarray
        """
        # If the coordinates are on GPU, send them back to CPU
        if scan.on_gpu:
            scan.set_on_gpu(False)

        core = self._beamform_packet_numba

        # Calls the beamformer
        xx, yy, zz = scan.ravel_pixels()
        grid = core(data, xx, yy, zz, self.setups, self.options)
        return np.reshape(grid, grid.shape[:-2] + scan.shape + grid.shape[-1:])

    def _checkup_lib_compatibility(self, option_name, option_value):
        """Checks if the current library used (numpy or numba) is compatible
        with the new selected option.

        :param str option_name: The name of the option to change
        :param int, float option_value: The value to update

        :returns: The new value for the option, that will work for sure
        :return type: int, float
        """
        if cfg.CPU_LIB == 'numpy' and not self.on_gpu:
            logger.warning("Capon is not implemented using Numpy, will use "
                           "Numba instead.")

        option_value = super()._checkup_lib_compatibility(
            option_name, option_value)

        # Additional constraint of Capon algorithm
        if option_name == 'compound':
            if option_value == 0:
                logger.warning("Compounding must be done with Capon.")
                option_value = 1

        # Additional constraint of Capon algorithm
        if option_name == 'reduce':
            if option_value == 0:
                logger.warning("Reduction must be done with Capon.")
                option_value = 1

        return option_value

    ###########################################################################
    # Numba callers
    ###########################################################################
    def _beamform_numba(self, data, xs, ys, zs, setups, options):
        """Caller, will call Numba beamforming kernel.

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param numpy.ndarray xs: the lateral coordinates of the pixels, ravelled
        :param numpy.ndarray ys: the elevational coordinates of the pixels,
            ravelled
        :param numpy.ndarray zs: the axial coordinates of the pixels, ravelled
        :param dict setups: the dictionary with the setups info
        :param dict options: the dictionary with the options info

        :returns: The beamformed data, of shape (nb_kept_transmissions,
            nb_kept_elements, nb_pixels)
        :return type: numpy.ndarray
        """
        grid = numba_capon.capon(
            data, self.is_iq,
            self.emitted_probe, self.received_probe,
            self.emitted_thetas, self.received_thetas, self.delays,
            setups['sampling_freq'], setups['central_freq'],
            np.float32(self.t0), setups['sound_speed'], setups['f_number'],
            xs, ys, zs,
            self.diagonal_loading_mode, self.l_prop, self.delta_l,
            options['interpolation'], options['reduction'],
            options['rx_apodization'], options['rx_apodization_alpha'],
            options['emitted_aperture'], options['reduce'], options['compound'],
            self.is_same_probe)

        if not self.is_iq:
            grid = grid.real

        axes = get_axes_to_reduce(options['compound'], options['reduce'])
        return np.squeeze(grid, axis=axes)

    def _beamform_packet_numba(self, data, xs, ys, zs, setups, options):
        """Caller, will call Numba beamforming kernel on a packet of frames.

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_frames, nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param numpy.ndarray xs: the lateral coordinates of the pixels, ravelled
        :param numpy.ndarray ys: the elevational coordinates of the pixels,
            ravelled
        :param numpy.ndarray zs: the axial coordinates of the pixels, ravelled
        :param dict setups: the dictionary with the setups info
        :param dict options: the dictionary with the options info

        :returns: The beamformed data, of shape (nb_kept_transmissions,
            nb_kept_elements, nb_pixels, nb_frames)
        :return type: numpy.ndarray
        """
        grid = numba_capon.capon_packet(
            data, self.emitted_probe, self.received_probe,
            self.emitted_thetas, self.received_thetas, self.delays,
            setups['sampling_freq'], setups['central_freq'],
            np.float32(self.t0), setups['sound_speed'], setups['f_number'],
            xs, ys, zs,
            self.diagonal_loading_mode, self.l_prop, self.delta_l,
            options['interpolation'], options['reduction'],
            options['rx_apodization'], options['rx_apodization_alpha'],
            options['emitted_aperture'], options['reduce'], options['compound'],
            self.is_same_probe)

        if not self.is_iq:
            grid = grid.real

        axes = get_axes_to_reduce(options['compound'], options['reduce'])
        return np.squeeze(grid, axis=axes)
