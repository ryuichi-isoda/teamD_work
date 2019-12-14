#!/usr/bin/env python
# coding: utf-8

# ライブラリのインポート
# from base_camera import BaseCamera
from flask import Flask,render_template, Response
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
import datetime

# Webカメラの画像をリアルタイム検出
class Camera(object):
    # 定数定義
    ESC_KEY = 27 # Escキー
    INTERVAL= 2000  # 待ち時間
    FRAME_RATE = 30  # 30fps
    CAPACITY = 10
    WINDOW_NAME_IN = "in" # inのwindow nameの指定
    WINDOW_NAME_OUT = "out" # outのwindow nameの指定

    # 分類器の指定
    cascade_file = "haarcascade_frontalface_default.xml"

    # 分類器の読み込み
    cascade = cv2.CascadeClassifier(cascade_file)

    def __init__(self):
        # デバイスの指定
        DEVICE_ID_IN = 0
        # DEVICE_ID_OUT = 1
        # カメラの映像を取得
        self.video_in = cv2.VideoCapture(DEVICE_ID_IN)
        # self.video_out = cv2.VideoCapture(DEVICE_ID_OUT)

    def __del__(self):
        # 終了処理
        self.video_in.release()
        # self.video_out.release()

    def get_frame_in(self):
        # フレームの読み込み
        success_in, image_in = self.video_in.read()
        # 人数の初期値
        count_in = 0
        # 変換処理ループ
        while success_in == True:
            # 画像の取得と顔の検出
            height, width, channels = image_in.shape
            face_list_in = cascade.detectMultiScale(img_in, minSize=(100, 100))
            # 検出した顔に印を付ける
            for (x, y, w, h) in face_list_in:
                # 白のフレームに指定
                color = (255, 255, 225)
                pen_w = 3
                cv2.rectangle(img_in, (x, y), (x+w, y+h), color, thickness = pen_w)
                count_in += 1
            # 左右反転処理
            img_in_flip_lr = cv2.flip(image_in, 1)
            # jpgに変換
            ret_in, jpeg_in = cv2.imencode('.jpg', img_in_flip_lr)
            # フレーム表示
            # cv2.imshow(WINDOW_NAME_IN, img_in_flip_lr)
            # 変換したものを返す
            return jpeg_in.tobytes()
            # Escキーで終了
            key = cv2.waitKey(INTERVAL)
            if key == ESC_KEY:
                break
            # 次のフレーム読み込み
            end_flag, c_frame_in = cap_in.read()
        cv2.destroyAllWindows()

    # def get_frame_out(self):
    #     success_out, image_out = self.video_out.read()
    #     img_out_flip_lr = cv2.flip(image_out, 1)
    #     ret_out, jpeg_out = cv2.imencode('.jpg', img_out_flip_lr)
    #     return jpeg_out.tobytes()

    # ファイルの保存
    def save_frame_in(self):
        dirname_in = './static/images_in/'
        if not os.path.exists(dirname_in):
            os.mkdir(dirname_in)
        success_in, image_in = self.video_in.read()
        img_in_flip_lr = cv2.flip(image_in, 1)
        file_name_in = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".jpg"
        try:
            for i in os.listdir(dirname_in):
                    os.remove(os.path.join(dirname_in,i))
            cv2.imwrite(os.path.join(dirname_in,file_name_in), img_in_flip_lr)
            print("saved")
        except:
            save("not saved")
        return file_name_in

    # ファイルの保存
    # def save_frame_out(self):
    #     dirname_out = './static/images_out/'
    #     if not os.path.exists(dirname_out):
    #         os.mkdir(dirname_out)
    #     success_out, image_out = self.video_in.read()
    #     img_out_flip_lr = cv2.flip(image_out, 1)
    #     file_name_out = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".jpg"
    #     try:
    #         for i in os.listdir(dirname_out):
    #                 os.remove(os.path.join(dirname_out,i))
    #         cv2.imwrite(os.path.join(dirname_out,file_name_out), img_out_flip_lr)
    #         print("saved")
    #     except:
    #         save("not saved")
    #     return file_name_out


    def frames():
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

        cv2.destroyAllWindows()
        # return render_template('index.html', num = num)
