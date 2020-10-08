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
    image =image.copy()
    # Find barcodes in image (QR/CODE128) and decode each
    barcodes = pyzbar.decode(image)

    # Initialise Lists to hold data
    Data_List = list()
    Type_List = list()

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

        # Append data to lists
        Data_List.append(barcodeData)
        Type_List.append(barcodeType)
        
        # Store barcode data in string
        text = "{} ({})".format(barcodeData, barcodeType)
        # Write barcode data back onto image
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 2)

    # Display output image
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    if len(Data_List):
        return (Data_List[0],image)
    else:
        return (None,image)


# Main Function
if __name__ == '__main__':

    image = cv2.imread(r"tests\test1.jpg")
    Out_Tuple = Barcode_Detect(image)
    
    print(Out_Tuple)