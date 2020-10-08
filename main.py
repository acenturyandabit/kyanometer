import cv2
import asyncio


source = cv2.VideoCapture("http://192.168.43.1:8083/video")


isOK=True
while isOK:
    isOK, frame = source.read()
    # do processing
    if isOK:
        cv2.imshow("frame",frame)
        key=cv2.waitKey(1)
        pass

