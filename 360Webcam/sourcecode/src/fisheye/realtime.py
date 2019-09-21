import cv2 as cv
import pcn
import numpy as np
import time

#video capture
cap = cv.VideoCapture("/dev/video0")
cap.set(cv.CAP_PROP_FRAME_HEIGHT,960)
cap.set(cv.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv.CAP_PROP_FOURCC,cv.VideoWriter.fourcc('M','J','P','G'))

#set donut params
image_width=1280;image_height=960;
cx=image_width/2;cy=image_height/2;
R1=100;R2=cy;

output_width=int(2.0*((R2+R1)/2)*np.pi)
output_height=int(R2-R1)

# build the mapping
def build_map(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy):
    map_x = np.zeros((Hd,Wd),np.float32)
    map_y = np.zeros((Hd,Wd),np.float32)
    for y in range(0,int(Hd-1)):
        for x in range(0,int(Wd-1)):
            r = (float(y)/float(Hd))*(R2-R1)+R1
            theta = (float(x)/float(Wd))*2.0*np.pi
            xS = Cx+r*np.sin(theta)
            yS = Cy+r*np.cos(theta)
            map_x.itemset((y,x),int(xS))
            map_y.itemset((y,x),int(yS))
        
    return map_x, map_y
# do the unwarping 
def unwarp(img,xmap,ymap):
    result = cv.remap(img,xmap,ymap,cv.INTER_LINEAR)
    return result

if __name__ == '__main__':
    # build unwarp map
    xmap,ymap=build_map(image_width,image_height,output_width,output_height,R1,R2,cx,cy)
    # network detection
    while cap.isOpened():
        ret, img = cap.read()
        winlist = pcn.detect(img)
        print(winlist)
        img = pcn.draw(img, winlist)
        cv.imshow('webcam image', img)
        cv.imshow('unwarping',unwarp(img,xmap,ymap))
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
