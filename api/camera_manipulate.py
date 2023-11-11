import os
import time

upload_dir = 'uploads/'

def get_gender():
    with open('camera/camera.txt', 'r') as f:
        gender = f.read()
    return gender

def get_cam():
    
    while True:
        gender = get_gender()
        for root, dirs, files in os.walk(upload_dir + gender + '/'):
            tmp_gender = get_gender()
            if (tmp_gender != gender):
                break
            for file in files:
                tmp_gender = get_gender()
                if (tmp_gender != gender):
                    break
                yield os.path.join(root, file)