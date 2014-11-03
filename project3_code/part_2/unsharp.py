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

def gaussian_by_hand(im, sigma):
    n, m = im.shape
    g = gauss_kernel(m, n, sigma)
    g_freq = get_freq(fft.ifftshift(g))
    c_freq = get_freq(im)
    return np.abs(get_img(c_freq*g_freq))

def Gaussian(im, sigma):
    return gaussian_filter(im, sigma, mode='reflect')

def Laplacian(im, sigma):
    assert np.max(im) <= 1
    return im - Gaussian(im, sigma)

def unsharp_mask(im, sigma, amp):
    assert np.max(im) <= 1
    return im + amp*Laplacian(im, sigma)