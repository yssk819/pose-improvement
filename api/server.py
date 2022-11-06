import cv2
import numpy as np
import base64
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path

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

# frontから受け取る形式
class WebcamBase64(BaseModel):
    data: str

# base64を画像に変換
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

# 関節の座標を取得 (p:関節の番号)
def findPoint(humans, p, w, h):
    for human in humans:
        try:
            body_part = human.body_parts[p]
            parts = [0,0]

            # 座標を整数に切り上げで置換
            parts[0] = int(body_part.x * w + 0.5)
            parts[1] = int(body_part.y * h + 0.5)
            
            # parts = [x座標, y座標]
            return parts
        
        except:
            pass

def checkPoint(humans, w, h):
    ok = True
    message = "判定可能です"
    if len(humans) > 1:
        ok = False
        message = "一人だけ写してください"
        return ok, message
    if len(humans) < 1:
        ok = False
        message = "人を検出できません"
        return ok, message
    
    for p in range(18):
        if findPoint(humans, p, w, h) == None:
            ok = False
            message = "全身を写してください"
            return ok, message
    return ok, message


@app.post("/")
async def judge(webcam_base64: WebcamBase64):
    webcam_img = base64_to_img(webcam_base64.data)

    # モデルの読み込み
    w = webcam_img.shape[1]
    h = webcam_img.shape[0]
    model = "mobilenet_thin"
    tensorrt = "False"
    resize_out_ratio = 4.0
    e = TfPoseEstimator(get_graph_path(model), target_size=(w, h), trt_bool=str2bool(tensorrt))

    # 姿勢の推定
    humans = e.inference(webcam_img, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
    res_img = TfPoseEstimator.draw_humans(webcam_img, humans, imgcopy=False)
    res_base64 = img_to_base64(res_img)

    # 判定可能か確認
    ok, message = checkPoint(humans, w, h)

    # 判定できる場合は判定
    if ok:
        # 判定
        print("hana", findPoint(humans, 0, w, h))
        print("migime", findPoint(humans, 14, w, h))
        print("hidarime", findPoint(humans, 15, w, h))

    return {"ok": ok, "message": message, "image": res_base64}
