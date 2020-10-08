### File Information
# Team: The Hardest Part
# SUMO Hackathon 2020
# Date: 08/10/2020
#
# Source: Code derived from work by Adrian Rosebrock
# https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/



# Imports
from pyzbar import pyzbar
import cv2

# Function Definition
def Barcode_Detect (image):

    # Find barcodes in image (QR/CODE128) and decode each
    barcodes = pyzbar.decode(image)

    # Iterate through each detected barcode
    for barcode in barcodes:

        # Extract location of bounding box containing barcode
        (x, y, w, h) = barcode.rect

        # Draw bounding box around barcode
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Set barcode data format and decode information
        barcodeData = barcode.data.decode("utf-8")
        # Identify type of barcode (QR or CODE128)
        barcodeType = barcode.type
        
        # Store barcode data in string
        text = "{} ({})".format(barcodeData, barcodeType)
        # Write barcode data back onto image
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 2)

        # Print decoded barcode information to terminal
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    # Display output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)