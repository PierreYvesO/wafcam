import fbchat

PY_UID = 1479027867

class Notification:
    def __init__(self):
        self.client = fbchat.Client("oupindrin.pierrey@outlook.com", "PatCam60")
    def send_notification(self, text):
        mess = fbchat.Message(text=text)
        self.client.send(mess, PY_UID)