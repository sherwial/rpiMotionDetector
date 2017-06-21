from video import PiCamWrapper
from frameprocessor import FrameProcessor
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


observances = [] # server
pcam = PiCamWrapper()
s = Server(observances, pcam)  # server

s.start()
pcam.setResolution(1664, 1232)
time.sleep(.1)

count = 0
framesPerProcess = 0  # Process rate
sleep_time = 1
data_array = []
frameQueue = Queue.Queue()
frame_processor = FrameProcessor(data_array, observances, frameQueue)
frame_processor.start()
while(True):
    threading._sleep(sleep_time)
    pcam.captureImage()
    if count > framesPerProcess:
        count = 0
        frameQueue.put(pcam.getImage())
    count += 1
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     frame_processor.status = False
    #     break

#cap.release()
#cv2.destroyAllWindows()
# data_array = data_array[30:]
# processed_data = [(t.year,t.month,t.day,t.hour,t.minute,t.second) for t in data_array]
# last_data = None
# filtered_data = []
# for i in processed_data:
#     if last_data == None:
#         last_data = i
#         filtered_data.append(i)
#     else:
#         if i[1] == last_data[1] \
#         and i[2] == last_data[2] \
#         and i[3] == last_data[3] \
#         and i[4] == last_data[4] \
#         and i[5] == last_data[5]:
#             pass
#         else:
#             filtered_data.append(i)
#             last_data = i
#
# pkl.dump(filtered_data, open("movements.pickle", "wb"))
# print "Data File Created"
# d = pkl.load(open("movements.pickle", "rb"))
# for i in d:
#     print i
