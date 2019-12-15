from flask import Flask, render_template, Response, request
from face_count_isoda_app import Camera

app = Flask(__name__, static_folder='./static', static_url_path='')

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        filename=Camera().save_frame_in()
        return render_template('photo_in.html', filename=filename)
    elif request.method =='GET':
        return render_template('index.html')
# ----------------------------------------
def gen(camera):
    while True:
        frame_in = camera.get_frame_in()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_in + b'\r\n\r\n')
        frame_out = camera.get_frame_out()
        yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame_out + b'\r\n\r\n')

@app.route('/video_feed_in')
def video_feed_in():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_out')
def video_feed_out():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# ----------------------------------------

# アプリケーションを動かすためのおまじない
if __name__ == "__main__":
    app.run(port=8000, debug=True)
