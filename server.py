from image import take_image
import cv2 as cv
 
from flask import Flask
from flask import send_file
cap = cv.VideoCapture(0)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return send_file('image.png')

@app.route('/take')
def take_pic():
    ret,frame = cap.read()
    cv.imwrite('image.png',frame) 
    return "took image"
if __name__ == "__main__":




    app.run(host='0.0.0.0')
