import numpy as np
import cv2
import pytesseract

def drawPolygons(drawOn, polygons, ratioWidth, ratioHeight, color=(0, 0, 255), width=1):
    for polygon in polygons:
        pts = np.array(polygon, np.int32)
        pts = pts.reshape((-1, 1, 2))
        # draw the polygon
        cv2.polylines(drawOn, [pts], True, color, width)


def drawBoxes(drawOn, boxes, ratioWidth, ratioHeight, color=(0, 255, 0), width=1):

    orig = drawOn
    for(x,y,w,h) in boxes:
        
        startX = int(x*ratioWidth)
        startY = int(y*ratioHeight)
        endX = int((x+w)*ratioWidth)
        endY = int((y+h)*ratioHeight)

        if any(idx<2 for idx in [startX,startY]) == False:
            boundary = 2
            text = drawOn[ startY - boundary:endY + boundary, startX - boundary:endX + boundary]
            text = cv2.cvtColor(text.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            textRecongized = pytesseract.image_to_string(text)
            drawOn = cv2.putText(drawOn, textRecongized, (endX,endY+5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA) 
            # draw the bounding box on the image

        cv2.rectangle(drawOn, (startX, startY), (endX, endY), color, width)

    # return orig


