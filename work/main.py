from flask import Flask, render_template, Response, request
from face_count_isoda_app import Camera

app = Flask(__name__, static_folder='./static', static_url_path='')

@app.route('/', methods = ['GET', 'POST'])
def index():
    num = Camera().get_num()
    return render_template('index.html', num=num)
# ----------------------------------------
def gen_in(camera):
    while True:
        frame = camera.get_frame_in()[0]
        yield (b'--frame\r\n'
               b'Content-Type: image\jpeg_\r\n\r\n' + frame + b'\r\n\r\n')


def gen_out(camera):
    while True:
        frame = camera.get_frame_out()[0]
        yield (b'--frame\r\n'
               b'Content-Type: image\jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed_in')
def video_feed_in():
    return Response(gen_in(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_out')
def video_feed_out():
    return Response(gen_out(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# ----------------------------------------

# アプリケーションを動かすためのおまじない
if __name__ == "__main__":
    app.run(port=8000, debug=True)
