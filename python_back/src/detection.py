import time
from threading import Thread

import cv2
import numpy as np
import math

LIMITE_CONF = 0.3  # limite de confiance de detection
LIMITE_CONF_NMS = .1  # limite de confiance pour l'algo NMS
TRACKING_OFFSET = 100
TIME_LIMIT = 2
FRAME_TIMER = .2
SIMILAR_THRESHOLD = 5
INTER_THRESHOLD = .25
DISPLAYED = ["cat", "dog"]


def display_detected(img, detected):
    """
    Affiche les rectangles des objets detectés
    :param img: image dans laquelle afficher les rectangles
    :param detected: liste des rectangles a afficher
    :return: None
    """
    for elmt in detected:
        box = elmt[0]
        className = elmt[1]
        confidence = elmt[2]
        color = elmt[3]

        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.circle(img, get_rect_center(x, y, w, h), radius=20, color=(0, 0, 255), thickness=2)
        cv2.rectangle(img, (x, y), (x + w, h + y), color=color, thickness=2)
        cv2.putText(img, className + "{:.2f}% ".format(confidence),
                    (box[0] + 10, box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


def get_rect_center(x, y, w, h):
    """
    Get the center of a rectangle in px point
    """
    centerX = int(x + w / 2)
    centerY = int(y + h / 2)
    return centerX, centerY


def remove_similar_centers(classDetected):
    """
    Detecte les elements similaires d'une classe et les fusionne
    :param classDetected: dictionnaire classname : elmts
    """
    for detected in classDetected:
        # list.sort() compare uniquement le 1er element d'une liste pour trier.
        # On peut donc utiliser pour trier seuelement par la position en ignorant le 2eme element.
        classDetected[detected].sort()
        points = [elmt[0] for elmt in classDetected[detected]]
        # points.sort()

        j = 0
        while j < len(points) - 1:
            points = [elmt[0] for elmt in classDetected[detected]]
            points.sort()
            indexes = set()
            i = j
            to_merge = set()
            while i < len(points) - 1 and similar_point(points[i], points[i + 1]):
                indexes.add(i)
                indexes.add(i + 1)
                to_merge.add(points[i])
                to_merge.add(points[i + 1])
                i += 1
            if len(indexes) > 0:
                for i in range(len(indexes)):
                    del classDetected[detected][0]

                average = [round(sum(x) / len(x)) for x in zip(*to_merge)]
                classDetected[detected].append((tuple(average), time.time()))
                classDetected[detected].sort()
                j = 0
            else:
                j += 1


def similar_point(p1, p2):
    return abs(p1[0] - p2[0]) <= SIMILAR_THRESHOLD and abs(p1[1] - p2[1]) <= SIMILAR_THRESHOLD


def is_in_areas(objectBox, forbiddenAreas, triggeredAreas):
    """
    Test qu'un element est forme une intersection de plus de INTER_THRESHOLD % avec toutes les zones données
    Une zone interdite qui est comprise dans le rectangle objectBox renvoi True directement
    Si plusieurs zones données se chevauchent l'intersection contera double
    @param objectBox: rectangle a tester
    @param forbiddenBoxes: zones données
    @return: True si l'aire du rectangel a tester et couvert a plus de INTER_THRESHOLD %
    """
    totalArea = 0
    for forbiddenArea in forbiddenAreas:
        forbiddenBox = forbiddenArea[3:] # Take only the 4 rect infos (x y w h)

        intersect = intersection_area(objectBox, forbiddenBox)
        # Ajoute l'id de la zone à la liste s'il y a collision
        if intersect > 0:
            triggeredAreas.append((intersect, forbiddenArea[0]))
        totalArea += intersect
    objectArea = objectBox[2] * objectBox[3]
    if totalArea > 0 and (totalArea > objectArea or totalArea / objectArea >= INTER_THRESHOLD):
        return True
    else:
        return False


def intersection_area(boxA, boxB):
    xA, yA, wA, hA = boxA
    xB, yB, wB, hB = boxB
    if xA <= xB and yA >= yB and wA >= wB and yA >= yB:
        return wA * hA
    x1 = max(min(xA, xA + wA), min(xB, xB + wB))
    y1 = max(min(yA, yA + hA), min(yB, yB + hB))
    x2 = min(max(xA, xA + wA), max(xB, xB + wB))
    y2 = min(max(yA, yA + hA), max(yB, yB + hB))

    return (x2 - x1) * (y2 - y1) if x1 < x2 and y1 < y2 else 0


def tracked_object(new_center, detectedObjects):
    """
    Recupere le potentiel objet detecté precedemment qui correspond à l'objet detecté actuellement.
    Cela permet de suivre un objet sans l'identifier comme nouveau
    :param new_center: centre de l'objet nouvelement detecté
    :param detectedObjects: liste des objets de la meme className dans el buffer d'objet detecté
    :return: index de l'objet correspondant dans le buffer et distance entre les 2 centres
    """
    minIndex = -1
    minDist = 99999
    for i in range(0, len(detectedObjects)):
        dist = math.dist(new_center, detectedObjects[i][0])
        if dist < minDist:
            minDist = dist
            minIndex = i

    return minIndex, minDist


class Detection(Thread):
    def __init__(self, camera, state_queue, detection_result_queue, forbidden_area_queue, displayed=None, forbidden_areas=None, display=False):
        """
        Lance un Tread de detection sur un flux video donné.
        @param state_queue: queue de communication start/stop entre l'objet camera et detection
        @param camera: flux video donnée
        @param detection_result_queue: queue de communication retournant les resultats de la detection
        @param displayed: liste des object a detecter
        @param forbidden_areas: liste des zones rectangle ou la detection d'un objet de la list displayed doit rencoyer
                                une information
        @param display: (DEBUG) affichage de la detection en temps reel
        """
        super().__init__()
        if forbidden_areas is None:
            forbidden_areas = list()
        if displayed is None:
            displayed = DISPLAYED
        self.forbidden_areas = forbidden_areas
        self.queue = state_queue
        self.forbidden_areas_queue = forbidden_area_queue
        self.cam = camera
        self.result = detection_result_queue
        self.displayed = displayed
        self.displayMap = {}
        for elmt in displayed:
            self.displayMap[elmt[1]] = elmt[0]

        # Lecture de la liste des objets detetable
        self.classNames: list
        classFile = '../mobilenet_deploy/coco.names'
        with open(classFile, 'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')

        # Modele pour la reconnaissance
        configPath = '../mobilenet_deploy/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = '../mobilenet_deploy/frozen_inference_graph.pb'

        # configuration du module de reconnaissance
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)  # determiné a pertir du model pbtxt (dim size)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)  # opencv utilise un mode BGR donc il faut inverser le R et B

        self.display = display
        self.lastInfos = []
        self.lastTriggeredArea = 0
        self.lastTimeTriggeredArea = time.time()
        for _ in self.displayMap:
            self.lastInfos.append(0)

    def startProcess(self):
        self.run()

    def run(self):
        """
        Lance la lecture du flux video et de la detection des objets
        :return: None (potential infinite loop)
        """

        # test d'une lecture de premiereframe
        sucess, _ = self.cam.getFrame()
        if not sucess:
            raise Exception(f"Impossible d'ouvrir le flux video {0}".format(self.cam.ip))
        detected = list()  # liste des objets detectes
        start_time = time.time()
        classDetected = {}  # Liste des objects detecté dans la scene pendant 1s
        while sucess and self.queue.empty():
            sucess, img = self.cam.getFrame()
            if time.time() - start_time > FRAME_TIMER:
                detected = list()  # liste des objets detectes
                start_time = time.time()
                classIds, confs, bbox = self.net.detect(img, confThreshold=LIMITE_CONF)  # detection des objets
                bbox = list(bbox)  # liste des postions
                confs = list(np.array(confs).reshape(1, -1)[0])
                confs = list(map(float, confs))  # liste des degrés de confiance

                # Pour eviter le chevauchement des detections d'objet et eviter les doublons, on applique un
                # algorithme NMS (Non-Maximum Suppression) qui va essayer de creer une detection commune d'un meme
                # objet
                indices = cv2.dnn.NMSBoxes(bbox, confs, LIMITE_CONF, LIMITE_CONF_NMS)

                # grace au NMS, la position d'un objet detecté est plus stable, on peut odnc essayer de voir si l'objet
                # detecté a deja ete trouvé dans une frame precedente ou c'est un nouveau
                isNew = True

                temp_detected = list()
                # Parcours des objets trouves
                for idx in indices:
                    i = idx[0]
                    box = bbox[i]
                    className = self.classNames[classIds[i][0] - 1]
                    if className not in self.displayMap:
                        break
                    if className not in classDetected:
                        classDetected[className] = list()

                    # Verifie si l'objet trouvé etait deja présent dans les frame precedentes
                    # isNew est marqué False et l'objet est supprimé de la liste
                    # la verification se fait par position des 4 coins
                    new_center = get_rect_center(box[0], box[1], box[2], box[3])
                    objectIndice, objectDist = tracked_object(new_center, classDetected[className])

                    if objectDist < TRACKING_OFFSET and objectIndice != -1 and len(classDetected[className]) > 0:
                        del classDetected[className][objectIndice]
                        isNew = False
                    if not isNew:
                        color = (255, 0, 0)  # Bleu si l'objet est deja connu
                    else:
                        color = (0, 255, 0)  # Vert si c'est un nouvel objet
                    triggeredAreas = list()
                    # Verifie si l'animal est dans une ou plusieurs zone interdite
                    if is_in_areas(box, self.forbidden_areas, triggeredAreas):
                        triggeredAreas.sort()
                        if self.lastTriggeredArea != triggeredAreas[0] and self.lastTimeTriggeredArea - time.time() > 5:
                            # Envoie seuelement la zone ou l'animal est le plus dedans
                            self.forbidden_areas_queue.put(triggeredAreas[0])
                            # Evite la répétition d'envoi de log
                            self.lastTimeTriggeredArea = time.time()

                    # Ajout du nouvel element detecté dans la liste
                    temp_detected.append((className, (new_center, time.time())))

                    # ajout a la liste des objets detectés dans la frame
                    detected.append((box, className, confs[i] * 100, color))
                for elmt in temp_detected:
                    classDetected[elmt[0]].append(elmt[1])

                # Dans le cas de faux positifs, la detection est en general tres succinte, pour palier a ce probleme et
                # eviter que ces erreurs de detection influent sur les resultats de la detection, on supprime les objets
                # detectes il y a plus d'1 seconde et on supprime la cle du dictionnaire si besoin.
                toDelete = list()
                for className in classDetected:
                    for detect in classDetected[className]:
                        if time.time() - detect[1] > TIME_LIMIT:
                            classDetected[className].remove(detect)
                            if len(classDetected[className]) == 0:
                                toDelete.append(className)
                remove_similar_centers(classDetected)
                for className in toDelete:
                    del classDetected[className]
            # pour debug
            if self.display:
                # Affiche les rectangles
                display_detected(img, detected)
                cv2.imshow("Output", img)
                cv2.waitKey(1)

            self.send_infos(classDetected)

    def send_infos(self, classDetected):
        """
        Dtecte si des nouveaux chats/chiens ont été detectés ou ont disparu et stocke le compteur chat/chien
        :param classDetected:
        """
        animals = list()
        for i, animal in enumerate(self.displayMap):
            if animal in classDetected:
                animals.append(len(classDetected[animal]))
            else:
                animals.append(0)
        output = ""

        for i, animal in enumerate(animals):
            if self.lastInfos[i] < animals[i]:
                output += "{0} in\n".format(list(self.displayMap.keys())[i])
            if self.lastInfos[i] > animals[i]:
                output += "{0} out\n".format(list(self.displayMap.keys())[i])
        if len(output) > 0:
            for i, nb in enumerate(animals):
                self.lastInfos[i] = nb
            # print(output)
            # Envoie les infos vers la camera
            with self.result.mutex:
                self.result.queue.clear()

            animalDict = {}
            for i, animal in enumerate(self.displayMap):
                animalDict[str(self.displayMap[animal])] = self.lastInfos[i]
            self.result.put(animalDict)
