from simple_websocket_server import WebSocketServer

from python_back.src import database_utils
from python_back.src.wafcam_websocket import WafcamSocket, launch, send_update_ws


def init_project():
    db_config = database_utils.read_env()
    server = WebSocketServer('localhost', 8000, WafcamSocket, select_interval=None)
    launch(db_config, server)
    send_update_ws()
    server.serve_forever()


if __name__ == '__main__':
    init_project()
