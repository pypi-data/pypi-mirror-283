/* Operation between the data to filter (nb_x, nb_z) and tmp_x (nb_x, nb_ext).
It fills the tmp_x array with, for each nb_ext n, the value:
start0 - data[nb_ext - n], with start0 twice the first time sample for a given
data.
*/


template <typename T>
__device__ void core_init_start_sig(const T *data,
                                    T *output_dx,
                                    const int nb_ext,
                                    const int dim_time_samples,
                                    const int i)
{
    /* Initializes the start signal to be used in the filtering process.

      Input parameters:
      =================

      data:             Array containing the input data used for initializing
                        the start signal.

      output_dx:        Output to store the initialized start signal.

      nb_ext:           The number of extension points for the start signal.

      dim_time_samples: The number of time samples in the input data.

      i:                The current index of the data (depends on the current
                        thread / block), has been defined in the global caller.
    */
    T start0 = 2.0f * data[i * dim_time_samples];
    for (int it = 0; it < nb_ext; it++) {
        int idx_data = i * dim_time_samples + nb_ext - it;
        output_dx[i * nb_ext + it] = start0 - data[idx_data];
    }
}


extern "C" {
    __global__ void init_start_sig_float(const float *data, float *output_dx,
                                         const int nb_ext,
                                         const int dim_time_samples,
                                         const int nb_data) {
        /* Caller of the "init start signal" function on float data, more
           information in its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_data) {
            core_init_start_sig(data, output_dx, nb_ext, dim_time_samples, i);
        }
    }

    __global__ void init_start_sig_complex(const complex<float> *data,
                                           complex<float> *output_dx,
                                           const int nb_ext,
                                           const int dim_time_samples,
                                           const int nb_data) {
        /* Caller of the "init start signal" function on complex data, more
           information in its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_data) {
            core_init_start_sig(data, output_dx, nb_ext, dim_time_samples, i);
        }
    }
}
