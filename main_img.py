from subprocess import call
import os


img_path = "images/lebron_james.jpg"
east_path = " --east frozen_east_text_detection.pb"
exe_string = "python text_detection.py" +  " -i " + img_path + east_path

print(exe_string)
os.system(exe_string)