import numpy as np
import numpy.fft as fft
from skimage.filter import gaussian_filter

def get_freq(im):
    return fft.fftshift(fft.fft2(im))

def get_img(freq):
    return fft.ifft2(fft.ifftshift(freq))

def gauss_kernel(m, n, sigma):
    def gauss_pixel(x, y, sigma):
        return (1./(2.*np.pi*sigma**2.))*np.exp(-(x**2.+y**2.)/(2.*sigma**2.))
    xs = np.linspace(-(m-1)/2., (m-1)/2., m)
    ys = np.linspace((n-1)/2., -(n-1)/2., n)
    xs, ys = np.meshgrid(xs, ys)
    return gauss_pixel(xs, ys, sigma)

def Gaussian(im, sigma):
    return gaussian_filter(im, sigma, mode='reflect')

def gaussian_by_hand(im, sigma):
    assert np.max(im) <= 1
    n, m, _ = im.shape
    hp = gauss_kernel(m, n, sigma)
    hp_freq = get_freq(fft.ifftshift(hp))
    colors = []
    for c in 0, 1, 2:
        c = im[:, :, c]
        c_freq = get_freq(c)
        colors.append(np.abs(get_img(c_freq*hp_freq)))
    return np.dstack(colors)

def Laplacian(im, sigma):
    assert np.max(im) <= 1
    return im - Gaussian(im, sigma)

def unsharp_mask(im, sigma, amp):
    assert np.max(im) <= 1
    return im + amp*Laplacian(im, sigma)