import asyncio
import threading
from datetime import datetime
import time

import cv2
from python_back.src.detection import Detection
from python_back.src.database import *
from cv2.cv2 import VideoCapture
from queue import Queue
from python_back.src.database_utils import read_env
from multiprocessing import Queue as mQueue
from _queue import Empty


def threaded(fn):
    """
    Allow to launch function with threads using decorators
    @param fn: function to be threaded
    @return: wrapper for thread
    """
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return wrapper


class Camera:
    def __init__(self, queue, ip, cam_id, size=tuple(), display=False , user='', pwd=''):
        self.cam_queue: mQueue = queue
        self.ip = self.parseURL(ip,user,pwd)
        self.display = display
        self.id = cam_id
        self.size = size
        self.cap: VideoCapture
        self.detection: Detection
        self.db = Database(read_env())
        self.forbidden_access_queue = Queue()
        self.detection_queue = Queue()
        self.detection_result = Queue()
        self.startCamera()

        # threaded event listeners
        self.save_infos()
        self.send_forbidden_access_infos()

    def stop_all(self):
        self.releaseCamera()
        self.db.closeConnection()

    def startCamera(self):
        if self.ip == 0:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(str(self.ip))
        if len(self.size) == 2:
            # Parametres capture video
            self.cap.set(3, self.size[0])
            self.cap.set(4, self.size[1])
            self.cap.set(10, 150)

        self.detection = Detection(self, self.detection_queue, self.detection_result, self.forbidden_access_queue,
                                   self.db.getEntities(), self.db.getForbiddenAreas(), self.display)
        self.detection.start()

    def displayCamera(self):
        ret, frame = self.getFrame()
        while ret:
            # Capture frame-by-frame
            ret, frame = self.getFrame()
            # Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def releaseCamera(self):
        if self.detection.is_alive():
            self.stopDetection()
        self.cap.release()

    def getFrame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def stopDetection(self):
        self.detection_queue.put("end")
        self.detection.join()

    def getID(self):
        return self.id

    def parseURL(self, ip, user, pwd):
        if ip.startswith('http://', 0, 6):
            temp = ip[:6]
        else:
            temp = ip
        return 'http://' + user + ':' + pwd + '@' + temp

    @threaded
    def save_infos(self):
        res = {}
        while self.cam_queue.empty():
            try:
                res = self.detection_result.get(timeout=5)
            except Empty:
                # on garde la meme date pour tous les envois
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for animal in res:
                    self.db.addLog(animal, res[animal], self.id, time)
                print("result_log_detected = " + str(res))
                res = {}
        self.stop_all()

    @threaded
    def send_forbidden_access_infos(self):

        res = {}
        while self.cam_queue.empty():
            try:
                res = self.forbidden_access_queue.get(timeout=2)
            except Empty:
                # on garde la meme date pour tous les envois
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for animal in res:
                    # TODO: Add insert for forbidden accesses db
                    pass
                print("result_log_in_area = " + str(res))
                time.sleep(10)
                res = {}
