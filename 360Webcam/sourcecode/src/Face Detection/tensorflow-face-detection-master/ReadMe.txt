This function implements the real-time Face Detection algorithm, through a inbuilt Wecam.
It simply utizes a pre-trained CNN weights (frozen_inference_graph_face.pb in folder "model") that implements face detection on Tensorflow Object Detection API
No obvious lag observed yet and the source code is commented.

Comparing to the other algorithm using Open CV cascade, this fuction provides a better detecion of side-faces.

Prerequisites:
Python 3.6.6
OpenCV version 3.4.2
tensorflow;
available webcam

How to use:
1. cd to the corresponding directory
2. simply run "python inference_usbCam_face.py 0" in cmd to run camerID=0
3. wait for about 5 sec to activate the webcam and initialize the functions
4. press "q" to quit when it finishes.

Outputs: boxes (normalized [ymin,xmin,ymax,xmax]);

source: https://github.com/yeephycho/tensorflow-face-detection
Author: Hengjia Li 18/04/2019