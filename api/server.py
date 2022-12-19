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
    isFront: bool


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
def findPoint(human, p, w, h):
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


# 判定可能か確認
def checkHumans(humans, w, h):
    ok = True
    messages = []

    if len(humans) > 1:
        # 複数人写っているとき
        ok = False
        messages.append("複数の人が写っています。一人だけ写してください。")
        return ok, messages
    if len(humans) < 1:
        # 人が検出されないとき
        ok = False
        messages.append("人を検出できませんでした。")
        return ok, messages
    
    # for p in range(18):
    #     if findPoint(humans[0], p, w, h) == None:
    #         ok = False
    #         messages.append("全身を写してください")
    #         return ok, messages
    
    return ok, messages


def judge_head(human, w, h):
    """
    頭が傾いているかどうかを判定
    体の中心のx座標と、耳のx座標との距離を左右それぞれ計算
    左右の距離の比率が閾値を超えたら悪い姿勢と判定
    """
    # 首の付け根あたりの座標
    center = findPoint(human, 1, w, h)
    # 耳の座標
    mimi_right = findPoint(human, 16, w, h)
    mimi_left = findPoint(human, 17, w, h)

    if center == None or mimi_right == None or mimi_left == None:
        return

    diff_left = abs(mimi_left[0] - center[0])
    diff_right = abs(mimi_right[0] - center[0])
    diff_ratio = max(diff_right, diff_left) / min(diff_right, diff_left)

    threshold = 1.2  # いい感じに調整
    if (diff_ratio >= threshold):
        message = "× 頭が傾いています。"
    else:
        message = "○ 頭はまっすぐです。"

    return message


def judge_lean(human, w, h):
    """
    上体が傾いているかどうかを判定
    体の中心のx座標と、腰のx座標との距離を左右それぞれ計算
    左右の距離の比率が閾値を越えたら悪い姿勢と判定
    """
    # 首の付け根あたりの座標
    center = findPoint(human, 1, w, h)
    # 腰の座標
    kosi_right = findPoint(human, 8, w, h)
    kosi_left = findPoint(human, 11, w, h)

    if center == None or kosi_right == None or kosi_left == None:
        return

    diff_left = abs(kosi_left[0] - center[0])
    diff_right = abs(kosi_right[0] - center[0])
    diff_ratio = max(diff_right, diff_left) / min(diff_right, diff_left)

    threshold = 1.25  # いい感じに調整
    if (diff_ratio >= threshold):
        message = "× 上体が傾いています。"
    else:
        message = "○ 上体はまっすぐです。"
    
    return message


def judge_kosi_front(human, w, h):
    """
    腰が左右のどちらかに出ているかを判定
    両足首の中心のx座標と、腰のx座標との距離を左右それぞれ計算
    左右の距離の比率が閾値を越えたら悪い姿勢と判定
    """
    # 足首の座標
    ankle_right = findPoint(human, 10, w, h)
    ankle_left = findPoint(human, 13, w, h)
    # 腰の座標
    kosi_right = findPoint(human, 8, w, h)
    kosi_left = findPoint(human, 11, w, h)

    if ankle_right == None or ankle_left == None or kosi_right == None or kosi_left == None:
        return

    # 足首の中間の座標
    center = int((ankle_right[0] + ankle_left[0]) / 2)

    diff_left = abs(kosi_left[0] - center)
    diff_right = abs(kosi_right[0] - center)
    diff_ratio = max(diff_right, diff_left) / min(diff_right, diff_left)

    threshold = 1.2  # いい感じに調整
    if (diff_ratio >= threshold):
        message = "× 腰が左右に出ています。両足に体重を乗せてみよう！"
    else:
        message = "○ あなたの腰は正常です。"

    return message


def judge_nekoze(human, w, h):
    """
    耳の位置が肩よりも前に出ているときに猫背と判定
    """
    # 耳の座標
    mimi_right = findPoint(human, 16, w, h)
    mimi_left = findPoint(human, 17, w, h)
    # 肩の座標
    kata_right = findPoint(human, 2, w, h)
    kata_left = findPoint(human, 5, w, h)

    threshold = 10  # いい感じに調整
    if mimi_right is not None and kata_right is not None:
        # 右側で判定
        diff_x = abs(mimi_right[0] - kata_right[0])
        diff_y = abs(mimi_right[1] - kata_right[1])

        if diff_x == 0:
            message = "○ 頭がまっすぐです。"
        elif diff_y / diff_x <= threshold:
            message = "× 頭が傾いています。顎を引いてみよう！"
        else:
            message = "○ 頭がまっすぐです。"
        
        return message

    elif mimi_left is not None and kata_left is not None:
        # 左側で判定
        diff_x = abs(mimi_left[0] - kata_left[0])
        diff_y = abs(mimi_left[1] - kata_left[1])
        
        if diff_x == 0:
            message = "○ 頭がまっすぐです。"
        elif diff_y / diff_x <= threshold:
            message = "× 頭が傾いています。顎を引いてみよう！"
        else:
            message = "○ 頭がまっすぐです。"
        
        return message

    else:
        return


def judge_lean_side(human, w, h):
    """
    肩と腰がまっすぐになっていないとき上体が傾いていると判定
    """
    # 肩の座標
    kata_right = findPoint(human, 2, w, h)
    kata_left = findPoint(human, 5, w, h)
    # 腰の座標
    kosi_right = findPoint(human, 8, w, h)
    kosi_left = findPoint(human, 11, w, h)

    threshold = 10  # いい感じに調整
    if kata_right is not None and kosi_right is not None:
        # 右側で判定
        diff_x = abs(kata_right[0] - kosi_right[0])
        diff_y = abs(kata_right[1] - kosi_right[1])

        if diff_x == 0:
            message = "○ 上体がまっすぐです。"
        elif diff_y / diff_x <= threshold:
            message = "× 上体が傾いています。体をまっすぐにしてみよう！"
        else:
            message = "○ 上体がまっすぐです。"

        return message
    
    elif kata_left is not None and kosi_left is not None:
        # 左側で判定
        diff_x = abs(kata_left[0] - kosi_left[0])
        diff_y = abs(kata_left[1] - kosi_left[1])

        if diff_x == 0:
            message = "○ 上体がまっすぐです。"
        elif diff_y / diff_x <= threshold:
            message = "× 上体が傾いています。体をまっすぐにしてみよう！"
        else:
            message = "○ 上体がまっすぐです。"

        return message

    else:
        return


def judge_kosi_side(human, w, h):
    """
    肩と腰がまっすぐになっていないとき腰が出ていると判定
    """
    # 腰の座標
    kosi_right = findPoint(human, 8, w, h)
    kosi_left = findPoint(human, 11, w, h)
    # 足首の座標
    asi_right = findPoint(human, 10, w, h)
    asi_left = findPoint(human, 13, w, h)

    threshold = 10  # いい感じに調整
    if kosi_right is not None and asi_right is not None:
        # 右側で判定
        diff_x = abs(kosi_right[0] - asi_right[0])
        diff_y = abs(kosi_right[1] - asi_right[1])

        if diff_x == 0:
            message = "○ 腰がまっすぐです。"
        elif diff_y / diff_x <= threshold:
            message = "× 腰が前後に出ています。腰をまっすぐにしてみよう！"
        else:
            message = "○ 腰がまっすぐです。"

        return message
    
    elif kosi_left is not None and asi_left is not None:
        # 左側で判定
        diff_x = abs(kosi_left[0] - asi_left[0])
        diff_y = abs(kosi_left[1] - asi_left[1])

        if diff_x == 0:
            message = "○ 腰がまっすぐです。"
        elif diff_y / diff_x <= threshold:
            message = "× 腰が前後に出ています。腰をまっすぐにしてみよう！"
        else:
            message = "○ 腰がまっすぐです。"

        return message

    else:
        return


def judge(human, w, h, isFront):
    if isFront:
        # 正面の場合
        messages = []
        
        res_head = judge_head(human, w, h)
        if res_head is not None:
            messages.append(res_head)
        
        res_lean = judge_lean(human, w, h)
        if res_lean is not None:
            messages.append(res_lean)

        res_kosi_front = judge_kosi_front(human, w, h)
        if res_kosi_front is not None:
            messages.append(res_kosi_front)

    else:
        # 側面の場合
        messages = []

        res_nekoze = judge_nekoze(human, w, h)
        if res_nekoze is not None:
            messages.append(res_nekoze)
        
        res_lean_side = judge_lean_side(human, w, h)
        if res_lean_side is not None:
            messages.append(res_lean_side)

        res_kosi_side = judge_kosi_side(human, w, h)
        if res_kosi_side is not None:
            messages.append(res_kosi_side)
    
    return messages


@app.post("/")
async def main(webcam_base64: WebcamBase64):
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
    ok, messages = checkHumans(humans, w, h)

    # 判定できる場合は判定
    if len(humans):
        # 判定
        messages = judge(humans[0], w, h, webcam_base64.isFront)
    
    if len(messages) == 0:
        messages.append("判定に失敗しました。全身が写るように撮影してください。")

    return {"ok": ok, "messages": messages, "image": res_base64}
