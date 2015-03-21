""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('/home/li/Documents/Softdes/toolboxes/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')
cap = cv2.VideoCapture(0)
while (True):
    #Capture, frame by frame
    ret, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
    for (x,y,w,h) in faces:
        frame[y:y+h, x:x+w,:] = cv2.dilate(frame[y:y+h, x:x+w, :], kernel)
        for face in frame:
            cv2.ellipse(frame, (((x+w)/2)+150, ((y+h)/2)+150), (75, 50),205,0,120, 0, 12)
            cv2.circle(frame, ((x+h+350)/2,(y+w)/2), 7, (255,255,255), 20)
            cv2.circle(frame, ((x+h+150)/2,(y+w)/2), 7, (255,255,255), 20)
            cv2.circle(frame, ((x+h+350)/2,(y+w+10)/2), 1, (0,0,0), 13)
            cv2.circle(frame, ((x+h+150)/2,(y+w+10)/2), 1, (0,0,0), 13)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()