import cv2

import phonesource

source = cv2.VideoCapture(0)
#source = phonesource.VideoCapture()
#source = cv2.VideoCapture("videosample.mp4")

def localDisplay(frame, result):
    cv2.imshow("frame",frame)

displayResult = localDisplay
#displayResult = phonesource.output

isOK=True
while isOK:
    isOK, frame = cam.read()
    if isOK:
        displayResult(frame, result={})