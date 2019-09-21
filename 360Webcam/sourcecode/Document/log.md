# week 4
## Camera system in the general form
### (hongjian he)
A camera display system is introduced to show input from cameras and provide interface for audio input/processing and output configuration.

The camera subsystem can be divided into 2 classes at this point: data_receiver and configuration_reader.

1. data_receiver:

This class defines the behaviour of the program about how the program reads input from cameras.
It is also possible to further integrate the audio input into this class.



2. configuration_reader:

This class defines how the program behaves depending on different user input.
The user can fully control the program's behaviour by editing the configuration file 
instead of going through the coding.
The current configuration options include a spd-say enabler and the cameras
index selection.

We set a main function that utilises these two classes to display and stitch the
images from 2 webcam. Since we are going to use fisheye camera, the remaining
tasks may include adding a function to data_receiver class that read fisheye image
input, adding a function to data_receiver class that could undistort the
image from fisheye camera, and defining the corresponding configuration option
for user to control this process.

# week 5
## Camera switching system
### (hongjian he)
The output of this system is 3 video windows that show 2 webcam and the camera switched by embeded algorithm depending on the sound arrival direction.

To make this system work, the following packages are needed:

'''opencv3, numpy, pyaudio, pyusb'''


### audio configuration
Since we don't have audio input at this stage, the video only has image
stream.

### image processing configuration
This system export image from webcam, display them, and switch based on
audio direction from audio processing result.

There are about 0.5 sec lag in this current design. The image quality is 
acceptable for online conference.

### current issue
the result from DOA is not stable. We need a better algorithm for determining
the sound direction, as well as sound cancellation function.


# week 6

## Installing opencv3 in anaconda environment by building from opencv source
### (by Hongjian)
It is possible to integrate the opencv source code into anaconda environment by building opencv3 first and linking its .so to anaconda site-packages.

Follow the bash script to do it on Debian (install\_opencv3\_conda.sh in the installation method directory).

## Observation with program efficiency:
### (by hongjian)
It is found that the camera switching program is slow because i add a keyboard control function to control the camera switching process. 
Its speed can be significantly improved if we remove this part.


# Teaching break

## Real-time face detector demo
### (by hongjian he)

### How it works
Opencv is used to solve the real-time face detection problem. The pretrained cascade classifier method is used to detect the face region.

The program is able to find the segment windows for faces. And the program at this point make a rectangle around that area.

### Current issue
1. The face detector fails when against light. And it makes the program even slower. We could improve the efficiency by probably using deep neural network detector.
2. The cascade classifier sometimes give a wrong region of face.



# Week 7

## Fisheye webcam input issue (solved)
### (by Hongjian)

### How it works
Reconfigure the opencv video capture object according to the webcam information
returned by the function v4l2-ctl --list-formats-ext function in bash.

Set video format, frame aspect ratio, and frame rate.


# week 10

## solve the problem of sending OpenCV output to skype on PC
Since the plug-and-play way requires far more programming than the capability 
of our team, we are looking for some other methods to do it.

The proposed method is to send the OpenCV output through local network as an IP camera that is reachable by the PC, and there will be an IP camera adaptor to make the IP camera
as a virtual camera on PC such that it can be detected by skype.

We found that there is an abandoned Linux program called mjpg-streamer that is able to stream a local uvc-device on linux as an IP camera. However, we still need a way 
to make the OpenCV Python output as a local uvc virtual device that is detectable by this program.

To do it, we first utilise the v4l2loopback Linux Kernel module to claim a virtual device, finally we use Python v4l2 utility to write our image frame to that virtual device.

We found a lot of softwares that can make an IP camera as virtual webcam on PC including OBS studio (not works for pre-installed skype), discord, and Zoom (this part is done by Minh).

## make the face detection as a separate thread running in the background
This can solve the problem of video lagging with face detection. The problem is reduced to lagging of face detection only.

## test for DOA and combine it into face detection
I actually found that the Voice Activity Detection with DOA predicts a reasonably good result for speech direction prediction.
So the only problem is to make this program into thread such that the video stream is fast. And we did it.

## Interface design
The interface is designed in the way that we rely on both the location of faces and the direction of voice.
If direction of voice is detected, we zoom in to the closest face detected in that direction.






