from simple_websocket_server import WebSocketServer

from python_back.src.wafcam_websocket import WafcamSocket, launch, send_update_ws

test_config = {
    'user': 'waf',
    'password': 'cam',
    'host': '127.0.0.1',
    'database': 'wafcam',
    'raise_on_warnings': True
}
def init_project():
    server = WebSocketServer('localhost', 8000, WafcamSocket, select_interval=None)
    launch(test_config, server)
    server.serve_forever()




if __name__ == '__main__':
    init_project()
