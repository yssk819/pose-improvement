import cv2
import numpy as np
import base64
from tkinter.tix import IMAGE
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebcamBase64(BaseModel):
    data: str

# Webcamのデータを画像に変換
def decode_webcam(webcam_base64):
    # いらない文字列を削除
    target = "data:image/jpeg;base64,"
    idx = webcam_base64.find(target)
    webcam_base64 = webcam_base64[idx+len(target):]

    # 変換
    webcam_binary = base64.b64decode(webcam_base64)
    webcam_png = np.frombuffer(webcam_binary, dtype=np.uint8)
    webcam_img = cv2.imdecode(webcam_png, cv2.IMREAD_COLOR)

    return webcam_img

def create_response():
    pass


@app.post("/")
async def judge(webcam_base64: WebcamBase64):
    # webcam_img = decode_webcam(webcam_base64)
    # if webcam_img:
    #     print("画像を受け取りました")
    #     print(webcam_img.shape)

    return {"res": "悪い姿勢です"}
