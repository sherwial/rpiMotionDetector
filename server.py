from image import take_image
import cv2 as cv
 
from flask import Flask
from flask import send_file
import threading
#cap.set()


class Server(threading.Thread):
    def __init__(self, obs):
        self.observs = obs
        threading.Thread.__init__(self)
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            string = "Observances:"
            for o in self.observs:
                string+="\n"
                string = string + '\n'
                string+=o

            return string

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
