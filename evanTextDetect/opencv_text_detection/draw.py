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

    textIm = drawOn.copy()
    textcache = {}
    for(x,y,w,h) in boxes:

        
        startX = int(x*ratioWidth) # Gets starting x 
        startY = int(y*ratioHeight) # Gets starting y 
        endX = int((x+w)*ratioWidth) # Compute ending x 
        endY = int((y+h)*ratioHeight) # Compute ending y 
        boundary = 2

        # Remove potential error 
        if any(idx<boundary for idx in [startX,startY]) == False:
            text = drawOn[ startY - boundary:endY + boundary, startX - boundary:endX + boundary] 
            text = cv2.cvtColor(text.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            textRecongized = pytesseract.image_to_string(text)
            textcache[textRecongized] = [startX, startY, endX, endY]
            
            # draw the bounding box on the image


    for text in textcache:
        coords = textcache[text]
        drawOn = cv2.putText(drawOn, text, (coords[0],coords[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102,48,35), 2, cv2.LINE_AA) 
            # drawOn = cv2.putText(drawOn, textRecongized, (endX,endY+5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA) 
        cv2.rectangle(drawOn, (coords[0], coords[1]), (coords[2], coords[3]), color, width)
        

    # return orig


