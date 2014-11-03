Hello, and welcome to Project 3!
Clippy the paperclip is taking the night off, so I'll be your host for this evening. 
To start, let me fill you in on the new packages you'll be needing to run this code.
You will need:
numpy, matplotlib, math, and skimage, including
skimage.filter, skimage.exposure, and skimage.transform

Ok, now that we've got that out of the way, let's go through each part of the code 
one by one, shall we?

Part 0:
Unsharp.py
This file imports fourier transforms and a built-in gaussian filter from skimage.
I also implemented the gaussian by hand but I don't use it because it's missing
some useful features like tri-color fft and  sophisticated edge handling.
By the way, I also implemented the color fft in part 1, but again, I don't use it.
The other important thing about this file is that it implements a Laplacian filter
and an unsharp mask filter.

Part 1:
Unsharp.py (see Part 0)
Align_Images.py
This is a re-implementation of the code that was given for aligning and cropping
images in MATLAB, but in Python. Note that I had already spent WAY too much time
writing this before someone graciously posted a python version on Piazza, so I just
used what I already had.
ALSO, this code has one extra little function that combines a high frequency
version of image 1 with a low frequency version of image 2, and averages them.

Part 2:
Unsharp.py (see Part 0)
Stack_Functions.py
This is a beautiful peice of code. For me, at least. This gorgeous text file
can create a set of images with N levels. The sigma of the gaussian at each 
level is a power of two higher than the previous level. For each stack, you
can implement whatever filter you want (Gaussian, Laplacian, etc) by passing
in the filter function to create_fstack.
If you just want a normal Laplacian stack, it can do that, too! Just use the
function create_stack, which calls create_fstack. You can also apply a mask here
(we don't use that till part 3 though).
Finally, the function save_stacks creates a lovely, well-labeled, well-normalized,
and VERY HIGH RESOLUTION image with all the lovely stacks you might care to give it.
It can take any number of stacks (in a list) and the shape of the final output table.

Part 3:
Unsharp.py (see part 0)
Stack_Functions.py (see part 2)
Main.py
OK, normally I don't bother explaining the main function because all it does is load
stuff and then call the functions in the other files. But this time the main function
actually does something so I figure I should describe it.
Oh, by the way, I forgot to mention this earlier but I've been converting all my images
to 0 to 1 space, so that's all the mess at the top. Anyway, This lovely code can take
in a mask image as well (but you have to comment and uncomment some stuff). Otherwise
it creates a simple left-right mask, and gets a Gaussian stack of the mask. Next we
also create Laplacian stacks of image 1 and image 2. We then apply the Gaussian mask
stack to each of the Laplacian stacks, reversing the sign for the second one. Finally
we combine the left and right filtered halves into a combined stack.
The next few lines are just formatting to get it into the right shape for save stacks.
Last but certainly not least, we also combine the composites using this composite
function (oh sorry, I forgot to mention I added this to the stack functions).
Composite gets the lowest frequencies that were not captured in the stack (you know,
depending on how big the picture was and how many levels were requested) and adds
them back into the sum of the Laplacian stack.
The result is beautiful. :)

Ok, I hope you enjoyed this tour as much as I did! Have a nice day!
