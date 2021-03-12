import asyncio

import cv2
from python_back.src.detection import  Detection
from cv2.cv2 import VideoCapture
from queue import Queue


class Camera:
    def __init__(self, ip, cam_id, size=tuple(), display=False):
        self.ip = ip
        self.display = display
        self.id = cam_id
        self.size = size
        self.cap: VideoCapture = 0
        self.startCamera()
        asyncio.run(self.save_infos())

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
        self.detection_queue = Queue()
        self.detection_result = Queue()
        self.detection = Detection(self.detection_queue, self, self.detection_result, self.display)
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

    async def save_infos(self):
        while True:
            # TODO: send data to BDD
            res = self.detection_result.get()
            print("result = " + str(res))
            await asyncio.sleep(1)



