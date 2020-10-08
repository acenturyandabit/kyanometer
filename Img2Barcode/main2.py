from Barcode import Barcode_Detect
import cv2

# Main
if __name__ == '__main__':

    image = cv2.imread(r"test_images\test1.jpg")
    Barcode_Detect(image)