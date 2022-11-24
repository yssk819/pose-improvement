import cv2
import numpy as np
import matplotlib.pyplot as plt

from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path


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
        messages.append({"message": "一人だけ写してください"})
        return ok, messages
    if len(humans) < 1:
        # 人が検出されないとき
        ok = False
        messages.append({"message": "人を検出できません"})
        return ok, messages
    
    for p in range(18):
        if findPoint(humans[0], p, w, h) == None:
            ok = False
            messages.append({"message": "全身を写してください"})
            return ok, messages
    
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

    diff_left = abs(mimi_left[0] - center[0])
    diff_right = abs(mimi_right[0] - center[0])
    diff_ratio = max(diff_right, diff_left) / min(diff_right, diff_left)

    threshold = 1.2  # いい感じに調整
    if (diff_ratio >= threshold):
        comment = "頭が傾いています。"
    else:
        comment = "頭はまっすぐです。"

    print(comment)  # test
    return comment


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

    diff_left = abs(kosi_left[0] - center[0])
    diff_right = abs(kosi_right[0] - center[0])
    diff_ratio = max(diff_right, diff_left) / min(diff_right, diff_left)

    threshold = 1.25  # いい感じに調整
    if (diff_ratio >= threshold):
        comment = "上体が傾いています。"
    else:
        comment = "上体はまっすぐです。"
    
    print(comment)  # test
    return comment


def judge_kosi(human, w, h):
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

    # 足首の中間の座標
    center = int((ankle_right[0] + ankle_left[0]) / 2)

    diff_left = abs(kosi_left[0] - center)
    diff_right = abs(kosi_right[0] - center)
    diff_ratio = max(diff_right, diff_left) / min(diff_right, diff_left)

    threshold = 1.2  # いい感じに調整
    if (diff_ratio >= threshold):
        comment = "腰が左右に出ています。両足に体重を乗せてみよう！"
    else:
        comment = "あなたの腰は正常です。"

    print(comment)  # test
    return comment


def judge(human, w, h, isFront):
    if isFront:
        # 正面の場合
        comments = []
        comments.append({"comment": judge_head(human, w, h)})
        comments.append({"comment": judge_lean(human, w, h)})
        comments.append({"comment": judge_kosi(human, w, h)})
        comments.append({"comment": "首が曲がっています"})
    else:
        # 側面の場合
        comments = []
    
    return comments


def main():
    # ===== 設定 =====
    isFront = True
    image_path = "../images/MicrosoftTeams-image (31).png"
    # image_path = "../images/kosi.png"
    image = common.read_imgfile(image_path, None, None)

    # ===== モデルの読み込み =====
    h, w = image.shape[0], image.shape[1]
    model = "mobilenet_thin"
    tensorrt = "False"
    resize_out_ratio = 4.0
    e = TfPoseEstimator(get_graph_path(model), target_size=(w, h), trt_bool=str2bool(tensorrt))

    # ===== 姿勢の推定 =====
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
    image_res = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

    # ===== 判定 =====
    # 判定可能か確認
    ok, messages = checkHumans(humans, w, h)

    # メッセージを表示してみる (テスト)
    for m in messages:
        print(m)

    # 判定できる場合は判定
    if ok:
        # 判定
        messages = judge(humans[0], w, h, isFront)
    
    # ===== 画像を表示 =====
    cv2.imwrite("../images/judge.png", image_res)


if __name__ == "__main__":
    main()
