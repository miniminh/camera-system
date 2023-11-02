import cv2
import uvicorn
import os
import time
from fastapi import FastAPI, Request, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi import FastAPI, File, UploadFile, Request
import shutil

from camera_manipulate import get_cam, get_gender

app = FastAPI()
templates = Jinja2Templates(directory="templates")

upload_dir = 'X:/ANHTAI/camera_system/api/uploads'



def gen_frames():
    camera = 'null'
    gender = ''
    cam_gen = get_cam()
    while True:
        new_gender = get_gender()
        if new_gender != gender:
            if gender != 'null':
                RedirectResponse("http://127.0.0.1:8000/play", status_code=status.HTTP_303_SEE_OTHER)
            gender = new_gender
            cam_gen = get_cam()
            camera = next(cam_gen)
            cap = cv2.VideoCapture(camera)
            
        success, frame = cap.read()
        if not success:
            print('no video')
            gender = 'null'
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get('/list')
def get_list(request: Request):
    file_list = {}
    file_list['male'] = []
    file_list['female'] = []
    for root, dirs, files in os.walk(upload_dir + '/male'):
        for file in files:
            f = os.path.join(root, file)
            file_list['male'].append(file)
    for root, dirs, files in os.walk(upload_dir + '/female'):
        for file in files:
            f = os.path.join(root, file)
            file_list['female'].append(file)
    return templates.TemplateResponse("video_list.html", {"request": request, 'file_list': file_list})

@app.get('/changegender')
def change():
    with open('camera/camera.txt', 'r') as f:
        camera = f.read()
    if camera == 'male': 
        camera = 'female'
    else: 
        camera = 'male'
    with open('camera/camera.txt', 'w') as f:
        f.write(camera)
    return RedirectResponse("http://127.0.0.1:8000/play", status_code=status.HTTP_303_SEE_OTHER)

@app.get('/play')
def play(request: Request):
    return templates.TemplateResponse("play.html", {"request": request, 'gender': get_gender()})

@app.get('/')
def homepage(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@app.post('/upload')
async def upload(video: UploadFile = File(...), gender = Form(...)):
    
    with open(f"uploads/{gender}/{video.filename}", "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    return RedirectResponse("http://127.0.0.1:8000/list", status_code=status.HTTP_303_SEE_OTHER)

@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)