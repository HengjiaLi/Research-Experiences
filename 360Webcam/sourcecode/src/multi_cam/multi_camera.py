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
#from mic_array import MicArray

##################################################################
# define my data receiver:
##################################################################
class data_receiver(object):
    '''this class defines the behaviour of the sensor receiver including camera and audio'''

    def __init__(self,camera_ind_list):
        ''' this function initiate the data_receiver class
        '''
        ## initiate tty receiver
        self.settings = termios.tcgetattr(sys.stdin)
        
        self.rlist=None
        self.key=None
        tty.setraw(sys.stdin.fileno())
        self.opencv_version=int(cv.__version__[0])

        # initiate the image receiver
        ## add all the camera capture into list
        self.camera_ind_list=camera_ind_list
        self.camera_list=[]
        self.frame_list=[]
        self.cam_ret_list=[]
        self.face_frame_list=[]
        self.ret=None
        self.frame=None
        for ind in camera_ind_list:
            self.camera_list.append(cv.VideoCapture(ind))
            self.frame_list.append(0)
            self.cam_ret_list.append(0)
            self.face_frame_list.append(0)

        ## add face detector init
        self.face_cascade = cv.CascadeClassifier('face_detector.xml')
#        self.face_cascade.load('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')

        ## add quit vonfig
#        self.is_quit = threading.Event()
        # add stitcher
#        self.stitcher = cv.Stitcher.create()
#        self.stitched_image=None
#        self.stitch_status=None
        print('data receiver initiated')

    def stitch(self):
        if self.opencv_version>=4:
            self.stitch_status, self.stitched_image=self.stitcher.stitch(self.frame_list)
        else:
            pass

    def get_frames(self):
        '''
        get frames from cameras, store it to list
        '''
        for ind,cam in enumerate(self.camera_list):
            self.cam_ret_list[ind],self.frame_list[ind]=cam.read()
            self.face_frame_list[ind]=self.frame_list[ind]
        

    def display_camera(self,camera_ind_list,whether_spdsay):
        '''display raw image from camera'''
        print("show cameras {} as required".format(str(camera_ind_list)))
        if whether_spdsay:
            subprocess.call(['spd-say','show cameras{}'.format(str(camera_ind_list))])
#        fig=plt.figure()
        self.get_key()
        while self.key!='q':
            #try:
            self.get_key()
            for cam_ind in camera_ind_list:
                self.ret, self.frame =  self.camera_list[cam_ind].read()
                if self.ret:
                    cv.imshow('camera {}'.format(cam_ind),self.frame)
                    cv.waitKey(10)
        cv.destroyAllWindows()

    def detect_face(self):
        if type(self.frame_list[0])!=int:
            for ind,cam_frame in enumerate(self.frame_list):
                faces= self.face_cascade.detectMultiScale(cv.cvtColor(cam_frame, cv.COLOR_BGR2GRAY),scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))

                for (x, y, w, h) in faces:
                    cv.rectangle(self.face_frame_list[ind], (x, y), (x+w, y+h), (0, 255, 0), 2)



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
    
    my_config = configuration_reader('../configuration/camera_configuration')
    my_config.config_extracter()
    my_config.get_camera_index()
    my_data = data_receiver(my_config.cameras_list)
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

    my_config = configuration_reader('../configuration/camera_configuration')
    my_config.config_extracter()
    my_config.get_camera_index()
    my_data = data_receiver(my_config.cameras_list)
    my_config.get_spdsay_config()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, my_data.settings)
    # set is_quit event
#    signal.signal(signal.SIGINT, my_data.signal_handler)
    my_mic_array=MicArray(16000,4,16000/4)
    my_mic_array.start()
    while 1:
        ## get terminal input
        my_data.get_key()
        key=my_data.key
        # get camera input
        my_data.get_frames()
        my_data.detect_face()
        # show the cameras and stitched images
        for ind,cam_ind in enumerate(my_data.camera_ind_list):
            if my_data.cam_ret_list[ind]:
#                print("Show camera {}".format(cam_ind))
                cv.imshow('camera {}'.format(cam_ind),my_data.frame_list[ind])
#                cv.imshow("Show camera {} with face detected".format(ind),my_data.face_frame_list[ind])
                cv.waitKey(3)
        # show stitched image
#        my_data.stitch()
#        if my_data.stitch_status != cv.Stitcher_OK:
#               print("Can't stitch images!")
#        else:
#            cv.imwrite("camera.png", my_data.stitched_image)
#            cv.imshow('Stitched image',my_data.stitched_image)

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
## main function control
##################################################################
if __name__=="__main__":
    main()
