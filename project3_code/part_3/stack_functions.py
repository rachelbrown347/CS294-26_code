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

def apply_mask(im, mask, sign):
        channels = []
        for j in 0, 1, 2:
            channels.append(im[:, :, j] * (mask if sign else 1-mask))
        return np.dstack(channels)

def apply_mask_stack(im_stack, mask_stack, sign):
    for i, (im, mask) in enumerate(zip(im_stack, mask_stack)):
        im_stack[i] = apply_mask(im, mask, sign)
    return im_stack

def save_stacks(fname, stack, plt_shape):
    r, c = plt_shape
    fig, axes = plt.subplots(nrows=r, ncols=c)
    fig.set_size_inches(18.5,10.5)

    for i, (ax, im) in enumerate(zip(axes.flat, stack), start=1):
        im = rescale_intensity(im, in_range=(-0.25, 0.25), out_range=(0, 1))
        ax.imshow(im)
        if i <= c:
            ax.set_title('Img 1 # {}'.format(i%c if i%c!=0 else c))
        elif i <= 2*c:
            ax.set_title('Img 2 # {}'.format(i%c if i%c!=0 else c))
        else:
            ax.set_title('Composite # {}'.format(i%c if i%c!=0 else c))
        ax.axis('off')
        fig.tight_layout()
    
    new_fname = fname + '_stacks.jpg'
    plt.savefig(new_fname, dpi=100)

def composite(images, c_stack, mask, levels):
    im1, im2 = images
    im1_low = apply_mask(Gaussian(im1,  2**(levels)), 
                         Gaussian(mask, 2**(levels)), 1)
    im2_low = apply_mask(Gaussian(im2,  2**(levels)), 
                         Gaussian(mask, 2**(levels)), 0)
    low_f_comp = sum([im1_low, im2_low])
    return sum(c_stack, low_f_comp)






