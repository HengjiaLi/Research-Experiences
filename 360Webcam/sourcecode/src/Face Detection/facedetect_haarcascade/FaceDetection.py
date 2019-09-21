import cv2

# read in the pre-trained cascade for face detection
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# grab the reference to the default webcam
vs = cv2.VideoCapture(0)

# keep looping
while True:
	# grab the current frame from the webcam
	ret, frame = vs.read()
  
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	# if it is Webcam, it will never stop
	if frame is None:
		break
	# run face detection
	faces = faceCascade.detectMultiScale(frame)
	# highlight the region of detected faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
	# show the frame to our screen
	cv2.imshow("Video", frame[:,:,:])
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# close all windows
cv2.destroyAllWindows()