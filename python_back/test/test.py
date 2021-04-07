from python_back.src.camera import Camera
from python_back.src.database import Database
from multiprocessing import Process, Queue

from python_back.src.database_utils import read_env
import time

if __name__ == '__main__':
    db = Database(read_env())
    # # cam = Camera("http://192.168.1.71:8080/stream.mjpeg", 1, size=(1280, 720), display=True)
    # # cam = Camera("rtsp://freja.hiof.no:1935/rtplive/definst/hessdalen03.stream", 1, size=(1280, 720), display=True)
    # # cam = Camera("http://wmccpinetop.axiscam.net/mjpg/video.mjpg", 1, size=(1280, 720), display=True)
    # # cam = Camera("http://158.58.130.148:80/mjpg/video.mjpg", 1, size=(1280, 720), display=True)
    room_ids = db.getRooms()
    # room_ids.append(("rtsp://freja.hiof.no:1935/rtplive/definst/hessdalen03.stream", 1))

    cams = list()
    queues = list()

    for room_id in room_ids:
        room_id = room_id[0]
        queue = Queue()
        camera_ip, user, pwd = db.getCameraFromRoomWithID(room_id)[0]
        # camera_ip = 0
        p = Process(target=Camera, args=(queue, camera_ip, room_id, (1280, 720), True, user, pwd))
        p.start()
        queues.append(queue)
        cams.append(p)
    db.closeConnection()
    time.sleep(1000)
    for i, cam in enumerate(cams):
        queues[i].put("stop")
        cam.join()

