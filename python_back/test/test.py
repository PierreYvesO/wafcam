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
    cam = Camera("http://192.168.1.71:8080/stream.mjpeg", 1, db, size=(1280, 720), display=True)
    cam.displayCamera()
    cam.releaseCamera()
    db.closeConnection()
