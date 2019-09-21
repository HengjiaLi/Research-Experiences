This folder contains the algorithms for the image stacking project. This project aims to blend a stack of macro images into a high-resolution and 
all-in-focus EDOF image. The included function are written in MATLAB and they are:

- "Calibrate.m": calibrate the camera position and compute the transform matrix between images

- "IMG_stack.m": register and blend the target images

- "IMG_stack_GF.m": register and blend the target images by applying guided filtering approach.

- "FileNumChecker.m": a function that automatically monitor the number of scanned image, and will return images once there are an image stack captured

- "IMG_stack_GF_V2.m": a combination of "FileNumChecker.m" and "IMG_stack_GF.m". Therefore, the script can constantly detect the image stacks in the 
target folder, and then blend the images along with the scan. You can use the binary images in the folder "finished" for testing this function, and the 
blending results are in the result "folder".

- "Transparrent_IMG.m": combines the color images and the Black&White mask, to crop out the background for each image.

the other functions in the folder are sub-functions of the above.

The workflow of this experiment is :

1) take a set of image scan for the calibration dot patterns (see folder "2019_01_25" for an example), and then run "Calibrate.m" to obtain the transformation 
matrix between images
2) take image scans for the target sepecimen and run "IMG_stack_GF_V2.m" to blend the images.
2) optional: you can use "IMG_stack_GF.m" or "IMG_stack.m" to test and to blend a single set of images, for example images in "2019_01_25".
3) turn on back lights and then repeat step 2 to obtain image masks
4) run "Transparrent_IMG.m" to combine the color and mask images, and to obtain the PNG image with transparrent background.
5) feed the PNG images into 3D reconstruction software.


If there are further questions, please contact hengjiali0625@gmail.com or u5629478@anu.edu.au
