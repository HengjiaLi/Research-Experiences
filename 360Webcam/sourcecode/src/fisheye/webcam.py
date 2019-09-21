import cv2

import pcn
cap = cv2.VideoCapture("/dev/video0")
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,960)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter.fourcc('M','J','P','G'))


if __name__ == '__main__':
    # network detection
    while cap.isOpened():
        ret, img = cap.read()
        winlist = pcn.detect(img)
#        print(winlist)
        img = pcn.draw(img, winlist)
        cv2.imshow('PCN', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
