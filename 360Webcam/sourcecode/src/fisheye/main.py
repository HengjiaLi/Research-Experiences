from flask import Flask, render_template, Response
from camera import VideoCamera
import threading
import pcn
import cv2 as cv


global fisheye_frame
global detected_frame
global winlist
fisheye_frame=None
detected_frame=None
winlist=None
def face_detector():
    global fisheye_frame
    global detected_frame
    global winlist
    while True:
        if type(fisheye_frame)!=type(None):
            winlist = pcn.detect(fisheye_frame)
            detected_frame= pcn.draw(fisheye_frame, winlist)

def cv2byte(img):
    ret,jpg=cv.imencode('.jpg', img)
    return jpg.tobytes()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    global fisheye_frame
    global detected_frame
    # set something into background
#    T=threading.Thread(target=camera.main, daemon=True)
#    T.start()
    while True:
        fisheye_frame= camera.get_frame()
        if type(detected_frame)!=type(None):
            frame=detected_frame
        else:
            frame=fisheye_frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2byte(frame) + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
#    return Response(gen(VideoCamera()),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    T=threading.Thread(target=face_detector, daemon=True)
    T.start()
    app.run(host='0.0.0.0', debug=True,threaded=True)
