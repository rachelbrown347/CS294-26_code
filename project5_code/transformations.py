import numpy as np
from numpy.linalg import solve, LinAlgError
from skimage.draw import polygon


def findA(p, p_prime):
    # change p, p' to form [[xs], [ys], [1s]]
    assert p.shape == (3, 2)
    assert p_prime.shape == (3, 2)
    p = np.vstack([p.T, [1, 1, 1]])
    p_prime = np.vstack([p_prime.T, [1, 1, 1]])

    # find A s.t. A p = p'
    # must be in form a x = b for solve
    # (A p).T = (p').T
    # p.T A.T = p'.T
    try:
        AT = solve(p.T, p_prime.T)
    except LinAlgError:
        return np.eye(3, 3)
    return AT.T


def findAs(pts1, pts2):
    assert pts1.shape[0] == pts2.shape[0]

    As = []
    for p1, p2 in zip(pts1, pts2):
        As.append(findA(p1, p2))
    return np.array(As)


def get_mask(im, coords):
    assert coords.shape == (3, 2)
    xs, ys = coords.T[0], coords.T[1]
    rr, cc = polygon(ys, xs)
    mask = np.zeros(im.shape, dtype=bool)
    mask[rr, cc] = 1
    return mask


def get_warp(src_im, src_coords, tgt_coords, A):
    # rows, columns
    # assume images are the same size!
    tgt_ys, tgt_xs = np.where(get_mask(src_im, tgt_coords)[:, :, 0])
    # change tgt_pts to form [[xs], [ys], [1s]]
    tgt_pts = np.vstack([tgt_xs, tgt_ys, np.ones(tgt_xs.shape)])
    assert tgt_pts.shape[0] == 3

    src_pts = A.dot(tgt_pts)

    src_pts[0] = np.clip(src_pts[0], 0, src_im.shape[1]-1)
    src_pts[1] = np.clip(src_pts[1], 0, src_im.shape[0]-1)
    assert src_pts.dtype == float

    src_pts = np.round(src_pts).astype(int)
    colors = src_im[src_pts[1], src_pts[0], :]
    return colors, tgt_pts


def warp_image(src_im, src_shape, tgt_shape, tri):
    src_coords = src_shape[tri.simplices].copy()
    tgt_coords = tgt_shape[tri.simplices].copy()

    # assume images are the same size!
    tgt_im = np.zeros(src_im.shape, dtype=src_im.dtype)

    # get transformation matrices
    As = findAs(tgt_coords, src_coords)

    # iterate through triangles
    for src, tgt, A in zip(src_coords, tgt_coords, As):
        colors, tgt_pts = get_warp(src_im, src, tgt, A)
        # no interpolation, just rounding
        tgt_pts = np.round(tgt_pts).astype(int)
        tgt_im[tgt_pts[1], tgt_pts[0], :] = colors
    return tgt_im


def get_weighted_shapes(shape1, shape2, w):
    def outer_product(w, s):
        all_ss = np.outer(w, s.T)
        out_shape = (w.shape[0] * s.T.shape[0], s.T.shape[1])
        return all_ss.reshape(out_shape)
    outer1 = outer_product(1. - w, shape1)
    outer2 = outer_product(w, shape2)
    return np.round(outer1 + outer2)


def get_warp_frames(im1, shape1, im2, shape2, tri, steps):
    w = np.linspace(0., 1., steps)
    ws = get_weighted_shapes(shape1, shape2, w)

    frames = []
    for f in range(steps):
        f_shape = ws[2*f : 2*f + 2].T
        w_im1 = warp_image(im1, shape1, f_shape, tri)
        w_im2 = warp_image(im2, shape2, f_shape, tri)
        frames.append((1. - w[f]) * w_im1 + w[f] * w_im2)
    return frames