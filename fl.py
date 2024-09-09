from flask import Flask, render_template, Response, json
from camera import VideoCamera
from detect_drowsiness import Drowsy
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('driver123.html')

def gen(camera):
    while True:
        if Drowsy.flag==False:
            continue
        frame = camera.get_frame()
        bro = Drowsy.det(frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + bro + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    if Drowsy.flag:
        return Response(gen(VideoCamera()),
            mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/stahp")
def kill_stream():
    Drowsy.flag=False
    VideoCamera.__del__(VideoCamera())
    return "Video Stopped"


@app.route("/stonks")
def stonks_stream():
    Drowsy.flag=True
    return "Video started"
if __name__ == '__main__':
    app.run()
