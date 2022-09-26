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
def base64_to_img(base64_data):
    # 不要な文字列を削除
    target = "data:image/png;base64,"
    idx = base64_data.find(target)
    base64_data = base64_data[idx+len(target):]
    
    # 変換
    bin_data = base64.b64decode(base64_data)
    np_data = np.frombuffer(bin_data, dtype=np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    return img

# 画像をbase64に変換
def img_to_base64(img):
    _, img = bin_data = cv2.imencode(".png", img)
    base64_data = base64.b64encode(img)

    return base64_data

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


@app.post("/")
async def judge(webcam_base64: WebcamBase64):
    webcam_img = base64_to_img(webcam_base64.data)
    w = webcam_img.shape[1]
    h = webcam_img.shape[0]

    # モデルの読み込み
    model = "mobilenet_thin"
    tensorrt = "False"
    resize_out_ratio = 4.0
    e = TfPoseEstimator(get_graph_path(model), target_size=(w, h), trt_bool=str2bool(tensorrt))
    humans = e.inference(webcam_img, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
    res_img = TfPoseEstimator.draw_humans(webcam_img, humans, imgcopy=False)
    res_base64 = img_to_base64(res_img)

    return {"message": "悪い姿勢です", "image": res_base64}
