import numpy as np
import skimage.transform as sktr

from metrics import *

def crop_edge(image):
    def select_cols():
        max_border = np.floor(0.1*image.shape[1])
        for c in np.arange(max_border):
            yield ncc(image[:, max_border - c], 
                      image[:, max_border - c - 1]), c
    border = min(select_cols())[1]
    return image[:, border:]

def crop_border(image):
    cropped = image
    for s in range(4):
        cropped = crop_edge(sktr.rotate(cropped, 90, resize=True))
    return cropped