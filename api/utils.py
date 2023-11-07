import random
import string
import numpy as np
import csv
from datetime import datetime

ID_COUNT = 0

def get_csv_headers(csv_file):
    """Returns a list of headers from a CSV file."""
    with open(csv_file, "r", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers

def get_csv_rows(csv_file):
    """Returns a list of rows from a CSV file."""
    rows = []
    with open(csv_file, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    rows = rows[1:]
    new_rows = [] 
    for i, row1 in enumerate(rows):
        for j, row2 in enumerate(rows):
            if i < j and row1[0] == row2[0]: 
                temp_row = row1[:-1]
                temp_row.append(row2[-1])
                new_rows.append(temp_row)

    for row in rows:
        ok = True
        for new_row in new_rows:
            if new_row[0] == row[0]:
                ok = False
                break
        if ok is True: 
            new_rows.append(row)
    print(new_rows)
    return new_rows

def generate_temp_filename():
    global ID_COUNT
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    filename = str(ID_COUNT) + '_' + dt_string + '_' + random_string
    ID_COUNT += 1
    return ID_COUNT - 1, filename

def distance(a, b):
    return np.linalg.norm(a - b)

def log(id, gender, age, is_in):
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    time_in = None
    time_out = None    
    if is_in: 
        time_in = dt_string
    else:
        time_out = dt_string
    
    with open('X:/ANHTAI/camera_system/data/log.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([id, gender, age, time_in, time_out])


csv_file = open('X:/ANHTAI/camera_system/data/log.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
header = ['id', 'gender', 'age', 'in', 'out']
csv_writer.writerow(header)
csv_file.close()

save_dir = 'X:/ANHTAI/camera_system/save/'

THRESHOLD = 0.5

# IM_W = 1600
# IM_H = 1200

# IM_W = 1920
# IM_H = 1080

IM_W = 720
IM_H = 480

THRESHOLD1 = THRESHOLD * IM_W

THRESHOLD2 = THRESHOLD1 + 10

FACE_W = FACE_H = 198

checkpoint_path = 'X:/ANHTAI/camera_system/model_checkpoint'

max_age = 64



SIMILAR_THRESHOLD = 10

video_path = 0
# video_path = "X:/ANHTAI/camera_system/test_case/street.mp4"
# video_path = "http://admin:admin@192.168.88.235:8081/video"