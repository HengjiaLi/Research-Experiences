# require opencv
#### lib initialisation
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from random import randrange
import argparse
import sys

'''
Stitching sample
================

Show how to use Stitcher API from python in a simple way to stitch panoramas
or scans.
'''


modes = (cv.Stitcher_PANORAMA, cv.Stitcher_SCANS)

#parser = argparse.ArgumentParser(description='Stitching sample.')
#parser.add_argument('--mode',
#    type = int, choices = modes, default = cv.Stitcher_PANORAMA,
#    help = 'Determines configuration of stitcher. The default is `PANORAMA` (%d), '
#         'mode suitable for creating photo panoramas. Option `SCANS` (%d) is suitable '
#         'for stitching materials under affine transformation, such as scans.' % modes)
#parser.add_argument('--output', default = 'result.jpg',
#    help = 'Resulting image. The default is `result.jpg`.')
#parser.add_argument('img', nargs='+', help = 'input images')
#args = parser.parse_args()
#for img_name in args.img:
#    img = cv.imread(img_name)
#    if img is None:
#        print("can't read image " + img_name)
#        sys.exit(-1)
#    imgs.append(img)

# read input images
imgs = []
print(modes)

# read images
im_name_list=['left.jpg','right.jpg']
images=[cv.imread(im_name) for im_name in im_name_list]

stitcher = cv.Stitcher.create()
status, pano = stitcher.stitch(images)

if status != cv.Stitcher_OK:
    print("Can't stitch images, error code = %d" % status)
    sys.exit(-1)

cv.imwrite("output.png", pano);
print("stitching completed successfully. %s saved!")
