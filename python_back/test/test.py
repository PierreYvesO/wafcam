from python_back.src.camera import Camera
from python_back.src.database import Database
user_config = {
    'user': 'waf',
    'password': 'cam',
    'host': '127.0.0.1',
    'database': 'wafcam',
    'raise_on_warnings': True
}
if __name__ == '__main__':
    db = Database(user_config)
    # cam = Camera("http://192.168.1.71:8080/stream.mjpeg", 1, db, size=(1280, 720), display=True)
    # cam = Camera("rtsp://freja.hiof.no:1935/rtplive/definst/hessdalen03.stream", 1, db, size=(1280, 720), display=True)
    # cam = Camera("http://wmccpinetop.axiscam.net/mjpg/video.mjpg", 1, db, size=(1280, 720), display=True)
    # cam = Camera("http://158.58.130.148:80/mjpg/video.mjpg", 1, db, size=(1280, 720), display=True)
    room_ids = db.getRooms()
    cams = list()
    for room_id in room_ids:
        print(room_id)
        cams.append(Camera(0, room_id[0], db, size=(1280, 720), display=True))
    for cam in cams:
        cam.releaseCamera()
    db.closeConnection()
