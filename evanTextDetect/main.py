import cv2
import numpy as np
import os
from opencv_text_detection import text_detection as td

dir_path = os.path.dirname(os.path.realpath(__file__))
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(os.path.join(dir_path,'Portrait_Powerbanks.mp4'))

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('X','V','I','D'), 10, (928,1024))
nframes=80
while(cap.isOpened()) and nframes>0:
  nframes=nframes-1
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    frame  = cv2.resize(frame,(1024,928),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    frame  = td.text_detection_alt(frame,
                               east=os.path.join(dir_path, 'opencv_text_detection/frozen_east_text_detection.pb'),
                               min_confidence=0.5, 
                               width=1024, 
                               height=928)
    # 
    # Display the resulting frame
    cv2.imshow('Frame',frame)
    print (frame.shape)
    out.write(frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  # Break the loop
  else: 
    break
  print ("frame")

# When everything done, release the video capture object
cap.release()
out.release()
# Closes all the frames
cv2.destroyAllWindows()