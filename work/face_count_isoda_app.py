#!/usr/bin/env python
# coding: utf-8

# ライブラリのインポート
import socket
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

    def __init__(self):
        # 定数定義
        ESC_KEY = 27 # Escキー
        INTERVAL= 2000  # 待ち時間
        FRAME_RATE = 30  # 30fps
        CAPACITY = 10
        WINDOW_NAME_IN = "in" # inのwindow nameの指定
        WINDOW_NAME_OUT = "out" # outのwindow nameの指定
        # デバイスの指定
        DEVICE_ID_IN = 0
        # 開発中はPCのカメラののみ使用しているので，デバイスの指定が一緒になっている．
        DEVICE_ID_OUT = 0
        # カメラの映像を取得
        self.video_in = cv2.VideoCapture(DEVICE_ID_IN)
        self.video_out = cv2.VideoCapture(DEVICE_ID_OUT)
        self.count_in = 0
        self.count_out = 0

    def __del__(self):
        # 終了処理（実行の仕方が不明）
        self.video_in.release()
        self.video_out.release()

    def get_frame_in(self):
        # 分類器の指定
        cascade_file = "haarcascade_frontalface_default.xml"
        # 自作したカスケード分類器
        # cascade_file = "cascade.xml"
        # 分類器の読み込み
        cascade = cv2.CascadeClassifier(cascade_file)
        # フレームの読み込み
        success_in, image_in = self.video_in.read()
        # 人数の初期値
        self.count_in = 0
        # 顔検出処理ループ
        while success_in == True:
            # 画像の取得と顔の検出
            height, width, channels = image_in.shape
            face_list_in = cascade.detectMultiScale(image_in, minSize=(100, 100))
            # 検出した顔に印を付ける
            for (x, y, w, h) in face_list_in:
                # 白のフレームに指定
                color = (255, 255, 225)
                pen_w = 3
                cv2.rectangle(image_in, (x, y), (x+w, y+h), color, thickness = pen_w)
                # 人数をカウント
                self.count_in += 1
            # 左右反転処理
            image_in_flip_lr = cv2.flip(image_in, 1)
            # jpgに変換
            ret_in, jpeg_in = cv2.imencode('.jpg', image_in_flip_lr)

            # 入店者数を返す．以下のように記述すると映像が出力されなくなる．
            # どうすれば映像と人数が同時にhtmlに出力できるうようなるか検討中
            # return render_template('index.html', count_in=count_in)

            # 変換したものを返す
            return jpeg_in.tobytes(), self.count_in
            # Escキーで終了（機能していない）
            key = cv2.waitKey(INTERVAL)
            if key == ESC_KEY:
                break
            # 次のフレーム読み込み
            success_in, image_in = cap_in.read()

    def get_frame_out(self):
        # 分類器の指定
        cascade_file = "haarcascade_frontalface_default.xml"
        # 分類器の読み込み
        cascade = cv2.CascadeClassifier(cascade_file)
        # フレームの読み込み
        success_out, image_out = self.video_out.read()
        # 人数の初期値
        self.count_out = 0
        # 顔検出処理ループ
        while success_out == True:
            # 画像の取得と顔の検出
            height, width, channels = image_out.shape
            face_list_out = cascade.detectMultiScale(image_out, minSize=(100, 100))
            # 検出した顔に印を付ける
            for (x, y, w, h) in face_list_out:
                # 白のフレームに指定
                color = (255, 255, 225)
                pen_w = 3
                cv2.rectangle(image_out, (x, y), (x+w, y+h), color, thickness = pen_w)
                # 人数をカウント
                self.count_out += 1
            # 左右反転処理
            image_out_flip_lr = cv2.flip(image_out, 1)
            # jpgに変換
            ret_out, jpeg_out = cv2.imencode('.jpg', image_out_flip_lr)
            # 変換したものを返す
            return jpeg_out.tobytes(), self.count_out
            # Escキーで終了（機能していない）
            key = cv2.waitKey(INTERVAL)
            if key == ESC_KEY:
                break
            # 次のフレーム読み込み
            success_out, image_out = cap_in.read()

    def get_num(self):
        # 分類器の指定
        cascade_file = "haarcascade_frontalface_default.xml"

        # 分類器の読み込み
        cascade = cv2.CascadeClassifier(cascade_file)
        # フレームの読み込み
        success, image_in = self.video_in.read()
        success, image_out = self.video_out.read()
        # 人数の初期値
        self.count_in = 0
        self.count_out = 0
        # 変換処理ループ
        while  True:
            # 画像の取得と顔の検出
            height, width, channels = image_in.shape
            face_list_in = cascade.detectMultiScale(image_in, minSize=(100, 100))
            height, width, channels = image_out.shape
            face_list_out = cascade.detectMultiScale(image_out, minSize=(100, 100))
            # 検出した顔に印を付ける
            for (x, y, w, h) in face_list_in:
                # 白のフレームに指定
                color = (255, 255, 225)
                pen_w = 3
                cv2.rectangle(image_in, (x, y), (x+w, y+h), color, thickness = pen_w)
                self.count_in += 1

            for (x, y, w, h) in face_list_out:
                # 白のフレームに指定
                color = (255, 255, 225)
                pen_w = 3
                cv2.rectangle(image_out, (x, y), (x+w, y+h), color, thickness = pen_w)
                self.count_out += 1

            num = self.count_in - self.count_out

            return num

    # ファイルの保存（今回は実装しない予定）
    # def save_frame_in(self):
    #     dirname_in = './static/images_in/'
    #     if not os.path.exists(dirname_in):
    #         os.mkdir(dirname_in)
    #     success_in, image_in = self.video_in.read()
    #     image_in_flip_lr = cv2.flip(image_in, 1)
    #     file_name_in = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".jpg"
    #     try:
    #         for i in os.listdir(dirname_in):
    #                 os.remove(os.path.join(dirname_in,i))
    #         cv2.imwrite(os.path.join(dirname_in,file_name_in), image_in_flip_lr)
    #         print("saved")
    #     except:
    #         save("not saved")
    #     return file_name_in

    # ファイルの保存（今回は実装しない予定）
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
