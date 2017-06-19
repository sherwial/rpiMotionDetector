from video import PiCamWrapper
import cv2
import numpy

camObj = PiCamWrapper()
camObj.captureImage()
cv2.imshow("TheImage", camObj.getImage())
cv2.waitKey(0)
cv2.destroyAllWindows()

