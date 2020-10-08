import numpy as np
import cv2
import pytesseract

def drawPolygons(drawOn, polygons, ratioWidth, ratioHeight, color=(0, 0, 255), width=1):
    for polygon in polygons:
        pts = np.array(polygon, np.int32)
        pts = pts.reshape((-1, 1, 2))
        # draw the polygon
        cv2.polylines(drawOn, [pts], True, color, width)
import re, string
pattern = re.compile('[^\w\d\. ]+')

def drawBoxes(drawOn, boxes, ratioWidth, ratioHeight, color=(0, 255, 0), width=1):

    textIm = drawOn.copy()
    textcache = {}
    for box in boxes:
        (x,y,w,h)=box
        
        startX = int(x*ratioWidth) # Gets starting x 
        startY = int(y*ratioHeight) # Gets starting y 
        endX = int((x+w)*ratioWidth) # Compute ending x 
        endY = int((y+h)*ratioHeight) # Compute ending y 
        boundary = 2

        # Remove potential error 
        if any(idx<boundary for idx in [startX,startY]) == False:
            text = drawOn[ startY - boundary:endY + boundary, startX - boundary:endX + boundary] 
            fatText=text.copy()
            for i in range(3):
                fatText=np.append(fatText,text,1)
            #text = cv2.cvtColor(text.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            custom_config = r'--oem 3 --psm 6 outputbase digits'

            textRecongized = pytesseract.image_to_string(text, config=custom_config)
            # we will get multiple copies of recurring strings
            # take the longest, most common string, priority on length
            textRecongized=pattern.sub("",textRecongized) # nerf all weird characters
            textRecongized=textRecongized.lower()
            parts=textRecongized.split(" ")
            partVotes={}
            for p in parts:
                if p not in partVotes:
                    partVotes[p]=0
                partVotes[p] = partVotes[p] + 1
            # get the entries in the dictionary, sort them by occurence, then take the first part (the actual word)
            sortedPartVotes=list(partVotes.items())
            sortedPartVotes.sort(key=lambda i: i[1],reverse=True)
            if sortedPartVotes:
                textRecongized=sortedPartVotes[0][0]
                textcache[textRecongized] = [startX, startY, endX, endY]
            
            # draw the bounding box on the image


    for text in textcache:
        coords = textcache[text]
        drawOn = cv2.putText(drawOn, text, (coords[0],coords[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102,48,35), 2, cv2.LINE_AA) 
            # drawOn = cv2.putText(drawOn, textRecongized, (endX,endY+5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA) 
        cv2.rectangle(drawOn, (coords[0], coords[1]), (coords[2], coords[3]), color, width)
        

    # return orig


