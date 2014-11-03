import numpy as np

def rms(a, b):
    i_avg = np.mean((a + b).ravel())
    return np.sqrt(((((a + b) - i_avg)**2).ravel().sum())/a.size)

def ncc(a, b):
    return ((a/np.linalg.norm(a)) * (b/np.linalg.norm(b))).ravel().sum()

def l2corr(a, b):
    return -((a-b)**2).sum().sum()