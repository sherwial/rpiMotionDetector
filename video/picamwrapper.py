from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np

class PiCamWrapper():
    def __init__(self):
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        self.setResolution(640, 480)
        self.currentImage = np.zeros(self.camera.resolution)
        self.rawCapture.seek(0)
        self.rawCapture.truncate(0)

    def openCam(self):
        pass

    def closeCam(self):
        pass

    def setResolution(self, width, height):
        self.camera.resolution = (width, height)

    def getResolution(self):
        return self.camera.resolution

    def captureImage(self):
        self.camera.capture(self.rawCapture, format="bgr")
        self.currentImage = self.rawCapture.array
        self.rawCapture.seek(0)
        self.rawCapture.truncate(0)

    def getImage(self):
        return self.currentImage
