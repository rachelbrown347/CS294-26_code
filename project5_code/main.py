import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import os.path
from scipy.spatial import Delaunay
from glob import glob
import subprocess

from get_triangulation import get_shape
from transformations import warp_image, get_warp_frames


def load_file(fpath, fname, example):
    """
    Load an image/shape pair.
    If the corresponding shape file does not exist
        then run get_shape using the example image.

    :param fpath: directory for image ('./images/')
    :param fname: image file name ('hermione.jpg')
    :param example: example path & file name ('examples/face_example.jpg')
    :return: im, im_shape
    """

    im = plt.imread(os.path.join(fpath, fname))
    ex_im = plt.imread(os.path.join(fpath, example))

    shape_name_path = os.path.join(fpath, fname[:-4] + '_shape.txt')
    if os.path.isfile(shape_name_path):
        im_shape = np.loadtxt(shape_name_path)
    else:
        im_shape = get_shape(im, ex_im, shape_name_path)
    return im, im_shape


def morph_pair():
    """
    Compute a sequence of morphs from one face to another.
    Parameters:
        fpath   = file path
        fname1  = starting image
        fname2  = ending image
        example = example image for corresponding points
        reverse = (True/False) add reversed frames to gif for looping
        steps   = number of steps from file1 to file2, inclusive
    :return: None
    """

    print('morphing pair...')

    fpath   = './images/'
    fname1  = 'beatle1.jpg'
    fname2  = 'beatle2.jpg'
    example = 'examples/face_example.jpg'

    reverse = True
    steps = 10
    assert 2*steps < 100, 'what are you doing?!? are you *trying* to run out of memory?!?'

    print('loading files...')
    im1, shape1 = load_file(fpath, fname1, example)
    im2, shape2 = load_file(fpath, fname2, example)

    assert im1.shape       == im2.shape,    'images must be the same size'
    assert shape1.shape    == shape2.shape, 'shape arrays must be the same size'
    assert shape1.shape[1] == 2,            'shape array must be shape n x 2'

    avg_shape = np.round((shape1 + shape2)/2.)
    tri = Delaunay(avg_shape)

    print('warping frames...')
    frames = get_warp_frames(im1, shape1, im2, shape2, tri, steps)

    if reverse:
        frame_order = it.chain(frames, frames[::-1])
    else:
        frame_order = frames

    out_name = '_'.join([fname1[:-4], fname2[:-4]])
    out_path = os.path.join('./output/', out_name)

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    print('saving frames...')
    for i, frame in enumerate(frame_order):
        plt.imsave(os.path.join(out_path, 'frame{:0>2d}.jpg'.format(i)), frame/255.)

    im1_2_avg = warp_image(im1, shape1, avg_shape, tri)
    im2_2_avg = warp_image(im2, shape2, avg_shape, tri)
    avg_face = 0.5 * im1_2_avg + 0.5 * im2_2_avg

    plt.imsave('./output/' + fname1[:-4] + '2' + fname2[:-4] + '_avg.jpg', im1_2_avg/255.)
    plt.imsave('./output/' + fname2[:-4] + '2' + fname1[:-4] + '_avg.jpg', im2_2_avg/255.)
    plt.imsave('./output/' + fname1[:-4] + '_' + fname2[:-4] + '_avg.jpg', avg_face/255.)

    print('creating gif...')
    arg1s = glob(out_path + '/*.jpg')
    arg2 = './output/' + out_name + '.gif'
    subprocess.check_output('convert -delay 5 -loop 0'.split() + arg1s + [arg2])

    print('warping complete!')
    return


def morph_population():
    """
    Load a set of population files,
        compute average face and average shape,
        save face and shape files.
    Parameters:
        face_files = list of file paths for population faces
        x_file = path to text file of population x coordinates
        y_file = path to text file of population y coordinates
        danish_faces = True/False (special exceptions for danish dataset)
    :return: None
    """

    print('morphing population...')
    danish_faces = False

    if danish_faces == True:
        face_files = glob('./imm_face_db/*-2*.jpg')
        # do not include files 2, 3, and 4 because they are B&W
        del face_files[2:5]
        x_file = 'danish_xs.txt'
        y_file = 'danish_ys.txt'
    else:
        face_files = glob('./images/beatle*.jpg')
        x_file = 'beatle_xs.txt'
        y_file = 'beatle_ys.txt'

    print('loading files...')

    # optional arg num loads only the first num files
    def load_pop_files(files, num=len(face_files)):
        images = []
        for f in files[:num]:
            images.append(plt.imread(f))
        xs = np.loadtxt(x_file)[:num]
        ys = np.loadtxt(y_file)[:num]
        return images, xs, ys
    images, xs, ys = load_pop_files(face_files)

    avg_shape = np.array([np.mean(xs, axis=0), np.mean(ys, axis=0)]).T
    avg_shape = np.round(avg_shape).astype(int)
    tri = Delaunay(avg_shape)

    print('warping faces...')
    warps = []
    for im, x, y in zip(images, xs, ys):
        src_shape = np.array([x, y]).T
        warps.append(warp_image(im, src_shape, avg_shape, tri))

    print('averaging faces...')
    w = 1./len(warps)
    warps = np.array(warps)
    avg_face = np.sum(w * warps, axis=0)
    if danish_faces == True:
        out_face  = './output/danish_avg.jpg'
        out_shape = './output/danish_avg_shape.txt'
    else:
        out_face  = './output/beatle_avg.jpg'
        out_shape = './output/beatle_avg_shape.txt'
    plt.imsave(out_face, avg_face/255.)
    np.savetxt(out_shape, avg_shape, fmt='%.0f')
    print('averaging complete!')
    return


def caricaturize():
    """
    Create a caricature of a face from another face.
    Parameters:
        fpath1  = path location for individual face
        fpath2  = path location for average face
        fname1  = individual face file name
        fname2  = average face name
        amt = what proportion of "caricature" to add
        danish_faces = True/False (special exceptions for danish dataset)
    :return: None
    """

    print('caricaturizing...')

    danish_faces = False

    fpath = './images/'

    if danish_faces:
        fname1  = 'myface_green.jpg'
        fname2  = 'danish_avg.jpg'
        example = 'examples/danish_example.jpg'
    else:
        fname1  = 'beatle_avg.jpg'
        fname2  = 'beatle1.jpg'
        example = 'examples/face_example.jpg'

    amt = 0.8

    im1, shape1 = load_file(fpath, fname1, example)
    im2, shape2 = load_file(fpath, fname2, example)

    assert im1.shape       == im2.shape,    'images must be the same size'
    assert shape1.shape    == shape2.shape, 'shape vectors must be the same size'
    assert shape1.shape[1] == 2,            'shape vectors must be shape n x 2'

    if danish_faces:
        fixed_xs = np.add(-shape1[:-4].T[0], im1.shape[1])
        fixed_xs = np.hstack([fixed_xs, shape1[-4:, 0]])
        shape1[:, 0] = fixed_xs

    avg_shape = np.round((shape1 + shape2)/2.)
    tri = Delaunay(avg_shape)

    difference = np.subtract(shape1, avg_shape)
    fwd_shape  = np.add(shape1, amt * difference)
    bkwd_shape = np.subtract(shape1, amt * difference)

    fwd_caricature  = warp_image(im1, shape1, fwd_shape, tri)
    bkwd_caricature = warp_image(im1, shape1, bkwd_shape, tri)

    plt.imsave('./output/' + '_'.join([fname1[:-4], 'to', fname2[:-4], 'fwd',  '{:.0f}.jpg'.format(10*amt)]),  fwd_caricature/255.)
    plt.imsave('./output/' + '_'.join([fname1[:-4], 'to', fname2[:-4], 'bkwd', '{:.0f}.jpg'.format(10*amt)]), bkwd_caricature/255.)

    print('caricaturizing complete!')
    return


def main():
    morph_pair()
    morph_population()
    caricaturize()
    return

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('main()')
    main()