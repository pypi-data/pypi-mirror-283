# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#distutils: language=c++
#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: embedsignature=True
# cython: language_level=3

from cython.operator import dereference as deref
from libcpp.vector cimport vector
from libc.stdint cimport uint32_t, uint64_t, int32_t, int64_t
import numpy as np
cimport cython
cimport numpy as np

np.import_array()

ctypedef uint32_t cl_uint

cdef extern from *:
    int NPY_LIKELY(int)
    int NPY_UNLIKELY(int)

cdef class flt_vector_as_array:
    cdef readonly object __array_interface__
    cdef vector[float] *buf
    cdef void set_data(self, vector[float]& other) except *

cdef class dbl_vector_as_array:
    cdef readonly object __array_interface__
    cdef vector[double] *buf
    cdef void set_data(self, vector[double]& other) except *

cdef class u32_vector_as_array:
    cdef readonly object __array_interface__
    cdef vector[uint32_t] *buf
    cdef void set_data(self, vector[uint32_t]& other) except *

cdef class u64_vector_as_array:
    cdef readonly object __array_interface__
    cdef vector[uint64_t] *buf
    cdef void set_data(self, vector[uint64_t]& other) except *

cdef class i32_vector_as_array:
    cdef readonly object __array_interface__
    cdef vector[int32_t] *buf
    cdef void set_data(self, vector[int32_t]& other) except *

cdef class i64_vector_as_array:
    cdef readonly object __array_interface__
    cdef vector[int64_t] *buf
    cdef void set_data(self, vector[int64_t]& other) except *