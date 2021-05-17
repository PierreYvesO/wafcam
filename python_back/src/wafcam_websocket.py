from simple_websocket_server import WebSocket

from python_back.src import database_utils
from python_back.src.camera import Camera
from python_back.src.database import Database
from multiprocessing import Process, Queue

test_config = {
    'user': 'waf',
    'password': 'cam',
    'host': '127.0.0.1',
    'database': 'wafcam',
    'raise_on_warnings': True
}


class Wafcam(WebSocket):
    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)
        self.clients = list()
        self.cams = list()
        self.queues = list()
        self.launch()

    def launch(self):
        db = Database(test_config)
        # db = Database(database_utils.read_env())
        room_ids = db.getRooms()

        for room_id in room_ids:
            room_id = room_id[0]
            queue = Queue()
            camera_ip, user, pwd = db.getCameraFromRoomWithID(room_id)[0]
            # camera_ip = 0
            p = Process(target=Camera, args=(queue, camera_ip, room_id, self, (1280, 720), True, user, pwd))
            p.start()
            self.queues.append(queue)
            self.cams.append(p)
        db.closeConnection()

    def reload(self):
        print("reloaded !")
        for i, cam in enumerate(self.cams):
            self.queues[i].put("stop")
            cam.join()

        self.cams = list()
        self.queues = list()
        self.launch()

    def handle(self):
        print("handling")
        print(self.data)
        if self.data == 'reload':
            self.reload()

    def send_update(self):
        for client in self.clients:
            client.send_message("log")

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')
