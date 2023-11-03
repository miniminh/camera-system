import cv2
from collections import defaultdict
import time
import numpy as np

from object_detection import track, check_pass, save
from utils import IM_H, IM_W, log, csv_file, distance, video_path
from choose import make_choice


live_cap = cv2.VideoCapture(video_path)
camera = cv2.VideoCapture('X:/ANHTAI/camera_system/api/uploads/ezin.mp4', cv2.CAP_DSHOW)

track_history = defaultdict(lambda: [])
    
cnt_in = 0
cnt_out = 0

people = []

cnt_gender = dict.fromkeys(['m', 'f'])

cnt_gender['m'] = 0
cnt_gender['f'] = 0

CAMERA = 'male'

while live_cap.isOpened():
    success, frame = live_cap.read()
    if success:
        start = time.time()
        
        frame = cv2.resize(frame, (IM_W, IM_H))
        
        results = track(frame)
        
        if results:
            annotated_frame = results[0].plot()
            
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
                    
            for box, track_id in zip(boxes, track_ids):
                is_pass, is_in = check_pass(box, track_id, track_history)
                
                if is_pass: 
                    # if right to left is in 
                    is_in = not is_in
                    
                    age, gender, feature = save(box, frame, is_in)
                    
                    if is_in:
                        people.append([age, gender, feature])
                        cnt_gender[gender] += 1
                        cnt_in += 1
                        print(f"a {age} {gender} just went in")
                    elif cnt_in - cnt_out > 0:
                        temp = [] 
                        for person in people: 
                            temp.append(distance(person[-1], feature))
                            
                        out_person = np.argmin(temp)
                        cnt_gender[people[out_person][1]] += 1
                        print(f'a {people[out_person][0]} {people[out_person][1]} just went out')
                        people.pop(out_person)
                        cnt_out += 1
                    else:
                        print("how come there's more people coming out than in?")
                        
                    log(age, gender, is_in)
                    track_history[track_id].clear()
                    
                if len(people) != 0:
                    CAMERA = make_choice(cnt_gender)
                    with open('camera/camera.txt', 'w') as f:
                        f.write(CAMERA)
                else:
                    with open('camera/camera.txt', 'w') as f:
                        f.write('')
                        
            cv2.putText(annotated_frame, f'{cnt_in - cnt_out}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
            cv2.imshow("test", annotated_frame)
        else:
            cv2.putText(frame, f'{cnt_in - cnt_out}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
            cv2.imshow("test", frame)
    
    end = time.time()
    # print(f'time_elapse: {end - start}')
    if cv2.waitKey(25) & 0xFF == ord('q'): 
        break