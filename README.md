# 立ち姿勢改善アプリ

創造工学特別実験 チームD


## 概要

カメラで体の正面・側面の写真を撮影して姿勢を判定し、改善のためのアドバイスを表示する


## APIサーバの準備

`/api`の中で以下を実行

必要なライブラリをインストール

```
pip --default-timeout=1000 install argparse dill fire matplotlib numba numpy psutil pycocotools requests scikit-image scipy slidingwindow tqdm swig tensorflow tensorpack tf-slim opencv-python
```

OpenPose環境の準備

```
cd tf_pose/pafprocess/
swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
cd ../../
cd models/graph/cmu/
bash download.sh
cd ../../../
```

APIサーバ起動

```
uvicorn server:app --reload
```


## 参考
- https://github.com/gsethi2409/tf-pose-estimation
