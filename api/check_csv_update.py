import os
import time

from fastapi import status
from fastapi.responses import RedirectResponse

cached_stamp = 0

def check_csv_update(csv_file):
    """Checks if a CSV file has been updated."""
    
    global cached_stamp
    
    last_modified = os.path.getmtime(csv_file)
    current_time = time.time()
    stamp = os.stat(csv_file).st_mtime
    if stamp != cached_stamp:
        cached_stamp = stamp
        return True
    else:
        return False

csv_file = 'X:\ANHTAI\camera_system\data\log.csv'

if __name__ == '__main__':
    while True:
        print("looking for change in log file")
        if (check_csv_update(csv_file)):
            print('kkk')
        print("sleeping")
        time.sleep(1)