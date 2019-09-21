import numpy as np
import cv2

cap = cv2.VideoCapture("/dev/video0")
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,960)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter.fourcc('M','J','P','G'))
if not cap.isOpened:
    print("camera not open properly")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
#    print('frame got')
#    print(type(frame))

    # Our operations on the frame come here
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    if ret:

#        print(frame.__dict__)
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
