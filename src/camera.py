import cv2
from detection import Detection
from cv2.cv2 import VideoCapture


class Camera:
    def __init__(self, ip, size=tuple()):
        self.ip = ip
        self.cap = 0
        self.size = size


        self.startCamera()

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
        # When everything done, release the capture
        self.cap.release()

    def getFrame(self):
        ret, frame = self.cap.read()
        return ret, frame


if __name__ == '__main__':
    # cam = Camera(0)
    cam = Camera("http://192.168.1.71:8080/stream.mjpeg")
    cam.displayCamera()
    cam.releaseCamera()
