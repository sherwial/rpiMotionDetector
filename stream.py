import numpy as np
import cv2
import datetime
import cPickle as pkl
import threading
import time
import Queue
import uuid
import os, shutil
from server import Server
from picamera.array import PiRGBArray
from picamera import PiCamera
kernel = np.ones((11, 11), np.uint8)
kerneld = np.ones((19, 19), np.uint8)
observances = []
s = Server(observances)
s.start()
camera = PiCamera()
rawCapture = PiRGBArray(camera)
camera.resolution = (1664,1232)
areaFilterLower=16000
areaFilterUpper=1600000
time.sleep(0.1)
def ensure_dir():
    try:
        os.mkdir('images')
    except:
        shutil.rmtree('images')
        os.mkdir('images')

class FrameProcessor(threading.Thread):
    def __init__(self,queue,data_array):
        ensure_dir()
        threading.Thread.__init__(self)
        self.saw_something = 0
        self.observance_time = 0
        self.movement_foundation = time.time()
        self.seconds_between_image =2 
        self.last_image_time = time.time()
        self.status = True
        self.queue = queue
        self.data = data_array
        self.frame_const = 0

    def run(self):
        print "Starting Frame Processor"
        while(self.status == True):
            if self.queue.qsize() == 0:
                threading._sleep(.05)
            else:
                self.process_frame(self.queue.get())

    def process_frame(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.frame_const = cv2.addWeighted(self.frame_const, .8, gray, .2, 0)
        diff = cv2.absdiff(gray, self.frame_const)
        ret, thresh = cv2.threshold(diff, 20,255,cv2.THRESH_BINARY)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        opening = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kerneld)
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

count = 0
framesPerProcess = 0  # Process rate
sleep_time = 1
data_array = []
q = Queue.Queue()

frame_processor = FrameProcessor(q,data_array)
frame_processor.start()

while(True):
    threading._sleep(sleep_time)
    camera.capture(rawCapture, format="bgr")
    #for i in range(0,5):
    #    ret, frame = cap.read()
    frame = rawCapture.array
    if count > framesPerProcess:
        count = 0
        q.put(frame)
    count += 1
    rawCapture.truncate(0)
    rawCapture.seek(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        frame_processor.status = False
        break

#cap.release()
#cv2.destroyAllWindows()
data_array = data_array[30:]
processed_data = [(t.year,t.month,t.day,t.hour,t.minute,t.second) for t in data_array]
last_data = None
filtered_data = []
for i in processed_data:
    if last_data == None:
        last_data = i
        filtered_data.append(i)
    else:
        if i[1] == last_data[1] \
        and i[2] == last_data[2] \
        and i[3] == last_data[3] \
        and i[4] == last_data[4] \
        and i[5] == last_data[5]:
            pass
        else:
            filtered_data.append(i)
            last_data = i

pkl.dump(filtered_data, open("movements.pickle", "wb"))
print "Data File Created"
d = pkl.load(open("movements.pickle", "rb"))
for i in d:
    print i
