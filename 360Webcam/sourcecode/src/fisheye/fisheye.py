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
import sys, select, termios, tty
import pcn
from flask import Flask, render_template, Response
#from mic_array import MicArray

##################################################################
# define my data receiver:
##################################################################
class data_receiver(object):
    '''this class defines the behaviour of the sensor receiver including camera and audio'''

    def __init__(self):
        ''' this function initiate the data_receiver class
        '''
        ## initiate tty receiver
        self.settings = termios.tcgetattr(sys.stdin)
        
        self.rlist=None
        self.key=None
        tty.setraw(sys.stdin.fileno())
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
        


    def get_key(self):
        '''call this function to get key from terminal'''
        self.rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if self.rlist:
            self.key = sys.stdin.read(1)
        else:
            self.key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
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
def main():
    ## data, configuration and controller initiation
    
    my_config = configuration_reader('../../configuration/camera_configuration')
    my_config.config_extracter()
    my_config.get_camera_index()
#    my_data = data_receiver(my_config.cameras_list)
    my_config.get_spdsay_config()


    while 1:
        ## get terminal input
        my_data.get_key()
        key=my_data.key
        # read camera input
        my_data.get_frames()
        my_data.detect_face()
        # show the cameras and stitched images
        for ind,cam_ret in enumerate(my_data.cam_ret_list):
#            print("in ret list")
            if cam_ret:
                
#                cv.imshow('camera {}'.format(ind),my_data.frame_list[ind])
                print(type(my_data.face_frame_list[ind]))
                cv.imshow("Show camera {} with face detected".format(ind),my_data.face_frame_list[ind])
                cv.waitKey(2)
        # show stitched image
#        cv.imshow('The person who is talking',my_data.frame_list[0])
#        cv.waitKey(2)

        ## determine based on input key
        if key=='k':
            print("k")
        elif my_data.key=='g':
            print(my_config.cameras)
        elif key=='q' or key==' ':
            break
        ## customised key
        elif key=='c':
            my_data.display_camera(my_config.cameras_list,my_config.spdsay_config)
            


def test():
    print("in test mode --------------")

#    my_config = configuration_reader('../configuration/camera_configuration')
#    my_config.config_extracter()
#    my_config.get_camera_index()
    my_data = data_receiver()
#    my_config.get_spdsay_config()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, my_data.settings)
    # set is_quit event
#    signal.signal(signal.SIGINT, my_data.signal_handler)
#    my_mic_array=MicArray(16000,4,16000/4)
#    my_mic_array.start()
    while 1:
        ## get terminal input
        my_data.get_key()
        key=my_data.key
        # get camera input
        my_data.get_frame()
        # imshow
        if my_data.ret:
            cv.imshow('Fisheye image',my_data.frame)
            cv.waitKey(1)

        ## determine based on input key

        # determine the chat camera based on sound direction

#        direction = my_mic_array.read_direction()
#        if direction<180:
#            cv.imshow('The person who is talking',my_data.frame_list[0])
#        else:
#            cv.imshow('The person who is talking',my_data.frame_list[1])
        if key=='k':
            direction = my_mic_array.read_direction()
            print(int(direction))
        elif key=='d':
            my_data.display_camera()
        elif my_data.key=='g':
            print(my_config.cameras)
        elif key=='q' or key==' ':
            break
        ## customised key
        elif key=='c':
            my_data.display_camera(my_config.cameras_list,my_config.spdsay_config)

#        # if quit
#        if my_data.is_quit.is_set():
#            break

def test0():
    print(cv.__version__)


 




##################################################################
## Ip camera behaviour
##################################################################


#################################################################
# main function control
#################################################################
if __name__=="__main__":
#    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, my_data.settings)
#    data=threading.Thread(target=my_data.display_camera,daemon=True)
#    data.start()
#    app.run('0.0.0.0', 5000,True)
    test()
