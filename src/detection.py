import time
import cv2
import numpy as np
import math

LIMITE_CONF = 0.6  # limite de confiance de detection
LIMITE_CONF_NMS = 0.3  # limite de confiance pour l'algo NMS
TRACKING_OFFSET = 80
TIME_LIMIT = 1
FRAME_TIMER = .2


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


class Detection:
    def __init__(self, camera, display=False):
        """
        Initialise un flux video ou la detection sera fait
        :param capture: feed to read on
        :param size: taille de l'image rentrante
        :param display: afficher un visuel opencv de la camera (debug)
        """
        self.cam = camera

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

        self.lastInfos = (0, 0)
        self.isOn = False

    def start(self):
        """
        Lance la lecture du flux video et de la detection des objets
        :return: None (potential infinite loop)
        """

        # test d'une lecture de premiereframe
        sucess, _ = self.cam.getFrame()
        if not sucess:
            raise Exception("Impossible d'ouvrir le flux video donné")
        detected = list()  # liste des objets detectes
        start_time = time.time()
        classDetected = {}  # Liste des objects detecté dans la scene pendant 1s
        while sucess and self.isOn:
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

                    if className not in classDetected:
                        classDetected[className] = list()

                    # Verifie si l'objet trouvé etait deja présent dans les frame precedentes
                    # isNew est marqué False et l'objet est supprimé de la liste
                    # la verification se fait par position des 4 coins
                    new_center = get_rect_center(box[0], box[1], box[2], box[3])
                    objectIndice, objectDist = self.tracked_object(new_center, classDetected[className])

                    if objectDist < TRACKING_OFFSET and objectIndice != 1:
                        del classDetected[className][objectIndice]
                        isNew = False
                    if not isNew:
                        color = (255, 0, 0)  # Bleu si l'objet est deja connu
                    else:
                        color = (0, 255, 0)  # Vert so c'est un nouvel objet
                    # Ajout du nouvel element detecté dans la liste
                    temp_detected.append((className, (new_center, time.time())))

                    # ajout a la liste des objets detectés dans la frame
                    detected.append((box, className, confs[i] * 100, color))
                for elmt in temp_detected:
                    classDetected[elmt[0]].append(elmt[1])

                # Dans le cas de faux positifs, la detection est en general tres succinte, pour palier a ce probleme et
                # eviter que ces erreurs de detection influe sur les resultats de la detection, on supprime les objets
                # detectes il y a plus d'1 seconde et on supprime la cle du dictionnaire si besoin.
                toDelete = list()
                for className in classDetected:
                    for detect in classDetected[className]:
                        if time.time() - detect[1] > TIME_LIMIT:
                            classDetected[className].remove(detect)
                            if len(classDetected[className]) == 0:
                                toDelete.append(className)
                self.remove_similar_centers(classDetected)
                for className in toDelete:
                    del classDetected[className]
            # pour debug
            if self.display:
                # Affiche les rectangles
                display_detected(img, detected)

                # Affichage console des objets presents dans la scene
                # for detect in classDetected:
                #     print(detect, ":", len(classDetected[detect]))
                # Affiche l'image sur ecran
                cv2.imshow("Output", img)
                cv2.waitKey(1)

            self.send_infos(classDetected)

    def send_infos(self, classDetected):
        if "dog" in classDetected:
            dogs = len(classDetected["dog"])
        else:
            dogs = 0
        if "cat" in classDetected:
            cats = len(classDetected["cat"])
        else:
            cats = 0
        output = ""
        if self.lastInfos[0] < dogs:
            output += "dog in\n"
        if self.lastInfos[0] > dogs:
            output += "dog out\n"
        if self.lastInfos[1] < cats:
            output += "cat in\n"
        if self.lastInfos[1] > cats:
            output += "cat out\n"
        if len(output) > 0:
            self.lastInfos = (dogs, cats)
            print(output)
        # TODO: Envoi les infos vers la BDD/front?
        pass

    def get_last_infos(self):
        return self.lastInfos

    def tracked_object(self, new_center, detectedObjects):
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

    def remove_similar_centers(self, classDetected):
        for detected in classDetected:
            points = [elmt[0] for elmt in classDetected[detected]]
            md = 20  # max distance allowed between two points
            points.sort()
            to_remove = set()  # keep track of items to be removed

            for i, point in enumerate(points):
                if i == len(points) - 1:
                    break
                other_point = points[i + 1]
                if abs(point[0] - other_point[0]) <= md and abs(point[1] - other_point[1]) <= md:
                    to_remove.add(i)

            for point in to_remove:
                del classDetected[detected][point]

    def stop_detection(self):
        self.isOn = False


if __name__ == '__main__':
    from camera import Camera
    cam = Camera("http://192.168.1.71:8080/stream.mjpeg", size=(1280, 70))
    detection = Detection(cam, display=True)
    detection.start()

