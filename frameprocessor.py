import threading
import cv2
import uuid
import numpy as np
import time

class FrameProcessor():
    def __init__(self,data_array):
        threading.Thread.__init__(self)
        self.areaFilterLower = 16000  # FrameProcessor
        self.areaFilterUpper = 1600000  # FrameProcessor
        self.kernel = np.ones((11, 11), np.uint8)  # frameProcessor
        self.kerneld = np.ones((19, 19), np.uint8) # frameProcessor
        self.saw_something = 0
        self.observance_time = 0
        self.movement_foundation = time.time()
        self.seconds_between_image =2
        self.last_image_time = time.time()
        self.status = True
        self.queue = queue
        self.data = data_array
        self.frame_const = 0

    def process_frame(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.frame_const = cv2.addWeighted(self.frame_const, .8, gray, .2, 0)
        diff = cv2.absdiff(gray, self.frame_const)
        ret, thresh = cv2.threshold(diff, 20,255,cv2.THRESH_BINARY)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, self.kernel)
        opening = cv2.morphologyEx(opening, cv2.MORPH_DILATE, self.kerneld)
        image,cnts,hier = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cnts,hier = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for thing in map(self.area, cnts):
            if (thing > areaFilterLower) and (thing < areaFilterUpper):
                print "Movement"
                if time.time()-self.last_image_time > self.seconds_between_image:
                    self.last_image_time = time.time()
                    id = uuid.uuid1().get_hex()
                    cv2.imwrite(str(id)+'.jpeg',frame)
                    observances.append({"uuid":id, "time":time.time(), "date": time.strftime("%c")})
                break

    def area(self, contour):
        return cv2.contourArea(contour)