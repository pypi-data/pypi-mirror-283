"""Methods for doppler imaging.
"""
import numpy as np
import scipy.signal
import scipy.ndimage

from .signal import _filtfilt_wn
from ultraspy.helpers.doppler_helpers import get_polynomial_coefficients
from ultraspy.helpers.windows_helpers import get_hamming_squared_kernel

import ultraspy as us


def apply_wall_filter(data, mode, degree=1, axis=-1):
    """Applies a clutter filter along slow time (last dimension of our data by
    default). Four modes are available:

        - none: when there are no wall filter to apply, doesn't do anything
        - mean: applies a basic mean filter (subtract the mean of the data
          along slow time)
        - poly: applies a polynomial filter. The polynomial regression consists
          in using orthogonal Legendre polynomial coefficients to remove the
          fitting polynomials from the data, which ends up to remove the low
          frequencies components. The degree is the upper degree of the
          polynomials we want to remove
        - hp_filter: applies a high-pass butterworth filter. The critical
          frequency is assumed to be a tenth of degree (HP filter of everything
          above 10% of the spectrum if degree = 1)

    The degree parameter is the order of the filter to apply. If it is set to 0,
    the 'mean' mode will be selected (as it is a polynomial wall filter of
    degree 0). If the hp_filter is selected, we'll consider w_n = degree / 10.

    :param numpy.ndarray data: The numpy array on which to perform the clutter
        filter
    :param str mode: The name of the clutter filter to use, can be either
        'none', 'mean', 'poly' or 'hp_filter'
    :param int degree: The order of our filter (or 10 * w_n if we do hp_filter)
    :param int axis: The axis on which to perform the clutter filter (the
        dimension of the slow time)

    :returns: The filtered data along slow time.
    :return type: numpy.ndarray
    """
    # No wall filter, do nothing
    if mode == 'none':
        return data

    # Mean wall filter
    if mode == 'mean' or degree == 0:
        return _apply_mean_wall_filter(data, axis=axis)

    # Polynomial wall filter
    elif mode == 'poly':
        return _apply_poly_wall_filter(data, degree, axis=axis)

    # High-pass wall filter
    elif mode == 'hp_filter':
        w_n = degree / 10
        return _apply_hp_wall_filter(data, w_n, axis=axis)

    # Unknown clutter filter
    else:
        raise AttributeError(
            f"Unknown wall filter. Please choose one of  the following: "
            f"none, mean, poly, hp_filter")


def spatial_smoothing(data, k_size, window_type='hamming'):
    """Performs a spatial smoothing on data, using a given smoothing function
    and a squared convolution kernel. Two methods are implemented:

        - hamming: Performs a convolution with a squared hamming window of size
          (k_size, k_size)
        - median: applies a median filter on a squared spatial matrix (of size
          (k_size, k_size)). If complex numbers, do the median of both real and
          imaginary parts separately

    :param numpy.ndarray data: The 2D numpy data to smoothen
    :param int k_size: The kernel size
    :param str window_type: The name of the windowing function to use, only
        'hamming' (default) and 'median' is supported for now.

    :returns: The smoothed data.
    :return type: numpy.ndarray
    """
    if window_type not in ['hamming', 'median']:
        raise AttributeError(
            f"Unknown window type function, please peak among supported "
            f"methods (hamming or median).")

    # No smoothing, simply returns the original data
    if k_size <= 1:
        return data

    if window_type == 'median':
        if data.imag.any():
            real = scipy.ndimage.median_filter(
                data.real, k_size, mode='nearest')
            imag = scipy.ndimage.median_filter(
                data.imag, k_size, mode='nearest')
            data = real + 1j * imag
        else:
            data = scipy.ndimage.median_filter(data, k_size, mode='nearest')
    else:
        k = get_hamming_squared_kernel(k_size)
        data = scipy.ndimage.correlate(data, k, mode='nearest')

    return data


def get_color_doppler_map(data, nyquist_velocity, smoothing='hamming',
                          kernel=1):
    """Computes the color doppler map, which is using the correlation of our
    data along slow time (last dimension of data), which are then converted to
    doppler velocity using the Doppler formula. It also can perform a spatial
    smoothing of a given number of pixels.

    .. math::
        v_{D} = -v_{c} . \\Im \\left (\\frac{\\log(\\text{data})}{\\pi} \
                              \\right )

    :param numpy.ndarray data: The numpy array I/Qs data
    :param float nyquist_velocity: The nyquist velocity, can be determined
        using c * prf / (4 * f_c)
    :param str smoothing: The smoothing method to use (either hamming or median)
    :param int kernel: The size of the squared kernel for smoothing

    :returns: The color map, which is of the shape of data (except the slow
        time dimension)
    :return type: numpy.ndarray
    """
    corr_matrix = np.sum(data[..., :-1] * np.conj(data[..., 1:]), axis=-1)
    corr_matrix = spatial_smoothing(corr_matrix, kernel, smoothing)
    imag_r = np.imag(np.log(corr_matrix))
    return -nyquist_velocity * imag_r / np.pi


def get_power_doppler_map(data, smoothing='hamming', kernel=1):
    """Computes the power doppler map, which is using the mean of squared
    values along slow time (defined as the last dimension of data). The result
    is then returned in dB. It can also perform a spatial smoothing of a given
    number of pixels.

    .. math::
        \\text{MS} = \\frac{\\sum_{i=1}^{n}{|\\text{data}_{\\ i}|^2}}{n}

        P_{D} = 10 . \\frac{\\log_{10}(\\text{MS})}{\\max(\\text{MS})}

    :param numpy.ndarray data: The numpy array data
    :param str smoothing: The smoothing method to use (either hamming or median)
    :param int kernel: The size of the squared kernel for smoothing

    :returns: The power map, which is of the shape of data (except the slow
        time dimension)
    :return type: numpy.ndarray
    """
    power = np.mean(np.abs(data) ** 2, axis=-1)
    power = spatial_smoothing(power, kernel, smoothing)
    return 10 * np.log10(power / np.max(power))


def dual_frequency_unalias(data, beamformed_fs, f01, p, band, sound_speed, prf,
                           smoothing='hamming', kernel=1):
    """Computes two Doppler maps with different central frequencies, that can
    be mapped together to propose an alias-free Color map. This is based on
    works of Ecarlat et al., IUS 2022, "Alias-free color Doppler using chirps"

    :param numpy.ndarray data: The beamformed IQs data
    :param float beamformed_fs: The sampling frequency along the beamformed
        signal, in Hz
    :param float f01: The first central frequency to use, in Hz
    :param int p: The p relation between f01 and f02
    :param float band: The band of the filter, in Hz
    :param float sound_speed: The speed of sound of the medium
    :param float prf: The PRF used during the acquisition
    :param str smoothing: The smoothing method to use (either hamming or median)
    :param int kernel: The size of the squared kernel for smoothing

    :returns: The unaliased color map
    :return type: numpy.ndarray
    """
    # Get central frequencies and nyquist velocities
    f02 = f01 * (p + 1) / p
    nyquist_1 = sound_speed * prf / (4 * f01)
    nyquist_2 = sound_speed * prf / (4 * f02)

    # Central freq 1
    iqs1 = _filtfilt_band(data, f01, beamformed_fs, band)
    cmap1 = get_color_doppler_map(iqs1, nyquist_1,
                                  smoothing=smoothing, kernel=kernel)

    # Central freq 2
    iqs2 = _filtfilt_band(data, f02, beamformed_fs, band)
    cmap2 = get_color_doppler_map(iqs2, nyquist_2,
                                  smoothing=smoothing, kernel=kernel)

    # De-aliasing
    return _unalias([cmap1, cmap2], [nyquist_1, nyquist_2], p)


def _apply_mean_wall_filter(data, axis=-1):
    """Applies a basic mean filter on our data along slow time (default axis is
    the last one). It simply subtracts the mean of the pixels along slow time.

    :param numpy.ndarray data: The numpy array on which to perform the mean
        wall filter
    :param int axis: The axis on which to perform the clutter filter (slow time
        dimension).

    :returns: The filtered data along slow time.
    :return type: numpy.ndarray
    """
    return data - np.mean(data, axis=axis, keepdims=True)


def _apply_poly_wall_filter(data, degree, axis=-1):
    """Applies a polynomial clutter filter on our data along slow time (default
    axis is -1). The polynomial regression consists in using orthogonal
    Legendre polynomial coefficients to remove the fitting polynomials from the
    data, which ends up to remove the low frequencies components. The degree is
    the upper degree of the polynomials we want to remove.

    :param numpy.ndarray data: The numpy array on which to perform the
        polynomial wall filter
    :param int degree: The upper degree of the polynomials we want to remove
    :param int axis: The axis on which to perform the clutter filter (slow time
        dimension)

    :returns: The filtered data along slow time.
    :return type: numpy.ndarray
    """
    # If the slow time is not along the last dimension, we should move it
    if axis != -1:
        data = np.moveaxis(data, axis, -1)

    # Get the number of frames
    nb_frames = data.shape[-1]

    # Polynomial coefficients
    polys = get_polynomial_coefficients(nb_frames, degree)
    coefficients = np.sum(polys * data[..., None, :], axis=-1)
    coefficients /= np.sum(polys ** 2, axis=-1)

    # High-pass filtered data
    lf_sig = np.sum(polys * coefficients[..., None], axis=-2)
    data -= lf_sig

    # Restore the initial dimensions
    if axis != -1:
        data = np.moveaxis(data, -1, axis)

    return data


def _apply_hp_wall_filter(data, w_n, axis=-1):
    """Applies a high-pass butterworth filter on our data along slow time
    (default axis is -1). The w_n parameter is the critical frequency where the
    gain will drop to 1 / sqrt(2). As we are working with digital filters, it
    is normalized from 0 to 1 where 1 is the Nyquist frequency.

    :param numpy.ndarray data: The numpy array on which to perform the
        band-pass wall filter
    :param float w_n: The normalized critical frequency to use for filtering.
    :param int axis: The axis on which to perform the clutter filter (slow time
        dimension), default to -1

    :returns: The filtered data along slow time.
    :return type: numpy.ndarray
    """
    w_n = np.array(w_n)
    return _filtfilt_wn(data, w_n, 'high', 5, axis=axis)


def _filtfilt_band(data, cutoff, sampling_freq, band, axis=-2):
    """Filters an IQs map along the axial dimension. The band filtering is
    performed between [cutoff - band / 2 ; cutoff + band / 2].

    :param numpy.ndarray data: The beamformed IQs to filter (along axial axis)
    :param float cutoff: The cutoff frequency, in Hz
    :param float sampling_freq: The beamformed sampling frequency, in Hz
    :param float band: The band of the filter, in Hz
    :param int axis: The axis on which to perform the filtering

    :returns: The filtered data along axial time.
    :return type: numpy.ndarray
    """
    lf = cutoff - band / 2
    hf = cutoff + band / 2
    if lf / (sampling_freq / 2) > 0.1:
        data = us.cpu.filtfilt(data, lf, sampling_freq, 'high', axis=axis)
    if hf / (sampling_freq / 2) < 0.9:
        data = us.cpu.filtfilt(data, hf, sampling_freq, 'low', axis=axis)
    return data


def _unalias(cmaps, nyquists, p):
    """Conversion using the lookup tables, for Alias free.

    :param list cmaps: The Doppler color maps of each central frequencies
    :param list nyquists: The list of nyquists of each central frequencies
    :param int p: The p relation between f01 and f02

    :returns: The unaliased map.
    :return type: numpy.ndarray
    """
    q = p + 1

    # Lookup table
    cases = np.round(q * (cmaps[1] - cmaps[0]) / (2 * nyquists[0]))
    nn1 = cases.copy()
    nn1[(cases == -2) | (cases == 2)] = 0
    nn2 = cases.copy()
    nn2[cases == -2] = 1
    nn2[cases == 2] = -1

    # Unaliased map
    return (p / (p + q)) * (cmaps[0] + (q / p) * cmaps[1] +
                            2 * nyquists[0] * (nn1 + nn2))
