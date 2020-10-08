import os
import pytesseract


img_path = "images/car_wash.png"
east_path = " --east frozen_east_text_detection.pb"
exe_string = "python text_detection.py" +  " -i " + img_path + east_path

print(exe_string)
os.system(exe_string)