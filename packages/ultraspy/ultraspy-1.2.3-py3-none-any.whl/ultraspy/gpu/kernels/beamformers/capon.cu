/* Actual Capon kernel. A few options are available:
- interpolation: 0 or 1 (none or linear)
- should_average: 0 or 1 (False or True)
- transmit_method: 0, 1 or 2 (centered, negative delays or positive delays)
- rx_apodization_method: 0 or 1 (Boxcar or Tukey window)
- rx_apodization_alpha: Factor (float) for our apodization window
- emitted_aperture: If True, the aperture is computed for emission elements
  also
*/

#define M_PI 3.14159265358979323846

#include "complex_utils.cu"
#include "probe_distances.cu"
#include "aperture_ratio.cu"
#include "interpolation.cu"
#include "apodization.cu"

#define PROBE_NB_ELEMENTS 128
#define HALF_NB_ELEMENTS 64


template <class T>
__device__ void capon_dots(T* matrix, T* normed, int window_size)
{
    /* Perform the Capon operation.

      Input parameters:
      =========
      matrix:      The matrix on which to perform the operation

      normed:      The inverse of the matrix

      window_size: The size of a window.
    */
    for (int e = 0; e < window_size; e++) {
        T tmp = 0;
        for (int j = 0; j < window_size; j++) {
            tmp += matrix[e * HALF_NB_ELEMENTS + j];
        }
        matrix[e] = tmp * normed[e];
    }
    T div = 0;
    for (int e = 0; e < window_size; e++) {
        div += normed[e] * matrix[e];
    }
    for (int e = 0; e < window_size; e++) {
        matrix[e] /= div;
    }
}


template <class T>
__device__ void dotFromDiag(T* matrix, int window_size)
{
    /* Perform the dot product of a diagonal matrix.

      Input parameters:
      =========
      matrix:      The matrix on which to perform the operation

      window_size: The size of a window.
    */
    int nb_r = HALF_NB_ELEMENTS;

    for (int i = 0; i < window_size; i++) {
        for (int j = i; j < window_size; j++) {
            T tmp = 0.0;
            for (int k = i; k < window_size; k++) {
                tmp += conjIfComplex(matrix[k * nb_r + i]) *
                       matrix[k * nb_r + j];
            }
            matrix[i * nb_r + j] = tmp;
            if (i != j) {
                matrix[j * nb_r + i] = conjIfComplex(tmp);
            }
        }
    }
}


template <class T>
__device__ void inverse(T* matrix, int window_size)
{
    /* Perform the inversion of a matrix.

      Input parameters:
      =========
      matrix:      The matrix on which to inverse

      window_size: The size of a window.
    */
    int nb_r = HALF_NB_ELEMENTS;

    for (int k = 0; k < window_size; k++) {
        if (matrix[k * nb_r + k] != T(0)) {
            matrix[k * nb_r + k] = T(1.0) / matrix[k * nb_r + k];
        }

        for (int i = k + 1; i < window_size; i++) {
            T tmp_sum = 0.0;
            for (int j = k; j < i; j++) {
                tmp_sum += matrix[i * nb_r + j] * matrix[j * nb_r + k];
            }
            if (matrix[i * nb_r + i] == T(0)) {
                matrix[i * nb_r + k] = T(0);
            } else {
                matrix[i * nb_r + k] = -tmp_sum / matrix[i * nb_r + i];
            }
        }
    }
}


template <class T>
__device__ void cholesky(T* matrix, int window_size)
{
    /* Perform the Cholesky decomposition.

      Input parameters:
      =========
      matrix:      The matrix on which to perform the decomposition

      window_size: The size of a window.
    */
    int nb_r = HALF_NB_ELEMENTS;

    for (int i = 0; i < window_size; i++) {
        for (int k = 0; k < i + 1; k++) {
            T tmp_sum = 0.0;
            for (int j = 0; j < k; j++) {
                tmp_sum += matrix[i * nb_r + j] *
                           conjIfComplex(matrix[k * nb_r + j]);
            }

            if (i == k) {
                matrix[i * nb_r + k] =
                    sqrt(matrix[i * nb_r + i] - tmp_sum);
            } else {
                if (matrix[k * nb_r + k] == T(0)) {
                    matrix[i * nb_r + k] = T(0);
                } else {
                    matrix[i * nb_r + k] = (T(1) / matrix[k * nb_r + k]) *
                                           (matrix[i * nb_r + k] - tmp_sum);
                }
            }
        }
        for (int k = i + 1; k < window_size; k++) {
            matrix[i * nb_r + k] = T(0);
        }
    }
}


template <class T>
__device__ void core_capon(const T *data,
                           const int start_data_idx,
                           const int is_iq,
                           const float *emitted_probe,
                           const float *received_probe,
                           const float *emitted_thetas,
                           const float *received_thetas,
                           const float *delays,
                           const int nb_t,
                           const int nb_ee,
                           const int nb_re,
                           const int nb_ts,
                           const float sampling_freq,
                           const float central_freq,
                           const float t0,
                           const float sound_speed,
                           const float *f_number,
                           const float x,
                           const float y,
                           const float z,
                           complex<float> *focused_data,
                           complex<float> *grid,
                           const int nb_pixels,
                           const int diagonal_loading_mode,
                           const float l_prop,
                           const float delta_l,
                           const int interpolation_method,
                           const int should_average,
                           const int rx_apodization_method,
                           const float rx_apodization_alpha,
                           const int emitted_aperture,
                           const int compound,
                           const int reduce,
                           const int i)
{
    /* Capon algorithm kernel, called in parallel for each pixel. It does, for
    each transmission:
        - computes the distances between the pixel to beamform and the probe /
          distance in the meridional plane, to get the aperture ratios. If it
          is not visible by the probe element, it is skipped.
        - computes the transmissions distances, as the closest probe element to
          each pixel
        - for each element of the received probe, computes the reception
          distance. If needed, a phase rotation is performed (for I/Qs) and,
          then, we get the corresponding interpolated data
        - builds the coherence matrices of the various sub-windows of the
          focused data, and average them
        - apply the robust Capon method (forward-backward or diagonal loading)
        - inverse the matrix then apply the Capon formula
        - use the resulting weights to ponderate the focused data

      Input parameters:
      =================

      data:                  The RFs to beamform, of shape (nb_a, nb_e, nb_t).

      start_data_idx:        The index of the first data to consider (if we are
                             working on a packet, this tells us from where to
                             expect to find the related frame).

      is_iq:                 Is set to 1 if the data are I/Qs (thus a phase
                             rotation is required).

      emitted_probe:         The positions of the elements of the emission
                             probe (three dimensional).

      received_probe:        The positions of the elements of the reception
                             probe (three dimensional).

      emitted_thetas:        The thetas of the emission probe (per cycle).

      received_thetas:       The thetas of the reception probe (per cycle).

      delays:                The array with all the delays of our emission
                             sequences.

      nb_t:                  The number of transmissions in our data.

      nb_ee:                 The number of emitted elements in the probe.

      nb_re:                 The number of received elements in the probe.

      nb_ts:                 The number of time samples.

      sampling_freq:         The sampling frequency of the acquisition.

      central_freq:          The central frequency of the probe used for the
                             acquisition.

      t0:                    The initial time of recording.

      sound_speed:           The speed of sound of the scanned medium.

      f_number:              The aperture of the probe elements. For any
                             position of the medium, (z / f_number)-width
                             elements of the probe may have an aperture wide
                             enough to observe at depth z. Two-dimensional, for
                             both the lateral and elevational axes.

      x:                     The x position of the current pixel.

      y:                     The y position of the current pixel.

      z:                     The z position of the current pixel.

      focused_data:          The focused data to fill at a given pixel.

      grid:                  The grid where to store the beamformed results.

      nb_pixels:             The number of pixels in the grid.

      diagonal_loading_mode: If set to True, will perform the diagonal loading
                             mode instead of standard (default) forward /
                             backward.

      l_prop:                The proportion of the delays to use to constitute
                             one window, should be ]0, 0.5].

      delta_l:               The delta factor to enhance the diagonal loading,
                             should be [1, 1000].

      interpolation_method:  The interpolation method to use (can be 0 (no
                             interpolation) or 1 (linear)).

      should_average:        This option defines if we average the results
                             after beamforming (by the number of locally
                             concerned elements, check f_number for details).
                             If 1, Delay And Mean is performed, else cas, Delay
                             And Sum.

      rx_apodization_method: The apodization method at reception to apply (can
                             be either 0 (boxcar) or 1 (tukey)).

      rx_apodization_alpha:  The coefficient to provide to our apodization
                             window (if 0, no apodization).

      emitted_aperture:      Set to 1 if the emitted elements have an aperture,
                             else case, 0.

      compound:              If set to 0, will not compound along the
                             transmissions.

      reduce:                If set to 0, will not reduce along the probe
                             elements.

      i:                     The current index of the data (depends on the
                             current thread / block), has been defined in the
                             global caller.
    */
    int base_focused_data = i * nb_re;
    int dim_nb_t = compound == 1 ? 1 : nb_t;
    int dim_nb_re = reduce == 1 ? 1 : nb_re;

    for (int it = 0; it < nb_t; it++) {
        float transmission = 10;  // 10m for infinity
        for (int iee = 0; iee < nb_ee; iee++) {
            float e_dist_to_x, e_dist_to_y, e_dists;
            get_distances(emitted_probe, nb_t, nb_ee, it, iee, x, y, z,
                          &e_dist_to_x, &e_dist_to_y, &e_dists);

            int base = it * nb_ee + iee;
            if (emitted_aperture == 1) {
                float e_ratio = get_aperture_ratio(
                    z, e_dist_to_x, e_dist_to_y, e_dists,
                    emitted_thetas[base], f_number);
                if (abs(e_ratio) > 1) {
                    continue;
                }
            }

            transmission = min(transmission,
                               delays[base] * sound_speed + e_dists);
        }

        if (transmission >= 10) {
            continue;
        }

        int count_re = 0;
        for (int ire = 0; ire < nb_re; ire++) {
            float r_dist_to_x, r_dist_to_y, r_dists;
            get_distances(received_probe, nb_t, nb_re, it, ire, x, y, z,
                          &r_dist_to_x, &r_dist_to_y, &r_dists);

            int base = it * nb_re + ire;
            float r_ratio = get_aperture_ratio(
                z, r_dist_to_x, r_dist_to_y, r_dists,
                received_thetas[base], f_number);

            if (abs(r_ratio) > 1) {
                continue;
            }

            float reception = r_dists;
            float tau = (reception + transmission) / sound_speed;
            float delay = tau - t0;
            float data_idx = delay * sampling_freq;

            // Get the corresponding data
            int base_idx = start_data_idx + it * nb_re * nb_ts + ire * nb_ts;
            complex<float> tmp = interpolate(data, base_idx, data_idx, nb_ts,
                                             interpolation_method);

            if (tmp != T(0)) {
                // Default to 1 for the apodization method here
                tmp *= get_apodization_weight(
                    r_ratio, rx_apodization_alpha, rx_apodization_method);

                if (is_iq == 1) {
                    // Phase rotation for IQs (does nothing if data are RFs)
                    complex<float> phase (0, 2 * M_PI * central_freq * tau);
                    tmp *= exp(phase);
                }

                // Add it to the focused_data elements
                int ii = base_focused_data + count_re;
                focused_data[base_focused_data + count_re] += tmp;
                count_re++;
            }
        }

        // Get window_size, nb_windows, delta
        int nb_elements = count_re;
        int window_size = int(floorf(nb_elements * l_prop));
        int nb_windows = nb_elements - window_size + 1;

        // Allocate memory for a correlation matrix, of pre-defined shape
        complex<float> correlation_r[HALF_NB_ELEMENTS * HALF_NB_ELEMENTS];

        // Fills the correlation matrix
        complex<float> trace = 0;
        bool is_empty = true;
        for (int ix = 0; ix < window_size; ix++) {
            for (int iy = 0; iy < window_size; iy++) {
                int idx = ix * HALF_NB_ELEMENTS + iy;
                correlation_r[idx] = T(0);
                for (int iw = 0; iw < nb_windows; iw++) {
                    int ib = base_focused_data + iw;
                    correlation_r[idx] += focused_data[ib + iy] *
                                          conjIfComplex(focused_data[ib + ix]);
                }
                if (correlation_r[idx] != T(0)) {
                    is_empty = false;
                }
                correlation_r[idx] /= nb_windows;
                if (ix == iy) {
                    trace += correlation_r[idx];
                }
            }
        }

        if (is_empty) {
            continue;
        }

        if (diagonal_loading_mode == 0) {
            // Forward backward
            for (int ix = 0; ix < window_size; ix++) {
                for (int iy = 0; iy < window_size - ix; iy++) {
                    int new_ix = (window_size - 1 - iy);
                    int new_iy = window_size - 1 - ix;
                    complex<float> tmp =
                        (correlation_r[new_ix * HALF_NB_ELEMENTS + new_iy] +
                         correlation_r[ix * HALF_NB_ELEMENTS + iy]) / T(2);
                    correlation_r[new_ix * HALF_NB_ELEMENTS + new_iy] = tmp;
                    correlation_r[ix * HALF_NB_ELEMENTS + iy] = tmp;
                }
            }
        }
        else if (diagonal_loading_mode == 1) {
            // Diagonal loading
            complex<float> diag_loading = trace / T(delta_l * window_size);
            for (int ix = 0; ix < window_size; ix++) {
                correlation_r[ix * HALF_NB_ELEMENTS + ix] += diag_loading;
            }
        }

        // Inverse using Cholesky
        cholesky(correlation_r, window_size);
        inverse(correlation_r, window_size);
        dotFromDiag(correlation_r, window_size);
        complex<float> normed_a[HALF_NB_ELEMENTS];
        for (int ix = 0; ix < window_size; ix++) {
            normed_a[ix] = T(1.0) / T(powf(window_size, 0.5));
        }
        capon_dots(correlation_r, normed_a, window_size);

        // correlation_r first line is used for the weights, the second line is
        // used for the sum of windows.
        complex<float> result = 0.0;
        for (int e = 0; e < window_size; e++) {
            correlation_r[HALF_NB_ELEMENTS + e] = 0.0;
            for (int iw = 0; iw < nb_windows; iw++) {
                int ib = base_focused_data + iw;
                correlation_r[HALF_NB_ELEMENTS + e] += focused_data[ib + e];
            }
            result += correlation_r[HALF_NB_ELEMENTS + e] * correlation_r[e];
        }

        if (!isnan(abs(result)) && window_size > 0) {
            grid[i] += result / T(window_size);
        }
    }
}


extern "C" {
    __global__ void capon_float(
            const float *data, const int is_iq,
            const float *emitted_probe, const float *received_probe,
            const float *emitted_thetas, const float *received_thetas,
            const float *delays,
            const int nb_t, const int nb_ee, const int nb_re, const int nb_ts,
            const float sampling_freq, const float central_freq, const float t0,
            const float sound_speed, const float *f_number,
            const float *x_coords, const float *y_coords, const float *z_coords,
            const int dim_nb_t, const int dim_nb_re,
            complex<float> *focused_data, complex<float> *grid,
            const int nb_pixels, const int diagonal_loading_mode,
            const float l_prop, const float delta_l,
            const int interpolation_method, const int should_average,
            const int rx_apodization_method, const float rx_apodization_alpha,
            const int emitted_aperture, const int compound, const int reduce)
    {
        /* Caller of the "capon" beamformer, more information in its device
           definition. It is expecting RFs (data of float type).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            int i_in_transmission = (int)i % (dim_nb_re * nb_pixels);
            int i_in_elements = (int)i_in_transmission % nb_pixels;
            int idx_p = (int)i_in_elements % nb_pixels;

            core_capon(data, 0, is_iq, emitted_probe, received_probe,
                       emitted_thetas, received_thetas, delays,
                       nb_t, nb_ee, nb_re, nb_ts,
                       sampling_freq, central_freq, t0, sound_speed, f_number,
                       x_coords[idx_p], y_coords[idx_p], z_coords[idx_p],
                       focused_data, grid, nb_pixels,
                       diagonal_loading_mode, l_prop, delta_l,
                       interpolation_method, should_average,
                       rx_apodization_method, rx_apodization_alpha,
                       emitted_aperture, compound, reduce, i);
        }
    }

    __global__ void capon_complex(
            const complex<float> *data, const int is_iq,
            const float *emitted_probe, const float *received_probe,
            const float *emitted_thetas, const float *received_thetas,
            const float *delays,
            const int nb_t, const int nb_ee, const int nb_re, const int nb_ts,
            const float sampling_freq, const float central_freq, const float t0,
            const float sound_speed, const float *f_number,
            const float *x_coords, const float *y_coords, const float *z_coords,
            const int dim_nb_t, const int dim_nb_re,
            complex<float> *focused_data, complex<float> *grid,
            const int nb_pixels, const int diagonal_loading_mode,
            const float l_prop, const float delta_l,
            const int interpolation_method, const int should_average,
            const int rx_apodization_method, const float rx_apodization_alpha,
            const int emitted_aperture, const int compound, const int reduce)
    {
        /* Caller of the "capon" beamformer, more information in its device
           definition. It is expecting IQs (data of complex type).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            int i_in_transmission = (int)i % (dim_nb_re * nb_pixels);
            int i_in_elements = (int)i_in_transmission % nb_pixels;
            int idx_p = (int)i_in_elements % nb_pixels;

            core_capon(data, 0, is_iq, emitted_probe, received_probe,
                       emitted_thetas, received_thetas, delays,
                       nb_t, nb_ee, nb_re, nb_ts,
                       sampling_freq, central_freq, t0, sound_speed, f_number,
                       x_coords[idx_p], y_coords[idx_p], z_coords[idx_p],
                       focused_data, grid, nb_pixels,
                       diagonal_loading_mode, l_prop, delta_l,
                       interpolation_method, should_average,
                       rx_apodization_method, rx_apodization_alpha,
                       emitted_aperture, compound, reduce, i);
        }
    }

    __global__ void packet_capon_float(
            const float *data, const int is_iq,
            const float *emitted_probe, const float *received_probe,
            const float *emitted_thetas, const float *received_thetas,
            const float *delays,
            const int nb_f, const int nb_t,
            const int nb_ee, const int nb_re, const int nb_ts,
            const float sampling_freq, const float central_freq, const float t0,
            const float sound_speed, const float *f_number,
            const float *x_coords, const float *y_coords, const float *z_coords,
            const int dim_nb_t, const int dim_nb_re,
            complex<float> *focused_data, complex<float> *grid,
            const int total_nb_pixels, const int diagonal_loading_mode,
            const float l_prop, const float delta_l,
            const int interpolation_method, const int should_average,
            const int rx_apodization_method, const float rx_apodization_alpha,
            const int emitted_aperture, const int compound, const int reduce)
    {
        /* Caller of the "pdas" beamformer working on packet of data, more
           information in its device definition. It is expecting RFs (data of
           float type).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < total_nb_pixels) {
            int i_in_transmission = (int)i % (dim_nb_re * total_nb_pixels);
            int i_in_elements = (int)i_in_transmission % total_nb_pixels;
            int i_in_pixels = (int)i_in_elements % nb_f;

            int idx_p = (int)i_in_elements / nb_f;
            int idx_f = i_in_pixels;

            int data_start_idx = idx_f * nb_t * nb_re * nb_ts;

            core_capon(data, data_start_idx, is_iq,
                       emitted_probe, received_probe,
                       emitted_thetas, received_thetas, delays,
                       nb_t, nb_ee, nb_re, nb_ts,
                       sampling_freq, central_freq, t0, sound_speed, f_number,
                       x_coords[idx_p], y_coords[idx_p], z_coords[idx_p],
                       focused_data, grid, total_nb_pixels,
                       diagonal_loading_mode, l_prop, delta_l,
                       interpolation_method, should_average,
                       rx_apodization_method, rx_apodization_alpha,
                       emitted_aperture, compound, reduce, i);
        }
    }

    __global__ void packet_capon_complex(
            const complex<float> *data, const int is_iq,
            const float *emitted_probe, const float *received_probe,
            const float *emitted_thetas, const float *received_thetas,
            const float *delays,
            const int nb_f, const int nb_t,
            const int nb_ee, const int nb_re, const int nb_ts,
            const float sampling_freq, const float central_freq, const float t0,
            const float sound_speed, const float *f_number,
            const float *x_coords, const float *y_coords, const float *z_coords,
            const int dim_nb_t, const int dim_nb_re,
            complex<float> *focused_data, complex<float> *grid,
            const int total_nb_pixels, const int diagonal_loading_mode,
            const float l_prop, const float delta_l,
            const int interpolation_method, const int should_average,
            const int rx_apodization_method, const float rx_apodization_alpha,
            const int emitted_aperture, const int compound, const int reduce)
    {
        /* Caller of the "capon" beamformer, more information in its device
           definition. It is expecting IQs (data of complex type).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < total_nb_pixels) {
            int i_in_transmission = (int)i % (dim_nb_re * total_nb_pixels);
            int i_in_elements = (int)i_in_transmission % total_nb_pixels;
            int i_in_pixels = (int)i_in_elements % nb_f;

            int idx_p = (int)i_in_elements / nb_f;
            int idx_f = i_in_pixels;

            int data_start_idx = idx_f * nb_t * nb_re * nb_ts;

            core_capon(data, data_start_idx, is_iq,
                       emitted_probe, received_probe,
                       emitted_thetas, received_thetas, delays,
                       nb_t, nb_ee, nb_re, nb_ts,
                       sampling_freq, central_freq, t0, sound_speed, f_number,
                       x_coords[idx_p], y_coords[idx_p], z_coords[idx_p],
                       focused_data, grid, total_nb_pixels,
                       diagonal_loading_mode, l_prop, delta_l,
                       interpolation_method, should_average,
                       rx_apodization_method, rx_apodization_alpha,
                       emitted_aperture, compound, reduce, i);
        }
    }
}
