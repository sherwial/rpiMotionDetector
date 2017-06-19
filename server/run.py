#!/usr/bin/python
import socket
from flask import Flask
from flask import send_file,render_template
from flask import Response
import threading
import cv2

# ip = socket.gethostbyname(socket.gethostname())

class Server(threading.Thread):
    def __init__(self, obs, picamobj):
        self.observs = obs
        threading.Thread.__init__(self)
        self.app = Flask(__name__)
        self.cam = picamobj

        @self.app.route('/')
        def observations():
            return render_template('observations.html', observs=self.observs)

        @self.app.route('/static/<filename>')
        def file(filename):
            try:
                return send_file('../'+filename+'.jpeg')
            except:
                return "Image outdated"

        @self.app.route('/video')
        def video_feed():
            return Response(self.gen(self.cam),
                            mimetype='multipart/x-mixed-replace; boundary=frame')


        def gen(self, camera):
            while True:
                frame = camera.getImage()
                ret, jpeg = cv2.imencode('.jpg', frame)
                bytes = jpeg.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        # @self.app.route('/take')
        # def take_pic():
        #     cap = cv.VideoCapture(0)
        #     cap.set(3,1280)
        #     cap.set(4,1024)
        #     ret,frame = cap.read()
        #     cv.imwrite('image.png',frame)
        #     cap.release()
        #     return "took image"

    def run(self):
        self.app.run(host='0.0.0.0', threaded=True)
