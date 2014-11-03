

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse import vstack
from scipy.sparse.linalg import lsqr

def construct_A2(s):
    imh, imw = s.shape
    n = imh*imw
    A = diags(
        diagonals=[1, -1, 1, -1, 1],
        offsets=[0, -1, -n, -n-imw, -2*n], 
        shape=[2*n + 1, n],
        format='csr', 
        dtype=float)
    A[n, -1] = 0
    A[-1, -imw] = 0
    return A

def compute_lsqr(s):
    imh, imw = s.shape
    A2 = construct_A2(s)
    b = A2.dot(s.ravel())
    v = lsqr(A2, b)[0]
    return v.reshape((imh, imw))
    
    