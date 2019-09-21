#!/usr/bin/env python

import fcntl, sys, os
from v4l2 import *
from threading import Thread, Lock
import time
import numpy as np
import cv2


class Streamer(Thread):
    _frameRate = 30
    _fmt = V4L2_PIX_FMT_MJPEG
    _curFrame = None
    _running = False
    _mutex = Lock()
#    _width=1280
#    height=720
#    width=720

    def __init__(self, devName,width,height):
        print("Frame resolution: {} x {}".format(width,height))
        Thread.__init__(self)
        if not os.path.exists(devName):
            print("Warning: device does not exist",devName)
        self._device = open(devName, 'wb', 0)
        capability = v4l2_capability()
        print("Get capabilities result: ",(fcntl.ioctl(self._device, VIDIOC_QUERYCAP, capability)))
        print("Capabilities: ", hex(capability.capabilities))
        print("V4l2 driver: " , capability.driver)

        format = v4l2_format()
        format.type = V4L2_BUF_TYPE_VIDEO_OUTPUT
        format.fmt.pix.pixelformat = self._fmt
        format.fmt.pix.width = width
        format.fmt.pix.height = height
        format.fmt.pix.field = V4L2_FIELD_NONE
        format.fmt.pix.bytesperline = width * 2
        format.fmt.pix.sizeimage = width * height * 2
        format.fmt.pix.colorspace = V4L2_COLORSPACE_JPEG

        print("Set format result: " ,(fcntl.ioctl(self._device, VIDIOC_S_FMT, format)))
        self._curFrame = np.zeros((height, width, 3), dtype=np.uint8)

    def updateFrame(self, frame):
        self._mutex.acquire()
        self._curFrame = frame
        self._mutex.release()

    def start(self):
        print("Starting Streamer on " , self._device)
        self._running = True
        Thread.start(self)

    def stop(self):
        self._running = False
        self.join()

    def run(self):
        while self._running:
            self._mutex.acquire()
            self._device.write(self._curFrame)
            self._mutex.release()
