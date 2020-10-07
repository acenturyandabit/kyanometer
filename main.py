import cv2

source = cv2.VideoCapture("http://192.168.43.1:8083/video")

def localDisplay(frame, result):
    cv2.imshow("frame",frame)
    key=cv2.waitKey(1)
    pass

displayResult = localDisplay

isOK=True
while isOK:
    isOK, frame =  source.read()
    # do processing
    if isOK:
        displayResult(frame, result={})
