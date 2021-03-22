import mysql.connector
from python_back.src.database_utils import config as prod_config

LOG_TABLE = ("room_entities", "room_id", "entity_id", "amount_entities", "time_record")
ENTITY_TABLE = ("entity", "*")
ROOM_TABLE = ("room", "*")
FORBIDDEN_TABLE = ("forbidden_area", "*")
CAMERA_TABLE = ("camera", "ip")


class Database:
    def __init__(self, user_config=None):
        if user_config is None:
            self.db = mysql.connector.connect(**prod_config)
        else:
            self.db = mysql.connector.connect(**user_config)
        self.processing = False

    def closeConnection(self):
        self.wait_available()
        self.processing = True
        self.db.close()

    def addLog(self, animal, number, camera_id, timestamp):
        self.wait_available()
        self.processing = True
        cursor = self.db.cursor(prepared=True)
        sql_insert = "INSERT INTO  `{0}`" \
                     "({1}, {2}, {3}, {4}) " \
                     "VALUES (%s, %s, %s, %s)".format(*LOG_TABLE)
        sql_data = (camera_id, animal, number, timestamp)
        cursor.execute(sql_insert, sql_data)
        self.db.commit()
        cursor.close()
        self.processing = False

    def buildSelect(self, table):
        self.wait_available()
        self.processing = True
        cursor = self.db.cursor(prepared=True)
        cursor.execute("SELECT {1} FROM {0}".format(*table))
        res = cursor.fetchall()
        cursor.close()
        self.processing = False
        return res

    def getEntities(self):
        return self.buildSelect(*ENTITY_TABLE)

    def getRooms(self):
        return self.buildSelect(*ROOM_TABLE)

    def getForbiddenAreas(self):
        return self.buildSelect(*FORBIDDEN_TABLE)

    def getCameraWithID(self, id_camera: int):
        self.wait_available()
        self.processing = True
        cursor = self.db.cursor(prepared=True)
        cursor.execute("SELECT {1} FROM {0} WHERE id={2}".format(*CAMERA_TABLE), id)
        res = cursor.fetchall()
        cursor.close()
        self.processing = False
        return res


    def wait_available(self):
        while self.processing:
            pass
