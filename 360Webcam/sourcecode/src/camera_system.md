# Coding template for camera system
The camera subsystem can be divided into 2 class: data_receiver and configuration_reader.

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