import cv2
from utils import FACE_H, FACE_W

def preprocess(img):
    res = cv2.resize(img, (FACE_W, FACE_H))
    return res