from simple_websocket_server import WebSocketServer

from python_back.src import database_utils
from python_back.src.wafcam_websocket import WafcamSocket, launch

def init_project():
    db_config = database_utils.read_env()
    server = WebSocketServer('localhost', 8000, WafcamSocket, select_interval=None)
    launch(db_config, server)
    server.serve_forever()


if __name__ == '__main__':
    init_project()
