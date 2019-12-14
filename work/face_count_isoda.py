#!/usr/bin/env python
# coding: utf-8

# ライブラリのインポート
from flask import Flask,render_template, Response
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
# 不要な警告を非表示にする
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__, static_folder='./static', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html', num = num)

# Webカメラの画像をリアルタイム検出
if __name__ == '__main__':
    # 定数定義
    ESC_KEY = 27     # Escキー
    INTERVAL= 2000     # 待ち時間
    FRAME_RATE = 30  # 30fps
    CAPACITY = 10
    WINDOW_NAME_IN = "in" # inのwindow nameの指定
    WINDOW_NAME_OUT = "out" # outのwindow nameの指定

    # デバイスの指定
    DEVICE_ID_IN = 0
    # DEVICE_ID_OUT = 1

    # 分類器の指定
    cascade_file = "haarcascade_frontalface_default.xml"

    # 分類器の読み込み
    cascade = cv2.CascadeClassifier(cascade_file)

    # カメラ映像取得
    cap_in = cv2.VideoCapture(DEVICE_ID_IN)
    # cap_out = cv2.VideoCapture(DEVICE_ID_OUT)

    # 初期フレームの読込
    end_flag, c_frame_in = cap_in.read()
    height, width, channels = c_frame_in.shape
    # end_flag, c_frame_out = cap_out.read()
    # height, width, channels = c_frame_out.shape

    # ウィンドウの準備
    cv2.namedWindow(WINDOW_NAME_IN)
    # cv2.namedWindow(WINDOW_NAME_OUT)

    # 人数の初期値
    count_in = 0
    # count_out = 0

    # 変換処理ループ
    while end_flag == True:

        # 画像の取得と顔の検出
        img_in = c_frame_in

        face_list_in = cascade.detectMultiScale(img_in, minSize=(100, 100))

        # 検出した顔に印を付ける
        for (x, y, w, h) in face_list_in:
            # 白のフレームに指定
            color = (255, 255, 225)
            pen_w = 3
            cv2.rectangle(img_in, (x, y), (x+w, y+h), color, thickness = pen_w)
            count_in += 1
        # 左右反転
        img_in_flip = cv2.flip(img_in, 1)
        # フレーム表示

        cv2.imshow(WINDOW_NAME_IN, img_in_flip)


        # # 画像の取得と顔の検出
        # img_out = c_frame_out
        # #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # face_list_out = cascade.detectMultiScale(img_out, minSize=(100, 100))
        #
        # # 検出した顔に印を付ける
        # for (x, y, w, h) in face_list_out:
        #     # 白のフレームに指定
        #     color = (255, 255, 225)
        #     pen_w = 3
        #     cv2.rectangle(img_out, (x, y), (x+w, y+h), color, thickness = pen_w)
        #     count_out += 1
        #
        # # 左右反転
        # img_out_flip = cv2.flip(img_out, 1)
        #
        # # フレーム表示
        # cv2.imshow(WINDOW_NAME_OUT, img_out_flip)

        # 部屋の人数をnumで定義
        # num = count_in - count_out
        num = count_in

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break

        # 次のフレーム読み込み
        end_flag, c_frame_in = cap_in.read()
        # end_flag, c_frame_out = cap_out.read()

    # 終了処理
    cap_in.release()
    # cap_out.release()
    cv2.destroyAllWindows()
