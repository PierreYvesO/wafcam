import mysql.connector
from datetime import datetime
config = {
    'user': 'scott',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'employees',
    'raise_on_warnings': True
}


class Database:
    def __init__(self):
        self.db = mysql.connector.connect(**config)

    def closeConnection(self):
        self.db.close()

    def addLog(self, type, number, camera_id):
        cursor = self.db.cursor()
        sql_insert = ("INSERT INTO log "
                       "(animal_type, amount, camera_id, date"
                       "VALUES (%s, %s, %s, %s, %s)")
        sql_data = (type, number, camera_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        cursor.execute(sql_insert, sql_data)
        self.db.commit()
        cursor.close()
