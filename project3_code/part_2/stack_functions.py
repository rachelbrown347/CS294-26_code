import matplotlib.pyplot as plt
import numpy as np
import skimage.transform as sktr
from skimage.exposure import rescale_intensity

from unsharp import *

def create_fstack(im, imfilter, levels):
    f_imgs = []
    for i, sigma in enumerate(2**np.arange(0, levels, 1)):
        f_imgs.append(imfilter(im, sigma))
    return f_imgs

def create_stack(im, levels):
    gstack = create_fstack(im, Gaussian, levels)
    stack = [im - gstack[0]]
    for i in range(0, len(gstack)-1, 1):
        stack.append(gstack[i] - gstack[i+1])
    return stack

def apply_mask_stack(im_stack, mask_stack, sign):
    for i, (im, mask) in enumerate(zip(im_stack, mask_stack)):
        im_stack[i] = im*(mask if sign else 1-mask)
    return im_stack

def save_stacks(fname, stack, plt_shape):
    r, c = plt_shape
    fig, axes = plt.subplots(nrows=r, ncols=c)
    fig.set_size_inches(18.5,10.5)
    sigma_list = [0, 1, 2, 4, 8, 16]
    for i, (ax, im) in enumerate(zip(axes.flat, stack), start=1):
        if i > c:
            ax.set_title('Laplacian ({0} - {1})'.format(sigma_list[i-c-1], sigma_list[i-c]))
            im = rescale_intensity(im, in_range=(-.25, .25), out_range=(0, 1))
            im = np.mean(im, 2)
        else:
            ax.set_title('Gaussian (Sigma={})'.format(sigma_list[i]))
        ax.imshow(im, cmap='gray')
        ax.axis('off')
        fig.tight_layout()
    
    new_fname = fname + '_stacks.jpg'
    plt.savefig(new_fname, dpi=300)