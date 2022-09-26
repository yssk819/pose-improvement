import io
import cv2
import numpy as np
import base64
from PIL import Image
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
def decode_base64(base64_data):
    # 不要な文字列を削除
    target = "data:image/png;base64,"
    idx = base64_data.data.find(target)
    base64_data.data = base64_data.data[idx+len(target):]
    
    # 変換
    bin_data = base64.b64decode(base64_data.data)
    np_data = np.frombuffer(bin_data, dtype=np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    return img


@app.post("/")
async def judge(webcam_base64: WebcamBase64):
    webcam_img = decode_base64(webcam_base64)

    return {"res": "悪い姿勢です"}
