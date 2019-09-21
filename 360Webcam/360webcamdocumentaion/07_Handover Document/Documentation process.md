# Introduction

# Software

## Sound

#### Enabling SPI Interface on the Raspberry Pi


#### Installing drivers for Respeaker Array

![Mic array image](04_Design%20Source/design%20figures/Mic_array.png)

As the project is open source, drivers for the Respeaker Mic array were installed 
from the instructions given from [this website](https://github.com/respeaker/mic_array). 
Specifically, open source codes pixel_ring.py (note that this code does not work presently
because it is not for the mic array, it is for the USB mic array) and mic_array.py were downloaded.
The parameters of these codes were changed for use for the specific model of the Respeaker
4-Mic Array for Raspberry Pi. 

#### Understanding and selecting the appropriate open source code
Through review of the mic_array.py code, it was understood that the code reads 
4 channels raw audio from the Mic Array, and estimates the sound's DOA (Direction of Arrival). 

#### Initial testing (5/4)
The output of this code was found to be an integer ranging from 1-360 which is representative of the direction
of the sound (in degrees) with respect to the mic array. The output of this open source code was 
tested and found to be approximately 4.3 values per second, or 258 values per min. For initial tests 
conducted, the detection of DOA of sound was tested by clapping and making noise around the device at
varying angles and distances. According to these tests, the initial results have shown that the DOA is 
very sensitive and easily influenced by background noise. This was noted to have a possible effect for
rapid image switching when combined with the USB based cameras. 

#### Implementation of average filter for noise cancellation (12/4)
Initially, the mic array was very sensitive to minute sound inputs. This resulted in
most background noise causing the device to have an unstable output in terms of detecting 
the direction of arrival (DOA) of the incoming sound. 

In order to migitate this effect, both noise cancellation and the averaging output were 
implemented. The mic array is capable of outputting 4.3 values per second with respect 
to the direction of sound. As such, Noise cancellation was realised by grouping every 8 values, 
deleting the outliers, and then taking the average of this given output. As a result, the
output for the DoA of sound is more stable and consistent. This will be useful in assisting the 
Image team for more consistent image switching for the camera with respect to detection of sound. 

#### Improving the response rate of the DOA algorithm (19/4)
As mentioned previously, 4 outliers were removed for every 8 values and then the average was taken to give 
the direction of the sound. For instance, if 8 values were given as [1 2 30 30 30 30 200 210], the four outliers 
would be ignored, and the average would be taken as 30, indicating a direction of 30 degrees relative to the mic array.
The code would then proceed to output the next 8 values, and so on. After testing, this result has shown to be not very accurate.
Additionally, there a delay was observed because of grouping 8 values together at a time. 

In order to improve the response rate of the DOA algorithm, a new method was implemented. The code would still detect
8 values at a time, though in an overlapping manner. For example, if the first group of values were [a b c d e f g h], 
then the next group would delete the first value, and append the next value, giving: [b c d e f g h i], and so on. This
function operates in the same manner as the previous one, although with this slight change, and it is designed to loop indefinitely. 

Additionally, according to meeting minutes 12/4/19, Gaussian weighting was found to be ineffective. 

#### Comparing/testing the Tyless USB microphone and Respeaker 4-Mic Array (25/4)
Initially, the team had intended for the Mic Array to be used to determine the sound DoA, while the USB microphone would be used for 
audio input. Recently, however, the sound team has discovered that the Mic array can also be used to record audio input. As such, both
devices were tested to determine whether the Mic Array could be used for both sound DoA and sound input. 

In order to do this, sound was recorded for 10 seconds for each device. It was found that the USB microphone operates with slightly higher sound
quality - this is perhaps due to the device's built-in noise cancellation hardware. The Mic array was found to be a feasible option for sound capture although 
with reduced sound quality. The team was therefore presented with a trade-off: if the Mic-array is used for both sound DoA and capture, the
amount of USB ports used will be reduced alongside the required costs and size of the device due to the USB microphone not being used. Of course, 
this would come at the cost of reduced sound quality. 

#### Improving noise cancellation (25/4)
Initially, noise cancellation was implemented by grouping every 8 values, deleting the outliers, and then taking the average of the given output. As a result, the
output for the DoA of sound would be more stable and consistent (as mentioned in documentation for 12/4).

For the second version, The code would still detect 8 values at a time, though in an overlapping manner. For example, if the first group of values were [a b c d e f g h], 
then the next group would delete the first value, and append the next value, giving: [b c d e f g h i], and so on (as mentioned in documentation for 19/4).

For the improvement of this version, a threshold was given for the sound input. This was achieved by converting the initial continuous time signal of the sound to a discrete time
one through a built-in python package called pyaudio. After this, a noise gate was added which essentially will filter out the peak amplitude of a sound wave below a given threshold. 
When tested, this would eliminate unnecessary sound capture for background noise including random sound or chatter in the surrounding environment. When no one is speaking, the Mic array
would give a default direction value of 0. 



#### Configuration of pixel ring


## Video

### General camera system (5/4)

A camera display system is introduced to show input from 90 degrees cameras and provide interface for audio input/processing and output configuration.
The camera subsystem can be divided into 2 classes at this point: data_receiver and configuration_reader.

##### data_receiver:

This class defines the behaviour of the program about how the program reads input from cameras.
It is also possible to further integrate the audio input into this class.

##### configuration_reader:

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

### Camera switching system (12/4)

Utilising two 90 degrees webcam, a function was developed to switch the input accepted based on the direction of sounds based on preliminaries DOA algorithm.
The output of the video system is 3 video windows that show 2 webcams, the third window will display whichever webcam is in the direction the sound is coming from. 
To make this system work, the following packages are needed:
+ OpenCV3
+ Numpy
+ PyAudio
+ PyUSB


However, as we haven't configure the audio input with video input at this stage, the current output only display the image. There are approximately 0.5 second lag
between the change in sound direction and switch video source. Despite the lag, the video quality from the two 90 degrees webcam are acceptable for online conference.
Another factor that affected the quality of output is the sensitivity of DOA algorithm, it is not stable currently and causes erratic switching. 

### Enhancing compability and efficiency (19/4)

#### Installing opencv3 in anaconda environment by building from opencv source
It is possible to integrate the opencv source code into the anaconda environment by building opencv3 first and linking its .so to anaconda site-packages.
Follow the bash script to do it on Debian (install_opencv3_conda.sh in the installation method directory). 

It is found that the current video processing algorithm is displaying latency due to the added keyboard control, the framerate of the output video increase significantly
when the function is removed. However, the team will retain this functionality for troubleshooting and manual control, the function will be removed in the final version. 

### Demonstrating and improving face dectection algorithm (26/4)

After researching face detection methodology, it is found that OpenCV contain a built-in face detection algorithm utilising the cascade classifier method.
This method has low computational requirement and can operates on the Raspberry Pi in conjunction with the camera. 
When the pretrained face detection algorithm isexecute, a rectangular window will appear around the face detected.

However, this method requires user to be staring directly at the camera for it to be effective. 
The face detection fails when bright lights are present behind the user, and utilisation of the algorithm causes latency in the program. 
The accuracy of face detection could be improve with the use of deep neural network detector, as the cascade classifier occasionally recognise background as faces. 

### Fisheye troubleshooting (3/5)

Reconfigure the opencv video capture object according to the webcam information
returned by the function v4l2-ctl --list-formats-ext function in bash.
Set video format, frame aspect ratio, and frame rate.

Creating a fisheye dewarp algorithm in Python 3, as the previous dewarping algorithm relies on simpleCV and exist on the Python 2 platform.
However, current Python platform utilise Python 3 and the OpenCV libraries, which is more comprehensive.

### Integrating rotational invariant face detection (10/5)

An open source algorithm is found that allow detection of face at all angles, and does not require the user to look directly at the camera. 
We are the first team that is utilising this algorithm with a fisheye camera as there are no existing publication, and it was an accidental discovery that the 
face detection algorithm work extremely well in conjunction with the fisheye camera. 

![Face detection](04_Design%20Source/design%20figures/Face_detection.png)

After testing the rotational invariant face detection and validating it using the fisheye camera, all the video processes and algorithm were combined into
one program. 

### Video streaming on user's PC(17/5)

The team attempt to implement a video stream similar to an IP camera system, however, it was found that OpenCV and the the use of an existing IP camera platform is not supported.
Therefore, the team needed to develop our own IP camera system, which capture frame-by-frame the video output from Raspberry Pi and upload it to an IP address on a local network.
However, the video stream is not recognisable by Skype as a source of video input.

This method also causes performance issue as instead of passing the video source directly to the PC, the Raspberry Pi must capture and send each frame separately.

### Inhouse IP camera system (24/5)

An incomplete and abandoned open source program relating to video streaming is found by one of the member. The team is able to utilise the incomplete codes and incorporate
it into the existing video processing program. The aim of the abandoned project was to stream MJPEG and allow the use of a video source, under MJPEG format, as an IP camera.

For the program to work as expected, the team devise a workaround through the creation of two virtual device for streaming/uploading and receiving/downloading videos from
the Raspberry Pi. OpenCV will create a virtual machine on the Raspberry Pi that is dedicated to uploading the video stream directly to a HTTP server, which is viewable through
an IP address. An application can then be installed on the user's PC that will create a second virtual device that will obtain the stream from the HTTP server, and create
a virtual webcam device on the user PC. This allow the video source from the Raspberry Pi to be recognised by Skype or other web conferencing services for video call. 


# Hardware


# Manufacturing and assembly

#### Initial design considerations
Based on the requirements outlined by the client, the device is required to be "Simple to build and operate".
Accordingly, the device required a housing unit to accommodate all the necessary hardware components. At this stage,
key design considerations included
- ease of access/removal of hardware components
- a design that can be 3D printed

#### Initial concept design
Based on the intial components being the 4 USB-based cameras, the Raspberry Pi and the Respeaker mic array, a rough concept
design was created so that the device could be visualised by the client. 

![Initial concept design](04_Design%20Source/design%20figures/4221_Concept_Design.PNG)

#### Concept design for Audit 1
Due to the previous design being purposed more for device visualisation and concept, another concept design was produced in line with more
practical design considerations for the first Audit:
- increasing height of device to keep USB cameras at an appropriate level for video calling
- holes/gaps to accomodate placement of component wires
- raised height of USB mic array to capture the DoA of sound more effectively 

The structure was therefore made much taller, and designed to consist of three "levels" atop a stand to house the microprocessor, USB cameras and 
mic array on separate levels. Notably, this design was created by John from the Sound sub-team, who extended his skills beyond the comfort zone of his \
engineering major and his signal processing background. 

![Concept design for Audit 1](04_Design%20Source/design%20figures/side_view.png)

#### Concept design for Audit 2
With the decision for the web conference device to utilise a wide view fish-eye lens camera instead of 4 USB cameras, 
the structure of the housing device would have to be completely redesigned. The addition of the USB microphone for sound
capture would also have to be considered. The preliminary design considerations for the device were thus as follows:

|       Function                |       Component    |       Dimensions        |
|   ---                         |       ---                     |       ---                 |      
|       Microprocessor          |   Raspberry Pi 3 Model B+            |   85.6mm x 56.5mm x 17mm |
|       Visual input            |   AHD digital video camera                    |  35.8mm x 35.8mm x35.5mm  |
|       Audio input             |   Respeaker 4-Mic Array for Raspberry Pi <br> Tyless 360 Conference USB microphone  | 65mm x 65mm x 9mm   <br>    D: 70mm H: 15mm  |
|       Other                   |  x        |    x

Accordingly, a three-level housing structure was proposed: 

![Concept design for Audit 2](04_Design%20Source/design%20figures/Side_view_1.PNG)

#### Drafting a modular design 
Due to the possibility of the 4-mic array being used for live sound capture instead of the USB microphone, the team was given the choice to create either a two-layer
or three-layer structure. In order to meet these two possibilities, modularity in the design was considered to allow these components to be added or removed as required
in the future. Notable changes from the previous design included the use of 3 pillars between levels to minimise sound interference, as well as a interlocking system in the
pillars for ease of access and removal of the internal hardware components. 

![Modular design](04_Design%20Source/design%20figures/Modular_design.JPG)

#### Final modular design frame 
After drafting the previous  modular design, the Assembly team translated the initial concept designs from Google sketchup on 
to Solidworks so that the device casing could be 3D printed. Slight adjustments were made to the design as the middle piece (see bottom left)
would not be able to be 3D printed due to the overhang which was not considered previously. Instead of 3 unique parts to print, 2 parts 
(a top and bottom part) would be used to allow for modularity between a 2 level or 3 level design. 

![Final modular design frame](04_Design%20Source/design%20figures/3D_Model.PNG)

#### Printed design frame 
The design was successfully 3D printed and used to house the components.

![Assembly](04_Design%20Source/design%20figures/Design.png)

#### Potential adjustments to modular design frame
It was found that the Raspberry Pi may overheat when used for extended periods of time due to requiring significant
processing power. Potential adjustments to the modular design frame were made to allow for more air flow and cooling of the device. 

![Comparison](04_Design Source/design figures/Grates_elevation_comparison.PNG)
