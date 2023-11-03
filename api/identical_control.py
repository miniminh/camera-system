import os
import time
from datetime import datetime, timedelta

from utils import save_dir

SAVE_TIME = 60 # minutes

def timeout(filedate):
    now = datetime.now() - timedelta(0, 60 * 60)
    return now > filedate


def loop_all():
    for root, dirs, files in os.walk(save_dir):
        for file in files:
            f = os.path.join(root, file)
            date_object = datetime.strptime(f[len(save_dir):-15], "%d_%m_%Y_%H_%M_%S")
            print(date_object)
            if timeout(date_object):
                os.remove(f)

if __name__ == '__main__':
    while True:
        print("looping through all files")
        loop_all()
        print("sleeping")
        time.sleep(10)