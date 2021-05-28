import python_back.src.database as db
from python_back.src.notification import Notification


class Analysis:
    def __init__(self, config=None, refresh=3600):
        self.notification = Notification()
        self.notification.send_notification("PATCAM est lancé!")
        self.refresh = refresh
        self.database = db.Database(config)
        self.entities = dict()
        db_entitites = self.database.getEntities()
        self.entities = {str(entity[0]): entity[1] for entity in db_entitites}
        self.isEmpty = True

    def start_analysis(self, refresh=3600):
        self.refresh = refresh
        text = "INFOS PATCAM:\n"
        temp_text = self.anaylisis_areas()
        temp_text += self.analysis_appearances()
        if self.isEmpty:
            temp_text = "Rien à signaler!"

        self.notification.send_notification(text + temp_text)
        self.isEmpty = True

    def anaylisis_areas(self):
        text = ""
        for entity_id in self.entities:
            result = self.database.getAreasFromLogByAnimalID(self.refresh, entity_id)
            if len(result) > 0:
                self.isEmpty = False
                text += f"Votre {self.entities[entity_id]} a été recemment proche de " \
                        f"{', '.join([f'{res[0]} ({res[1]})' for res in result])}\n"
            else:
                text += f"Votre {self.entities[entity_id]} n'a été detecté près d'aucune zone recemment!\n"
        return text

    def analysis_appearances(self):
        text = ""
        for entity_id in self.entities:
            result = self.database.getRoomsFromLogByAnimalID(self.refresh, entity_id)
            hours = int(self.refresh / 3600)
            hour_text = "heure"
            if hours >= 2:
                hour_text = "heures"
            if len(result) > 0:
                self.isEmpty = False
                text = f"En {hours} {hour_text}, votre {self.entities[entity_id]} est passé par " \
                       f"{', '.join([res[0] for res in result])}\n"
            else:
                text += f"En {hours} {hour_text}, aucun {self.entities[entity_id]} (Drataet) ne semble pas avoir été " \
                        f"détecté!\n"

        return text

    def __del__(self):
        self.notification.send_notification("PATCAM est terminé")
