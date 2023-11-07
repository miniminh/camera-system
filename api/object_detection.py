from ultralytics import YOLO
import numpy as np

from utils import THRESHOLD1, THRESHOLD2, save_dir, generate_temp_filename
from age_gender import predict, get_feature

model = YOLO('yolov8n.pt')

def track(frame):
    results = model.track(frame, persist=True, verbose=False, classes=0)
    if results[0].boxes.id == None: 
        return None
    return results

def check_pass(box, track_id, track_history):
    x, y, w, h = box
    track = track_history[track_id]
    track.append((float(x), float(y)))  # x, y center point
    if len(track) > 30:  # retain 90 tracks for 90 frames
        track.pop(0)
    if (track[0][0] > THRESHOLD2 and track[-1][0] < THRESHOLD1):
        return True, False
    if (track[0][0] < THRESHOLD1 and track[-1][0] > THRESHOLD2):
        return True, True
    return False, False
            
def save(box, frame, is_in):
    x, y, w, h = box
    X1 = int(x) - (int(w) // 2)
    X2 = int(x) + (int(w) // 2)
    Y1 = int(y) - (int(h) // 2)
    Y2 = int(y) + (int(h) // 2)
    
    crop_frame = frame[Y1:Y2, X1:X2]
    
    feature = get_feature(crop_frame)
    if is_in: 
        id, filename = generate_temp_filename()
        filename = save_dir + filename
        np.save(filename, feature)
        age, gender = predict(feature)
        return id, age, gender, feature
    else:
        return None, None, None, feature