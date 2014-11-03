from image_io import *
from compute_lsqr import *
from get_mask import *

from skimage.transform import rescale

def get_mask_info(ys, xs):
    x_range = max(xs) - min(xs)
    y_range = max(ys) - min(ys)
    max_size = (y_range, x_range)
    top_left = (min(ys), min(xs))
    return max_size, top_left

def crop_to_mask(im, ys, xs):
    # Crop source to mask
    im_mask = get_mask(im, ys, xs)
    im_max, im_topleft = get_mask_info(ys, xs)
    im = im[min(ys):max(ys), min(xs):max(xs), :]                   ### color ###
    im_mask = im_mask[min(ys):max(ys), min(xs):max(xs), :]         ### color ###
    return im, im_mask

def fit_in_box(s, s_mask, s_max, t_max):
    # Resize foreground and mask so area fits in box
    y_ratio = float(t_max[0])/s_max[0]
    x_ratio = float(t_max[1])/s_max[1]
    if y_ratio > x_ratio:
        s = rescale(s, x_ratio)
        s_mask = rescale(s_mask, x_ratio)
    else:
        s = rescale(s, y_ratio)
        s_mask = rescale(s_mask, y_ratio)
    return s, s_mask

def align_images(s, t):
    # Create mask for source image
    instructions = 'Use the mouse to draw a loose polygon around the object.\
                    \nDouble-click on the last point to exit.'
    s_xs, s_ys = get_outline(s, instructions)

    # Draw bounding box on background
    instructions = 'Use the mouse to draw a box around the target area.\
                    \nDouble-click on the last point to exit.'
    t_xs, t_ys = get_outline(t, instructions)

    t_max, t_topleft = get_mask_info(t_ys, t_xs)
    s_max, s_topleft = get_mask_info(s_ys, s_xs)

    s, s_mask = crop_to_mask(s, s_ys, s_xs)
    s, s_mask = fit_in_box(s, s_mask, s_max, t_max)
    assert s.shape == s_mask.shape

    ty, tx = t_topleft
    sy, sx, sc = s_mask.shape
    off_y, off_x = (t_max[0] - sy, t_max[1] - sx)
    
    tinyt_topleft = (ty + off_y, tx + off_x)

    tinyt = t[ty + off_y : ty + off_y + sy,
              tx + off_x : tx + off_x + sx, :].copy()              ### color ###

    # Set t inside mask to s
    #t[ty + off_y : ty + off_y + sy,
    #  tx + off_x : tx + off_x + sx
    #][s_mask != 0] = s[s_mask != 0]

    return s, s_mask.astype(bool), tinyt, tinyt_topleft

