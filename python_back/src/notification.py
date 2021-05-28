import fbchat

PY_UID = 1479027867

def test():
    client = fbchat.Client("oupindrin.pierrey@outlook.com", "PatCam60")
    mess = fbchat.Message(text="test")
    client.send(mess, PY_UID)


if __name__ == '__main__':
    test()
