import cv2
import uvicorn
import os
import json
import time
import asyncio
from fastapi import FastAPI, Request, status, Form, BackgroundTasks, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse, HTMLResponse
from fastapi import FastAPI, File, UploadFile, Request
import shutil

from camera_manipulate import get_cam, get_gender
from utils import get_csv_headers, get_csv_rows
from check_csv_update import check_csv_update

app = FastAPI()
templates = Jinja2Templates(directory="templates")

upload_dir = 'X:/ANHTAI/camera_system/api/uploads'



def gen_frames():
    camera = 'null'
    gender = ''
    cam_gen = get_cam()
    while True:
        new_gender = get_gender()
        while new_gender == '': 
            new_gender = get_gender()
            time.sleep(1)
        if new_gender != gender:
            if gender != 'null':
                RedirectResponse("/play", status_code=status.HTTP_303_SEE_OTHER)
            gender = new_gender
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
    return RedirectResponse("/play", status_code=status.HTTP_303_SEE_OTHER)

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
    return RedirectResponse("/list", status_code=status.HTTP_303_SEE_OTHER)

@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')
    

@app.websocket("/ws_data")
async def data(websocket: WebSocket):
    """Displays a CSV file."""
    await websocket.accept()
    while True:
        print('called')
        # Get the CSV file path.
        csv_file_path = "X:/ANHTAI/camera_system/data/log.csv"

        while not check_csv_update(csv_file_path):
            await asyncio.sleep(1)

        # Get the list of headers and rows from the CSV file.
        rows = get_csv_rows(csv_file_path)
        json_rows = json.dumps(rows)

        # Send the JSON string to the websocket.    
        await websocket.send_text(json_rows)
        # Pass the headers and rows to the HTML template.
        # await websocket.send_text(f'{headers}, {rows}')
        # await websocket.send_text(templates.TemplateResponse("data.html", {"request": request, "headers": headers, "rows": rows}))

@app.get("/data")
async def get_csv_data(request: Request):
    return templates.TemplateResponse("data.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)