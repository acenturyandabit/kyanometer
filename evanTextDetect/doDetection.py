from opencv_text_detection import text_detection as td


def doDetection(frame):
    frame  = cv2.resize(frame,(1024,928),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    frame  = td.text_detection(frame,
                               east=os.path.join(dir_path, 'opencv_text_detection/frozen_east_text_detection.pb'),
                               min_confidence=0.5, 
                               width=1024, 
                               height=928)
    return (frame,prices)