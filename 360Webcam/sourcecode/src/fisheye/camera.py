import cv2 as cv
import numpy as np
import threading
import pcn

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

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

        self.cam_capturer = cv.VideoCapture(0)
        self.cam_capturer.set(cv.CAP_PROP_FRAME_HEIGHT,960)
        self.cam_capturer.set(cv.CAP_PROP_FRAME_WIDTH,1280)
        self.cam_capturer.set(cv.CAP_PROP_FOURCC,cv.VideoWriter.fourcc('M','J','P','G'))
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        self.ret=None
        self.frame=None
        self.dewarping_frame=None
        self.faces=None
        self.face_detection_state=1
        self.winlist=None
        self.face_detection_thread=None

        print('data receiver initiated')
    
    def __del__(self):
        self.cam_capturer.release()

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

    def get_raw_image(self):
        self.ret, self.frame= self.cam_capturer.read()

    def main(self):
        while self.frame!=None:
            self.winlist=pcn.detect(self.frame)
            print("Found face(s)")
    def draw_faces(self):
        if self.winlist:
            self.frame=pcn.draw(self.frame,self.winlist)
    
    def get_frame(self):
        self.get_raw_image()
        self.draw_faces()
        self.dewarp()
        image=self.dewarping_frame
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()
