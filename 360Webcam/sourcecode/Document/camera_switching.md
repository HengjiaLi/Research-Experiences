# Camera switching system
## Time of completion: week5
The output of this system is 3 video windows that show 2 webcam and the camera switched by embeded algorithm depending on the sound arrival direction.

To make this system work, the following packages are needed:

'''opencv3, numpy, pyaudio, pyusb'''


## audio configuration
Since we don't have audio input at this stage, the video only has image
stream.

## image processing configuration
This system export image from webcam, display them, and switch based on
audio direction from audio processing result.

There are about 0.5 sec lag in this current design. The image quality is 
acceptable for online conference.

## current issue
the result from DOA is not stable. We need a better algorithm for determining
the sound direction, as well as sound cancellation function.

