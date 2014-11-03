import numpy as np
from scipy.sparse import diags
from scipy.sparse import vstack
from scipy.sparse.linalg import lsqr

def shift(m, direction):
    padded = np.pad(m, [(d, 0) if d>0 else (0, -d) for d in direction], mode='constant')
    return padded[[np.s_[:sh] if d>0 else np.s_[-sh:] for sh, d in zip(m.shape, direction)]]

def inside(mask):
    return shift(mask, (-1, 0)) & shift(mask, (0, -1)) & shift(mask, (1, 0)) & shift(mask, (0, 1))

def construct_A4(s, s_border=[[]]):
    imh, imw = s.shape
    sy, sx = np.where(s_border)
    npx = imh*imw
                 # [x,x+1], [x,x-1], [y,y+1], [y,y-1]
    all_offsets = [[0, -1], [0, 1], [0, -imw], [0, imw]]
    As = []
    for offset in all_offsets:
        A = diags(
            diagonals=[1, -1],
            offsets=offset,
            shape=[npx, npx],
            format='csr',
            dtype=float)
        r, c = (A[imw*sy + sx, :] < 0).nonzero()
        A[(imw*sy + sx)[r], c] = 0
        r, c = A[imw*sy + sx, :].nonzero()
        As.append(A)
    return vstack(As)

def set_b(b, mask, values):
    bigmask = np.concatenate([mask, mask, mask, mask])
    b[bigmask] = values[bigmask]
    return b

def poisson_blend(s, s_mask, tinyt, t, tinyt_topleft, maximum=False):
    s_inside = inside(s_mask)
    s_border = s_mask & ~s_inside
    s_outside = ~s_inside

    A4 = construct_A4(s)
    t_prime = A4.dot(tinyt.ravel())
    s_prime = A4.dot(s.ravel())

    b = t_prime.copy()
    if maximum == True:
        max_prime = np.maximum(s_prime, t_prime)
        b = set_b(b, s_inside.ravel(), max_prime)
    else:
        b = set_b(b, s_inside.ravel(), s_prime)
    tinyt_values = np.concatenate([tinyt.ravel(), tinyt.ravel(), tinyt.ravel(), tinyt.ravel()])
    b = set_b(b, s_border.ravel(), tinyt_values)

    A4 = construct_A4(s, s_border=s_border)
    imh, imw = s.shape
    v = lsqr(A4, b)[0]
    out = v.reshape((imh, imw))

    tttly, tttlx = tinyt_topleft
    tty, ttx = tinyt.shape
    t[tttly:tttly + tty, tttlx:tttlx + ttx] = out
    return t


