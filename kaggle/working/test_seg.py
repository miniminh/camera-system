from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train/weights/best.pt")

video_path = "/Users/dev/development/minhphan/camera-system/test_case/test_case.mp4"

live_cap = cv2.VideoCapture(video_path)

while live_cap.isOpened():
    success, frame = live_cap.read()
    if success:
        
        frame = cv2.resize(frame, (1920, 1080))
        
        results = model.predict(frame)
        
        if results:
            annotated_frame = results[0].plot()
            boxes = results[0].boxes.xywh.cpu()
            classes = results[0].boxes.cls.cpu()

            clothes = [] 
            for box, clothes_class in zip(boxes, classes):
                item_id = clothes_class.item()
                item_name = results[0].names[item_id]
                x, y, w, h = box
                X1 = int(x) - (int(w) // 2)
                X2 = int(x) + (int(w) // 2)
                Y1 = int(y) - (int(h) // 2)
                Y2 = int(y) + (int(h) // 2)
                crop_frame = frame[Y1:Y2, X1:X2]

                clothes.append(crop_frame)

            

            cv2.imshow("test", annotated_frame)
        else:
            cv2.imshow("test", frame)
    
    # print(f'time_elapse: {end - start}')
    if cv2.waitKey(25) & 0xFF == ord('q'): 
        break