import unittest

from python_back.src.notification import Notification


class MyTestCase(unittest.TestCase):
    def test_basic_send(self):
        notif = Notification()
        notif.send_notification("test")


if __name__ == '__main__':
    unittest.main()
