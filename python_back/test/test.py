from simple_websocket_server import WebSocketServer

from python_back.src.wafcam_websocket import Wafcam


def init_project():
    server = WebSocketServer('localhost', 8000, Wafcam, select_interval=None)
    server.serve_forever()


if __name__ == '__main__':
    init_project()
