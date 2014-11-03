
# CS294-26 Project 1 : Color Compositing
# by Rachel Albert
# This script loads a set of R, G, and B filtered images 
# and aligns and composites them into a single color image
# with excess border regions cropped.

import numpy as np
import skimage as sk
import skimage.io as skio

from metrics import *
from cleaning_functions import *


def image_split(image):
    im_size = len(im)/3
    b = im[:im_size]
    g = im[im_size:2*im_size]
    r = im[2*im_size:3*im_size]
    return r, g, b

def align(c1, c2, c3, trans_c1c3):
    (c1_r, c1_c), (c3_r, c3_c) = trans_c1c3
    d = [[c1_r, 0, c3_r],
         [c1_c, 0, c3_c]]
    rows, cols = c1.shape

    # here, instead of rolling/shifting the image I
    # find the maximum overlap for all three colors
    # given their translation

    c1 = c1[max(d[0]) - c1_r: rows + min(d[0]) - c1_r,
            max(d[1]) - c1_c: cols + min(d[1]) - c1_c]
    c2 = c2[max(d[0])       : rows + min(d[0]),
            max(d[1])       : cols + min(d[1])]
    c3 = c3[max(d[0]) - c3_r: rows + min(d[0]) - c3_r,
            max(d[1]) - c3_c: cols + min(d[1]) - c3_c]

    assert len(set([c1.shape, c2.shape, c3.shape])) == 1
    return c1, c2, c3

def find_alignment(c1, c2, radius):
    # find the middle of the image
    rows, cols = c1.shape
    rows /= 2
    cols /= 2
    def corr():
        for d_rows in np.arange(-radius, radius + 1):
            for d_cols in np.arange(-radius, radius + 1):
                # to test other metrics, replace ncc with appropriate
                # function name from metrics.py
                diff = ncc(c1[rows - radius: rows + radius + 1,
                              cols - radius: cols + radius + 1],
                           c2[rows - d_rows - radius: rows - d_rows + radius + 1,
                              cols - d_cols - radius: cols - d_cols + radius + 1])
                yield diff, (d_rows, d_cols)
    corr, trans = max(corr())
    return trans

def image_align(c1, c2, c3, radius):
    trans_c1 = find_alignment(c2, c1, radius)
    c1, c2, c3 = align(c1, c2, c3, (trans_c1, (0, 0)))
    trans_c3 = find_alignment(c2, c3, radius)
    return (trans_c1, trans_c3)

def pyramid_align(r, g, b):
    rows, cols = r.shape
    # number of pyramid levels is proportionate to image size
    max_s = int(np.log2(min(rows, cols)) - 6)
    max_s = max(max_s, 0)
    trans_gb = np.array([[0,0], [0, 0]])
    for s in range(max_s, 0, -1):
        scale = (2**s)
        c1, c2, c3 = align(r, g, b, trans_gb)
        
        c1 = sktr.rescale(c1, 1./scale)
        c2 = sktr.rescale(c2, 1./scale)
        c3 = sktr.rescale(c3, 1./scale)

        sm_trans = image_align(c1, c2, c3, 15)
        sm_trans = np.asarray(sm_trans)
        trans_gb = trans_gb + (sm_trans * scale)
        
    return trans_gb

impath = '../data/'

imnames =   ['bridge.tif',
             'cathedral.jpg',
             'emir.tif',
             'harvesters.tif',
             'lady.tif',
             'melons.tif',
             'monastery.jpg',
             'onion_church.tif',
             'selfie.tif',
             'settlers.jpg',
             'three_generations.tif',
             'tobolsk.jpg',
             'train.tif',
             'turkmen.tif',
             'village.tif']

#imnames = ['train.tif']
imnames = ['emir.tif', 'lady.tif', 'three_generations.tif']

for imname in imnames:
    print(imname)    
    im = skio.imread(impath+imname)
    im = sk.img_as_float(im)
    r, g, b = image_split(im)

    trans_gb = pyramid_align(r, g, b)
    print(trans_gb)

    color_image = np.dstack(align(r, g, b, trans_gb))

    # optional lines to save full-size color images
    fname = '../output/' + imname[:-4] + '_color.jpg'
    skio.imsave(fname, color_image)

    cropped_image = crop_border(color_image)
    
    #skio.imshow(cropped_image)
    #skio.show()
    fname = '../output/' + imname[:-4] + '_cropped.jpg'
    skio.imsave(fname, cropped_image)
