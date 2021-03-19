import mysql.connector
from python_back.src.database_utils import config as prod_config

LOG_TABLE = ("room_entities", "room_id", "entity_id", "amount_entities", "time_record")
ENTITY_TABLE = ("entity",)
ROOM_TABLE = ("id", "room",)


class Database:
    def __init__(self, user_config=None):
        if user_config is None:
            self.db = mysql.connector.connect(**prod_config)
        else:
            self.db = mysql.connector.connect(**user_config)

    def closeConnection(self):
        self.db.close()

    def addLog(self, animal, number, camera_id, timestamp):
        print(animal, number, camera_id, timestamp)
        cursor = self.db.cursor(prepared=True)
        sql_insert = "INSERT INTO  `{0}`" \
                     "({1}, {2}, {3}, {4}) " \
                     "VALUES (%s, %s, %s, %s)".format(*LOG_TABLE)
        sql_data = (camera_id, animal, number, timestamp)

        cursor.execute(sql_insert, sql_data)
        self.db.commit()
        cursor.close()

    def getEntities(self):
        cursor = self.db.cursor(prepared=True)
        cursor.execute("SELECT * FROM {0}".format(*ENTITY_TABLE))
        res = cursor.fetchall()
        cursor.close()
        return res

    def getRooms(self):
        cursor = self.db.cursor(prepared=True)
        cursor.execute("SELECT {0} FROM {1}".format(*ROOM_TABLE))
        res = cursor.fetchall()
        cursor.close()
        return res
