import cv2 as cv

def take_image():
    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    cv.imwrite('image.png',frame)
    cap.release()
