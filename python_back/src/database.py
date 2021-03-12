import mysql.connector
from datetime import datetime
config = {
    'user': ' 2z2tz_admin',
    'password': 'PaTcAm78',
    'host': '2z2tz.myd.infomaniak.com',
    'database': '2z2tz_patcam_prod',
    'raise_on_warnings': True
}


class Database:
    def __init__(self, user_config=None):
        if user_config is None:
            self.db = mysql.connector.connect(**config)
        else:
            self.db = mysql.connector.connect(**user_config)

    def closeConnection(self):
        self.db.close()

    def addLog(self, type, number, camera_id, timestamp):
        cursor = self.db.cursor(prepared=True)
        sql_insert = ("INSERT INTO `log` "
                       "(room_id, entity_id, amount_entities, time_record)"
                       "VALUES (%s, %s, %s, %s)")
        sql_data = (camera_id, type, number, timestamp)

        cursor.execute(sql_insert, sql_data)
        self.db.commit()
        cursor.close()
