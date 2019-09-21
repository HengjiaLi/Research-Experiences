import cv2 as cv
import numpy as np
import tensorflow as tf

from utils import label_map_util
from utils import visualization_utils_color as vis_util

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = './model/frozen_inference_graph_face.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = './protos/face_label_map.pbtxt'

NUM_CLASSES = 2

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.image_height=960
        self.image_width=1280

        ## set fisheye camera params
        self.image_width=1280;self.image_height=960;
        self.cx=self.image_width/2;self.cy=self.image_height/2;
        self.R1=100;
        self.R2=self.cy
        self.map_x=None
        self.map_y=None

        self.output_width=int(2.0*((self.R2+self.R1)/2)*np.pi)
        self.output_height=int(self.R2-self.R1)
        self.build_map(self.image_width,self.image_height,self.output_width,self.output_height,self.R1,self.R2,self.cx,self.cy)

        self.video = cv.VideoCapture(0)
        self.video.set(cv.CAP_PROP_FRAME_HEIGHT,self.image_height)
        self.video.set(cv.CAP_PROP_FRAME_WIDTH,self.image_width)
        self.video.set(cv.CAP_PROP_FOURCC,cv.VideoWriter.fourcc('M','J','P','G'))
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        self.tDetector = TensoflowFaceDector(PATH_TO_CKPT)
    
    def __del__(self):
        self.video.release()
    def build_map(self,Ws,Hs,Wd,Hd,R1,R2,Cx,Cy):
        self.map_x = np.zeros((Hd,Wd),np.float32)
        self.map_y = np.zeros((Hd,Wd),np.float32)
        for y in range(0,int(Hd-1)):
            for x in range(0,int(Wd-1)):
                r = (float(y)/float(Hd))*(R2-R1)+R1
                theta = (float(x)/float(Wd))*2.0*np.pi
                xS = Cx+r*np.sin(theta)
                yS = Cy+r*np.cos(theta)
                self.map_x.itemset((y,x),int(xS))
                self.map_y.itemset((y,x),int(yS))
    def dewarp(self):
        self.dewarping_frame=cv.remap(self.frame,self.map_x,self.map_y,cv.INTER_LINEAR)
    
    def get_frame(self):
        success, image = self.video.read()
        img = cv.remap(image,self.map_x,self.map_y,cv.INTER_LINEAR)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        # face detection
        (boxes, scores, classes, num_detections) = tDetector.run(img)
        vis_util.visualize_boxes_and_labels_on_image_array(img,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=4)
        ret, jpeg = cv.imencode('.jpg', img)
        return jpeg.tobytes()
