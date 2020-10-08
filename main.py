import cv2
import asyncio



#### dummy image to barcode for now
##import img2barcode
class _img2barcode:
    def getBarcode(frame):
        return None
img2barcode = _img2barcode()
#### end dummy image 2 barcode


source = cv2.VideoCapture("http://192.168.43.1:8083/video")
isOK=True
while isOK:
    isOK, frame = source.read()
    # do processing
    if isOK:

        priceCandidates = priceDetector.getPriceCandidates()
        ## should be [price,x,y]

        cv2.imshow("frame",frame)
        key=cv2.waitKey(1)
        pass

