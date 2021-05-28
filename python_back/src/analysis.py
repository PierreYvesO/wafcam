import python_back.src.database as db
from python_back.src.utils import threaded

class Analysis:
    def __init__(self, config=None):
        self.database = db.Database(config)
        logs = self.database.getLogs(43200)  # 12 heures
        logs_dict = [dict(zip(db.LOG_TABLE[1], log)) for log in logs]
        self.appear_list = list()
        self.area_list = list()

        for log in logs_dict:
            if log['id_area'] is not None:
                self.area_list.append(log)
            if log['number'] is not None:
                self.appear_list.append(log)

    @threaded
    def anaylisis_areas(self):
        pass

    @threaded
    def analysis_appearances(self):
        pass



    def __del__(self):
        self.database.closeConnection()
