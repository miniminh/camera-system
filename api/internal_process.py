import cv2
from collections import defaultdict
import time
import numpy as np
import torch

from object_detection import track, check_pass, save
from utils import IM_H, IM_W, log, csv_file, distance, video_path, ONLY_ALLOW_ONCE, SIMILAR_THRESHOLD
from choose import make_choice
from age_gender import get_id, check_was_in


live_cap = cv2.VideoCapture(video_path)
camera = cv2.VideoCapture('uploads/ezin.mp4', cv2.CAP_DSHOW)

track_history = defaultdict(lambda: [])
    
cnt_in = 0
cnt_out = 0

people = []

cnt_gender = dict.fromkeys(['m', 'f'])

cnt_gender['m'] = 0
cnt_gender['f'] = 0

CAMERA = 'male'

cnt = 0

while live_cap.isOpened():
    success, frame = live_cap.read()
    if success:
        cnt += 1
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
                    
                    track_history[track_id].clear()
                     
                    # if right to left is in 
                    # is_in = not is_in
                    
                    id, feature = save(box, frame, is_in)          
                    
                    if is_in:
                        if id == None: 
                            print('already in')
                            continue
                        people.append(feature)
                        cnt_in += 1
                        print(f"a person just went in")
                    elif cnt_in - cnt_out > 0:
                        temp = [] 
                        chosen = None
                        for person in people: 
                            similarity = torch.nn.functional.cosine_similarity(person, feature).item()
                            print(similarity)
                            if similarity > SIMILAR_THRESHOLD:
                                chosen = person
                                break
                        if chosen is None: 
                            print("i don't know who just went out")
                            continue
                        id = get_id(chosen)
                        print(f'a person just went out')
                        index = people.index(chosen)
                        people.pop(index)
                        cnt_out += 1
                    else:
                        print("how come there's more people coming out than in?")
                        continue
                    log(id, None, None, is_in)
                        
                    
                    
                    
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