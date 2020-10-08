# USAGE
# opencv-text-detection --image images/lebron_james.jpg

# import the necessary packages
import argparse
import os
import time

import cv2
from nms import nms
import numpy as np

from opencv_text_detection import utils
from opencv_text_detection.decode import decode
from opencv_text_detection.draw import drawPolygons, drawBoxes




def segmented_text_detection(image,chunkW=128, chunkH=128, **kwargs):
    default_text_args={
        "east":"frozen_east_text_detection.pb",
        "min_confidence":0.5
    }
    for key,value in kwargs.items():
        default_text_args[key]=value
    maxX=int(np.ceil(image.shape[0]/chunkW))
    maxY=int(np.ceil(image.shape[1]/chunkH))
    for dX in range(maxX):
        for dY in range(maxY):
            text_detection(image[dX*chunkW:dX*chunkW+chunkW,dY*chunkH:dY*chunkH+chunkH,:],default_text_args['east'],default_text_args['min_confidence'],chunkW,chunkH)


def fetchTextCoords(img, candidates):
    results=[]
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
            results.append((textRecongized,(x,y,w,h)))
    return results


def text_detection(image, east, min_confidence, width, height):
    # load the input image and grab the image dimensions
    # image = cv2.imread(image)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    orig = image.copy()
    (origHeight, origWidth) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    ratioWidth = origWidth / float(newW)
    ratioHeight = origHeight / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (imageHeight, imageWidth) = image.shape[:2]

    cv2.imshow("resized",image)

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    # print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)


    # calculate the mean of RGB values
    imshape = image.shape
    flattenedImageChannels=image.reshape((imshape[0]*imshape[1],3))
    means = np.mean(flattenedImageChannels)
    print (means)
    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets

    blob = cv2.dnn.blobFromImage(image, 1.0, (imageWidth, imageHeight), means, swapRB=True, crop=False)
    print (type(blob))
    print (blob.shape)
    print (image.shape)
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()

    # show timing information on text prediction
    # print("[INFO] text detection took {:.6f} seconds".format(end - start))


    # NMS on the the unrotated rects
    confidenceThreshold = min_confidence
    nmsThreshold = 0.4

    # decode the blob info
    (rects, confidences, baggage) = decode(scores, geometry, confidenceThreshold)

    offsets = []
    thetas = []
    for b in baggage:
        offsets.append(b['offset'])
        thetas.append(b['angle'])

    ##########################################################

    # functions = [nms.felzenszwalb.nms, nms.fast.nms, nms.malisiewicz.nms]
    functions = [nms.felzenszwalb.nms]

    # print("[INFO] Running nms.boxes . . .")

    for i, function in enumerate(functions):

        start = time.time()
        indicies = nms.boxes(rects, confidences, nms_function=function, confidence_threshold=confidenceThreshold,
                                 nsm_threshold=nmsThreshold)
        end = time.time()

        indicies = np.array(indicies).reshape(-1)
        if indicies.size != 0: 
            drawrects = np.array(rects)[indicies]

            name = function.__module__.split('.')[-1].title()
            # print("[INFO] {} NMS took {:.6f} seconds and found {} boxes".format(name, end - start, len(drawrects)))

            drawOn = orig.copy()
            # create a CLAHE object (Arguments are optional).
            # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            # grayed = cv2.cvtColor(drawOn.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            # drawOn = clahe.apply(grayed)
            
            drawBoxes(drawOn, drawrects, ratioWidth, ratioHeight, (0, 255, 0), 2)

            title = "nms.boxes {}".format(name)

            # imText = cv2.rotate(imText, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow(title,drawOn)
            # cv2.imshow("Text Detection", drawOn)

        else:
            name = function.__module__.split('.')[-1].title()
            drawOn = orig.copy()
            title = "nms.boxes {}".format(name)
            # drawOn = cv2.rotate(drawOn, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow(title,drawOn)


    cv2.waitKey(1)


    # # convert rects to polys
    # polygons = utils.rects2polys(rects, thetas, offsets, ratioWidth, ratioHeight)

    # print("[INFO] Running nms.polygons . . .")

    # for i, function in enumerate(functions):

    #     start = time.time()
    #     indicies = nms.polygons(polygons, confidences, nms_function=function, confidence_threshold=confidenceThreshold,
    #                              nsm_threshold=nmsThreshold)
    #     end = time.time()

    #     indicies = np.array(indicies).reshape(-1)

    #     drawpolys = np.array(polygons)[indicies]

    #     name = function.__module__.split('.')[-1].title()

    #     print("[INFO] {} NMS took {:.6f} seconds and found {} boxes".format(name, end - start, len(drawpolys)))

    #     drawOn = orig.copy()
    #     drawPolygons(drawOn, drawpolys, ratioWidth, ratioHeight, (0, 255, 0), 2)

    #     title = "nms.polygons {}".format(name)
    #     drawOn = cv2.rotate(drawOn, cv2.ROTATE_90_CLOCKWISE)
    #     cv2.imshow(title,drawOn)
    #     cv2.moveWindow(title, 150+i*300, 150)

    # cv2.waitKey(1)


def text_detection_command():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", type=str,
        help="path to input image")
    ap.add_argument("-east", "--east", type=str, default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'frozen_east_text_detection.pb'),
        help="path to input EAST text detector")
    ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
        help="minimum probability required to inspect a region")
    ap.add_argument("-w", "--width", type=int, default=736,
        help="resized image width (should be multiple of 32)")
    ap.add_argument("-e", "--height", type=int, default=576,
        help="resized image height (should be multiple of 32)")
    args = vars(ap.parse_args())

    text_detection(image=args["image"], east=args["east"], min_confidence=args['min_confidence'], width=args["width"], height=args["height"], )


if __name__ == '__main__':
    text_detection_command()
