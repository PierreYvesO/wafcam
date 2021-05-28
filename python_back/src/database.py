from datetime import datetime

import mysql.connector
from python_back.src.database_utils import config as prod_config, isDatabaseSet, read_env

LOG_TABLE = ("log", ["id_camera", "id_animal", "number", "id_area", "timestamp"])
ROOM_FROM_LOG_ANIMAL_TABLE = ("room", ["room.name"])
AREA_FROM_LOG_ANIMAL_TABLE = ("area, room, camera", ["area.name, room.name"])
ENTITY_TABLE = ("animal", ["*"])
ROOM_TABLE = ("room", ["id_room", "name"])
FORBIDDEN_TABLE = ("area", ["*"])
CAMERA_TABLE = ("camera", ["id_camera", "ip_adress", "user", "password"])


class Database:
    def __init__(self, user_config=None):
        if user_config is None:
            if isDatabaseSet:
                self.db = mysql.connector.connect(**prod_config)
            else:
                self.db = mysql.connector.connect(read_env())
        else:
            self.db = mysql.connector.connect(**user_config)
        self.processing = False

    def closeConnection(self):
        self.wait_available()
        self.db.close()

    def addLog(self, animal, number, camera_id, id_forbidden_area, timestamp):
        self.wait_available()
        self.processing = True
        cursor = self.db.cursor(prepared=True)
        sql_insert = "INSERT INTO  `{0}`" \
                     "({1})" \
                     "VALUES (%s, %s, %s, %s, %s)".format(LOG_TABLE[0], ",".join(LOG_TABLE[1]))
        sql_data = (camera_id, animal, number, id_forbidden_area, timestamp)
        cursor.execute(sql_insert, sql_data)
        self.db.commit()
        cursor.close()
        self.processing = False

    def getLogs(self, time_elapsed):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        condition = f"TIMESTAMPDIFF(SECOND, timestamp, '{timestamp}') < {time_elapsed}"
        return self.buildSelect(LOG_TABLE, condition)

    def getRoomsFromLogByAnimalID(self, time_elapsed, animal_id):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        condition = "room.id_room IN (SELECT log.id_camera " \
                    "FROM `log` " \
                    f"WHERE TIMESTAMPDIFF(SECOND, log.timestamp, '{timestamp}') < {time_elapsed} " \
                    f"AND log.id_animal='{animal_id}' " \
                    f"AND log.number is NOT NULL " \
                    "GROUP BY log.id_camera)"
        return self.buildSelect(ROOM_FROM_LOG_ANIMAL_TABLE, simpleCondition=condition)

    def getAreasFromLogByAnimalID(self, time_elapsed, animal_id):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        condition = "area.id_area IN (SELECT log.id_area " \
                    "FROM `log` " \
                    f"WHERE TIMESTAMPDIFF(SECOND, log.timestamp, '{timestamp}') < {time_elapsed} " \
                    f"AND log.id_animal='{animal_id}' " \
                    f"AND log.id_area is NOT NULL " \
                    "GROUP BY log.id_camera)" \
                    "and camera.id_camera=area.id_camera and room.id_room=camera.id_room"
        return self.buildSelect(AREA_FROM_LOG_ANIMAL_TABLE, simpleCondition=condition)

    def addDetectedAnimalLog(self, animal, number, camera_id, timestamp):
        self.addLog(animal, number, camera_id, None, timestamp)

    def addDetectedInForbiddenAreaLog(self, animal, id_forbidden_area, camera_id, timestamp):
        self.addLog(animal, None, camera_id, id_forbidden_area, timestamp)

    def buildSelect(self, table, simpleCondition=None):
        self.wait_available()
        self.processing = True
        cursor = self.db.cursor(prepared=True)
        sql_request = "SELECT {1} FROM {0}".format(table[0], ",".join(table[1]))
        if simpleCondition is not None:
            sql_request += f" WHERE {simpleCondition}"
        cursor.execute(sql_request)
        res = cursor.fetchall()
        cursor.close()
        self.processing = False
        return res

    def getEntities(self):
        return self.buildSelect(ENTITY_TABLE)

    def getRooms(self):
        return self.buildSelect(ROOM_TABLE)

    def getCameras(self):
        return self.buildSelect(CAMERA_TABLE)

    def getCamerasFromID(self, cam_id):
        return self.buildSelect(CAMERA_TABLE, f"idcamera={cam_id}")

    def getForbiddenAreas(self):
        return self.buildSelect(FORBIDDEN_TABLE)

    def getCameraFromRoomWithID(self, id_room: int):
        self.wait_available()
        self.processing = True
        cursor = self.db.cursor(prepared=True)
        cursor.execute("SELECT `{1}`,`{2}`,`{3}` FROM {0} WHERE id_room={4}".format(*CAMERA_TABLE, id_room))
        res = cursor.fetchall()
        cursor.close()
        self.processing = False
        return res

    def wait_available(self):
        while self.processing:
            pass

    def getRoomFromCameraID(self, cam_id):
        self.buildSelect(ROOM_TABLE, f"id_room={cam_id}")
