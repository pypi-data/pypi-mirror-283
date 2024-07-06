/* Some utility functions for complex numbers.
*/


template <typename T>
__device__ T conjIfComplex(T v) {
    return T(0);
}

template <>
__device__ float conjIfComplex(float v) {
    return v;
}

template <>
__device__ complex<float> conjIfComplex(complex<float> v) {
    return conj(v);
}
