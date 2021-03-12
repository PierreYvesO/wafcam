from python_back.src.camera import Camera

if __name__ == '__main__':
    cam = Camera("http://192.168.1.71:8080/stream.mjpeg", 1, size=(1280, 720), display=True)
    cam.displayCamera()
    cam.releaseCamera()
