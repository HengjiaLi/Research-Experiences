##################################################################
## library initialisation
##################################################################
import signal
import time
import threading
import cv2 as cv
import numpy as np
#from matplotlib import pyplot as plt
import subprocess
import time
import math
import sys, select
#import pcn
from flask import Flask, render_template, Response
import socket


#from mic_array import MicArray

##################################################################
# define my data receiver:
##################################################################
class data_receiver(object):
    '''this class defines the behaviour of the sensor receiver including camera and audio'''

    def __init__(self):
        ''' this function initiate the data_receiver class
        '''
        
        self.opencv_version=int(cv.__version__[0])

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

        # initiate the image receiver
        ## add all the camera capture into list
        self.cam_capture=cv.VideoCapture('/dev/video0')
        self.cam_capture.set(cv.CAP_PROP_FRAME_WIDTH,self.image_width)
        self.cam_capture.set(cv.CAP_PROP_FRAME_HEIGHT,self.image_height)
        self.cam_capture.set(cv.CAP_PROP_FOURCC,cv.VideoWriter.fourcc('M','J','P','G'))
        self.ret=None
        self.frame=None
        self.dewarping_frame=None
        self.faces=None
        self.face_detection_state=1
        self.winlist=None
        self.face_detection_thread=None

        print('data receiver initiated')

    def get_frame(self):
        self.ret,self.frame=self.cam_capture.read()
        frame=self.frame
    def display_frame(self):
        while 1:
            if self.ret:
                cv.imshow('cam',self.frame)
                cv.waitKey(10)

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


    def display_camera(self):
        '''display raw image from camera'''
        while self.cam_capture.isOpened():
            if self.face_detection_state:
                self.face_detection_state=0
                self.get_frame()
                self.draw_face()
                self.dewarp()
                self.face_detection_thread=threading.Thread(target=self.detect_face)
                self.face_detection_thread.start()

                cv.imshow('fisheye camera',self.frame)
                cv.imshow('dewarped frame',self.dewarping_frame)
                cv.waitKey(1)
            else:
                self.get_frame()
                self.draw_face()
                self.dewarp()
                cv.imshow('fisheye camera',self.frame)
                cv.imshow('dewarped frame',self.dewarping_frame)
                cv.waitKey(1)


    def detect_face(self):
#        print("In detect face")
        self.winlist=pcn.detect(self.frame)
        self.face_detection_state=1
    def draw_face(self):
        if self.winlist:
            self.frame=pcn.draw(self.frame,self.winlist)
        

#    def signal_handler(self,sig, num):
#        self.is_quit.set()
#        print('Quit')


class configuration_reader(object):
    '''
    This class define the behaviour of configuration importing by using a finit state machine
    '''
    def __init__(self,file_name):
        # given the configuration file, add the configuration to the object
        self.file_name=file_name
        self.state='idle'
        self.config_dict={}
        self.config_dict[self.state]=[]
        self.cameras_list=[]
        self.spdsay_config=None


    def config_extracter(self):
        # open the file
        config_file=open(self.file_name,'r')
        ## extract all the configurations in file
        for line in config_file:
            line=line.strip()
            # define the state, state transition behaviour and associate to config dict
            if line=='':
                continue
            elif len(line)>2 and line[0]=='<' and line[-1]=='>':
                # this is a configuration line
                if line[1:4]=='end':
                    # end a current state and transfer to idle state
                    self.state='idle'
                if line[1:6]=='start':
                    # add a state to configuration dict
                    self.state=line[7:-1]
                    self.config_dict[self.state]=[]
            else:
                # information line
                self.config_dict[self.state].append(line)
        # close a file
        config_file.close()

    def get_camera_index(self):
        ## loop through camera_index
        for config_line in self.config_dict['cameras_index']:
            config_buffer=config_line.split()
            for camera_ind in config_buffer:
                if camera_ind.isdigit():
                    self.cameras_list.append(int(camera_ind))
    def get_spdsay_config(self):
        config_line = self.config_dict['spdsay_config'][0]
        self.spdsay_config=int(config_line)





        
##################################################################
## Define the main & test function
##################################################################

 




##################################################################
## Ip camera behaviour
##################################################################
# define our web server app

def server_run(my_data):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0",5000))
    server_socket.listen(5)


    print("Your IP address is: ", socket.gethostbyname(socket.gethostname()))


#    client_socket, address = server_socket.accept()
    print("Server Waiting for client on port 5000")

    while 1:


#        print('in')
        client_socket, address = server_socket.accept()
        
#        ret,jpg=cv.imencode('.jpg', cv.resize(my_data.frame,(120,90)))
        my_data.get_frame()
        if my_data.ret:
            cv.imshow('cam',my_data.frame)
            cv.waitKey(1)
            ret,jpg=cv.imencode('.jpg', my_data.frame)

        #image.save("webcam.jpg")

            client_socket.sendall(jpg.tobytes())


#################################################################
# main function control
#################################################################
if __name__=="__main__":
    my_data=data_receiver()
#    T=threading.Thread(target=my_data.display_frame,daemon=True)
#    T.start()
    server_run(my_data)
