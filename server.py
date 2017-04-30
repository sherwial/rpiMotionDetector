from image import take_image
import cv2 as cv
 
from flask import Flask
from flask import send_file
#cap.set()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return send_file('image.png')

@app.route('/take')
def take_pic():
    cap = cv.VideoCapture(0)
    ret,frame = cap.read()
    cv.imwrite('image.png',frame)
    cap.release()
    return "took image"
if __name__ == "__main__":
    app.run(host='0.0.0.0')
