from _queue import Empty
from simple_websocket_server import WebSocket, WebSocketServer
from multiprocessing import Process, Queue

from python_back.src.database import Database
from python_back.src.camera import Camera

clients = []
cams = dict()
queues = dict()
ws_queue: Queue = Queue()
global server, config


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
    Démarre les objets caméras
    :param database_config: identifiants de connexion à la bdd
    :param serv: serveur websocket en cours d'execution
    """
    global cams, queues, server, config
    if serv is not None:
        server = serv
    config = database_config
    db = Database(database_config)

    cameras = db.getCameras()
    for cam_id, camera_ip, user, pwd in cameras:
        queue = Queue()

        p = Process(target=Camera, args=(queue, camera_ip, cam_id, ws_queue, (1280, 720), True, user, pwd))
        p.start()
        queues[cam_id] = queue
        cams[cam_id] = p
    db.closeConnection()

    send_update_ws()


def reload(value: int = None, delete=False):
    """
    Recharge les objets caméras
    """
    global cams, queues
    if value is None:
        print("reloaded !")
        for i, cam in cams:
            queues[i].put("stop")
            cam.join()
            queues[i].close()

        cams = list()
        queues = list()
        launch(server)
    else:
        queues[value].put("stop")
        cams[value].join()
        queues[value].close()
        if delete:
            del cams[value]
            del queues[value]
        else:
            db = Database(config)
            cam_id, camera_ip, user, pwd = db.getCamerasFromID(value)
            queue = Queue()

            p = Process(target=Camera, args=(queue, camera_ip, cam_id, ws_queue, (1280, 720), True, user, pwd))
            p.start()
            queues[cam_id] = queue
            cams[cam_id] = p
            db.closeConnection()



@cam.threaded
def send_update_ws():
    """
    Récupère les données envoyés par les caméras pour le websocket
    :return:
    """
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
    """
    Envoi un signal au clients que de nouvelles données sont disponibles dans la bdd
    :param type_log: type de log ajouté
    """
    global clients
    for client in clients:
        client.send_message(type_log)
    server.handle_request()
