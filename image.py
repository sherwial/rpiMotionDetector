import cv2 as cv

cap = cv.VideoCapture(0)

#cap.set(3,1280)
#cap.set(4,720)
ret, frame = cap.read()
height, width,channels = frame.shape
print height
print width
cv.imwrite('image.png',frame)
cap.release()
