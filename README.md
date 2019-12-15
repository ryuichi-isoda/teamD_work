## 混雑状況確認アプリ
HAIT Lab 2期 東京 Dチーム の最終プロダクトです．

カフェの混雑状況がwebアプリでリアルタイムに確認できるようにします．

### 技術
- openCVのカスケード分類器を使った顔の検出
- flaskでアプリ化

### 実装状況
- [x] openCVを使って顔の検出
- [ ] flaskとの連携
    - [x] 映像を出力
    - [ ] 人数を出力

### 注
face_count_isoda.pyは使いません．openCVの動作確認のために作成しました．

flaskで実装する際は，face_count_isoda_app.pyを使ってください．
