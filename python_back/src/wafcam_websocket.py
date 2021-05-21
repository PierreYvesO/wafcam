from _queue import Empty
from simple_websocket_server import WebSocket, WebSocketServer
from multiprocessing import Process, Queue

from python_back.src.database import Database
import python_back.src.camera as cam

clients = []
cams = list()
queues = list()
ws_queue: Queue = Queue()
global server


class WafcamSocket(WebSocket):
    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)

    def handle(self):
        if self.data == 'reload':
            reload()

    def connected(self):
        global clients
        print(self.address, 'connected')
        clients.append(self)

    def handle_close(self):
        global clients
        print(self.address, 'closed')
        clients.remove(self)


def launch(database_config, serv: WebSocketServer = None):
    """
    Démarre
    :param serv: Websocket server that is running
    :return:
    """
    global cams, queues, server
    if serv is not None:
        server = serv
    db = Database(database_config)

    cameras = db.getCameras()
    for cam_id, camera_ip, user, pwd in cameras:
        queue = Queue()

        p = Process(target=cam.Camera, args=(queue, camera_ip, cam_id, ws_queue, (1280, 720), True, user, pwd))
        p.start()
        queues.append(queue)
        cams.append(p)
    db.closeConnection()

    send_update_ws()


def reload():
    global cams, queues
    print("reloaded !")
    for i, cam in enumerate(cams):
        queues[i].put("stop")
        cam.join()
        queues[i].close()

    cams = list()
    queues = list()
    launch(server)


@cam.threaded
def send_update_ws():
    res = {}
    while True:
        try:
            res = ws_queue.get(timeout=2)
        except Empty:
            if len(res) > 0:
                send_update(res)
                print(res)

            res = {}


def send_update(type_log):
    global clients
    for client in clients:
        client.send_message(type_log)
    server.handle_request()
