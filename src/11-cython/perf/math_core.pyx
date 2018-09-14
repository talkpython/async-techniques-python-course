from libc.math cimport sqrt

import cython

def do_math(start: cython.float = 0, num: cython.float = 10):
    pos: cython.float = start
    k_sq: cython.float = 1000 * 1000

    with nogil:
        while pos < num:
            pos += 1
            sqrt((pos - k_sq) * (pos - k_sq))
