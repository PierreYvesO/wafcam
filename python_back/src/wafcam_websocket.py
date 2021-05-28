import time
from _queue import Empty
from simple_websocket_server import WebSocket, WebSocketServer
from multiprocessing import Process, Queue

from python_back.src.analysis import Analysis
from python_back.src.database import Database
from python_back.src.camera import Camera
from python_back.src.utils import threaded

clients = []
cams = dict()
queues = dict()
ws_queue: Queue = Queue()
global server, config


class WafcamSocket(WebSocket):
    def __init__(self, ws_server, sock, address):
        super().__init__(ws_server, sock, address)

    def handle(self):
        elmt, value = self.data.split(' ')
        if elmt.startswith('cam'):
            list_values = value.split(',')
            delete = False
            if 'del' in elmt:
                delete = True
            reload(list_values, delete=delete)
            pass
        elif elmt.startswith("area"):
            reload(value, False)
            pass

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
    launch_analysis(database_config)


@threaded
def launch_analysis(database_config):
    analysis = Analysis(config=database_config)
    while True:
        time.sleep(3600)
        analysis.start_analysis()


def reload(values, delete):
    """
    Recharge les objets caméras
    """
    global cams, queues
    db = Database(config)
    for value in values:
        # Stop Process
        queues[value].put("stop")
        cams[value].join()
        queues[value].close()

        # Delete Value from list
        if delete:
            del cams[value]
            del queues[value]
        else:

            cam_id, camera_ip, user, pwd = db.getCamerasFromID(value)

            queue = Queue()

            p = Process(target=Camera, args=(queue, camera_ip, cam_id, ws_queue, (1280, 720), True, user, pwd))
            p.start()
            queues[cam_id] = queue
            cams[cam_id] = p
    db.closeConnection()


@threaded
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
