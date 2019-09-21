This function implements the real-time Face Detection algorithm, through a inbuilt Wecam.
It simply utizes a built-in Cascade (the XML filte) that contains OpenCV data used to detect faces. 
No obvious lag observed yet and the source code is commented.

Prerequisites:
Python 3.6.6
OpenCV version 3.4.2
available webcam

How to use:
1. cd to the corresponding directory
2. simply run "python FaceDetection.py" in cmd
3. wait for about 10sec to activate the webcam and initialize the functions
4. press "q" to quit when it finishes.

Outputs: x,y,w,h (see line 22 of "FaceDetection.py")
This algorithm marks the detected faces by a rectangular frame. x and y stands for the location, and
w, h stands for the weidth and height of the rectangle.

Author: Hengjia Li 18/04/2019