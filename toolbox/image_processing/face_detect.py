""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture('time_lapse_2D.mov')

while (True):
	#Capture, frame by frame
	ret, frame = cap.read()
	#Operations on the frame
	#Making it gray
	gray = cv2. cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#Display the resulting frame
	cv2.imshow('frame', gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()