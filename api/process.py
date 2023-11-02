import cv2
from collections import defaultdict
import time

from object_detection import track, check_pass, save
from utils import IM_H, IM_W, log, csv_file

video_path = 0
video_path = "X:/ANHTAI/camera_system/test_case/test_case.mp4"
# video_path = "http://admin:admin@192.168.:8081/video"
# video_path = "one_person.webm"
# video_path = "X:/ANHTAI/camera_system/test_case/street.mp4"
# video_path = "http://192.168.89.112:14204/video"
cap = cv2.VideoCapture(video_path)

def process_video(cap):
    try:
        track_history = defaultdict(lambda: [])
        
        cnt_in = 0
        cnt_out = 0
        
        while cap.isOpened():
            success, frame = cap.read()
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
                            print(f"someone pass, id: {track_id}")
                            
                            exist, age, gender = save(box, frame)
                            
                            if not exist:
                                if is_in:
                                    cnt_in += 1
                                else:
                                    cnt_out += 1
                                # print(age, gender)
                                log(age, gender, is_in)
                            track_history[track_id].clear()
                                
                    cv2.putText(annotated_frame, f'{cnt_in}, {cnt_out}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
                    cv2.imshow("test", annotated_frame)
                else:
                    cv2.putText(frame, f'{cnt_in}, {cnt_out}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
                    cv2.imshow("test", frame)
            end = time.time()
            print(f'time_elapse: {end - start}')
            if cv2.waitKey(25) & 0xFF == ord('q'): 
                break
    except KeyboardInterrupt: 
        print("exiting")
        cap.release()
        cv2.destroyAllWindows()


process_video(cap)