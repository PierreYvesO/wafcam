import unittest
from python_back.src.database import Database

"""For those test you need a working database already setup"""

test_config = {
    'user': 'waf',
    'password': 'cam',
    'host': '127.0.0.1',
    'database': 'wafcam',
    'raise_on_warnings': True
}


class DatabaseTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database(test_config)

    def test_get_forbidden_areas(self):
        forbiddens = self.db.getForbiddenAreas()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
