import random
import string
import numpy as np
import csv
from datetime import datetime

def generate_temp_filename():
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    filename = dt_string + '_' + random_string
    return filename

def distance(a, b):
    return np.linalg.norm(a - b)

def log(age, gender, is_in):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if gender == 0: 
        g = 'male'
    else:
        g = 'female'
    with open('X:/ANHTAI/camera_system/data/log.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([dt_string, age, g, is_in, not is_in])


csv_file = open('X:/ANHTAI/camera_system/data/log.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)
header = ['time', 'age', 'gender', 'in', 'out']
csv_writer.writerow(header)
csv_file.close()

save_dir = 'X:/ANHTAI/camera_system/save/'

THRESHOLD = 0.5

# IM_W = 1600
# IM_H = 1200

IM_W = 1920
IM_H = 1080

THRESHOLD1 = THRESHOLD * IM_W

THRESHOLD2 = THRESHOLD1 + 10

FACE_W = FACE_H = 198

checkpoint_path = 'X:/ANHTAI/camera_system/model_checkpoint'

max_age = 64

SIMILAR_THRESHOLD = 10

video_path = 0
video_path = "X:/ANHTAI/camera_system/test_case/test_case.mp4"