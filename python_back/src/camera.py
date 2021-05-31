from playsound import playsound
from cv2.cv2 import VideoCapture
from queue import Queue
from multiprocessing import Queue as mQueue
from _queue import Empty
import cv2

from python_back.src.detection import Detection
from python_back.src.database import *
from python_back.src.database_utils import read_env
from python_back.src.utils import threaded


class Camera:
    def __init__(self, queue, ip, cam_id, websocket, size=tuple(), display=False, user='', pwd=''):
        self.websocket_queue = websocket
        self.cam_queue: mQueue = queue
        self.ip = self.parseURL(ip, user, pwd)
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
                                   self.db.getEntities(), self.db.getForbiddenAreas(self.id), self.display)
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
        old_res = {}
        while self.cam_queue.empty():
            try:
                res = self.detection_result.get(timeout=5)
            except Empty:
                if old_res != res:
                    # on garde la meme date pour tous les envois
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for animal in res:
                        self.db.addDetectedAnimalLog(animal, res[animal], self.id, timestamp)
                    print("result_log_detected = " + str(res))
                    self.websocket_queue.put("info")
                    res = old_res
        self.stop_all()

    @threaded
    def send_forbidden_access_infos(self):

        while self.cam_queue.empty():
            try:
                res = self.forbidden_access_queue.get(timeout=5)

                # on garde la meme date pour tous les envois
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                animal, (_, id_area)  = res
                playsound("./python_back/byebye_patafix.mp3", block=False)
                self.db.addDetectedInForbiddenAreaLog(animal, id_area, self.id, timestamp)
                print(f"result_log_in_area = {animal}, {id_area}")
                # self.websocket_queue.put("area")

            except Empty:
                pass

