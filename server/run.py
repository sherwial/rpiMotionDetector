#!/usr/bin/python
import socket
from flask import Flask
from flask import send_file,render_template
import threading

# ip = socket.gethostbyname(socket.gethostname())

class Server(threading.Thread):
    def __init__(self, obs):
        self.observs = obs
        threading.Thread.__init__(self)
        self.app = Flask(__name__)

        @self.app.route('/')
        def observations():
            return render_template('observations.html', observs=self.observs)

        @self.app.route('/static/<filename>')
        def file(filename):
            try:
                return send_file('../'+filename+'.png')
            except:
                return "Image outdated"
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
        self.app.run(host='0.0.0.0')
