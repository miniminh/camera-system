import os
import time
from datetime import datetime, timedelta

from utils import save_dir

SAVE_TIME = 60 # minutes

def timeout(filedate):
    now = datetime.now() - timedelta(0, 10 * 60)
    return now > filedate


def loop_all():
    for root, dirs, files in os.walk(save_dir):
        for file in files:
            f = os.path.join(root, file)
            print(file)
            time_start = file.find('_')
            date_object = datetime.strptime(file[time_start + 1:-15], "%d_%m_%Y_%H_%M_%S")
            if timeout(date_object):
                os.remove(f)

if __name__ == '__main__':
    while True:
        print("looping through all files")
        loop_all()
        print("sleeping")
        time.sleep(10)