Project 5
Rachel Albert

This code is in python.

There is one line of bash code in this file (to create the gif). If you would like to run this code without bash, you may comment out line 100.

In addition to the standard libraries (itertools, os, glob, subprocess), you will also need:
numpy, scipy, matplotlib, and skimage (scikit-image).

To run the code, just run main.py. By default this will run all three sections:
morph_pair, morph_population, and caricaturize.

To run only a portion of the code, go to the main function at the bottom and comment out the functions you do not want to run.

NOTE about Danish Faces Database: 
In warp_population and caricaturize there is a parameter "danish_faces" since some special exceptions needed to be made regarding coordinate formatting. By default this parameter is set to FALSE so that the code can run in a self-contained manner without the danish faces database. However, it should still work if you set danish_faces to TRUE as long as the original danish faces database is in the same directory as the code.

::A Tour of the Code::
Happy Halloween by the way!




                                .-.
                   heehee      /aa \_
                             __\-  / )                 .-.
                   .-.      (__/    /        haha    _/oo \
                 _/ ..\       /     \               ( \v  /__
                ( \  u/__    /       \__             \/   ___)
                 \    \__)   \_.-._._   )  .-.       /     \
                 /     \             `-`  / ee\_    /       \_
              __/       \               __\  o/ )   \_.-.__   )
             (   _._.-._/     hoho     (___   \/           '-'
          boo '-'                        /     \
                                       _/       \    teehee
                                      (   __.-._/
                                       '-'


main.py

load_file : 
    Load an image/shape pair.
    If the corresponding shape file does not exist
        then run get_shape using the example image.

    :param fpath: directory for image ('./images/')
    :param fname: image file name ('hermione.jpg')
    :param example: example image path & file name ('examples/face_example.jpg')
    :return: im, im_shape

*   get_triangulation.py

    get_corr :
        This is the "get points from user" script.
    get_shape :
        This calls get_corr, then adds the four corners of the image and saves the shape.

morph_pair :
    Compute a sequence of morphs from one face to another.
    Parameters:
        fpath   = file path
        fname1  = starting image
        fname2  = ending image
        example = example image for corresponding points
        reverse = (True/False) add reversed frames to gif for looping
        steps   = number of steps from file1 to file2, inclusive

    IMPORTANT: both images and shape arrays must be the same size
               shape array must be in the form n x 2

    We load 2 files, compute the average shape, and compute the triangulation
    Then we create the weight values for each frame and weight each shape and crossfade.

    Finally we save each frame and create and save a gif of all the frames.

*   transformations.py
    
    findA :
        This computes 3x3 affine transformation matrix A from point arrays p and p'.
        (Find A such that A p = p')
        A simple transpose identity is used to get the variables into the proper form for numpy's solve function.

        Note: in cases where p == p', A is degenerate so we return the identity matrix.

    findAs :
        This just zips up the points and calls findA.

    get_mask :
        This finds a mask of the coordinates given. The mask is the same shape as the image.

    get_warp :
        This calls np.where(get_mask) to obtain the target xy points for the triangle vertices that are passed in from tgt_coords, then the matrix A is applied to obtain float source points.
        Instead of interpolating, the float source points are clipped to the image boundary and rounded to the nearest integer. Those points are then used to find the corresponding color values in the source image, which is returned as the target colors.
        We return the target colors and the target points.

    warp_image :
        Given an image, a source shape, a target shape, and a triangulation, this returns a warped image. We iterate through the triangles and call get_warp for each.

    get_weighted_shapes :
        Given two shapes and a list of weights, compute the outer product of (1-w) * shape1 and w * shape2, then round to the nearest integer.

    get_warp_frames :
        Given a number of steps, create evenly spaced weights, then apply get_weighted_shapes to get a list of shapes for each frame. Iterate through the frames, warp and weight each image to the corresponding shape, and return a list of frames.

morph_population :
    Load a set of population files,
        compute average face and average shape,
        save face and shape files.
    Parameters:
        face_files = list of file paths for population faces
        x_file = path to text file of population x coordinates
        y_file = path to text file of population y coordinates
        danish_faces = True/False (special exceptions for danish dataset)

    First, obtain list of population files using glob.
    Load each image and load the corresponding shape files.

    Note: shape files for populations were computed offline using python pandas.

    Find the average shape and warp all faces into the average. Then weight each face by 1/numfaces and sum.

    This function saves the average face and average shape.

caricaturize :
    Create a caricature of a face from another face.
    Parameters:
        fpath1  = path location for individual face
        fpath2  = path location for average face
        fname1  = individual face file name
        fname2  = average face name
        amt = what proportion of "caricature" to add
        danish_faces = True/False (special exceptions for danish dataset)

    Load a reference image (i.e. population average) and a face to be caricaturized (i.e. population image). Compute the average shape and obtain a Delaunay triangulation.

    Finally, subtract the difference between the reference and the individual, and add a proportion of that difference back to the individual to obtain the caricature shape. Warp the individual into the caricature shape. Do the same thing in the opposite direction to obtain "backward" caricature.









