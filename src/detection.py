import time
import cv2
import numpy as np

LIMITE_CONF = 0.6  # limite de confiance de detection
LIMITE_CONF_NMS = 0.2  # limite de confiance pour l'algo NMS


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
        cv2.rectangle(img, (x, y), (x + w, h + y), color=color, thickness=2)
        cv2.putText(img, className + "{:.2f}% ".format(confidence),
                    (box[0] + 10, box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


class Detection:
    def __init__(self, video_path=0, size=(1280, 720), display=False):
        """
        Initialise un flux video ou la detection sera fait
        :param video_path: 0=(webcam), port@ip (camera ip)
        :param size: taille de l'image rentrante
        :param display: afficher un visuel opencv de la camera (debug)
        """
        # Parametres capture video
        self.cap = cv2.VideoCapture(video_path)
        self.cap.set(3, size[0])
        self.cap.set(4, size[1])
        self.cap.set(10, 150)

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

    def start(self):
        """
        Lance la lecture du flux video et de la detection des objets
        :return:
        """
        success, img = self.cap.read()  # Lecture de la 1ere frame
        if not success:
            raise Exception("Impossible d'ouvrir le flux video donné")

        classDetected = {}  # Liste des objects detecté dans la scene pendant 1s
        while success:
            detected = list()  # liste des objets detectes
            classIds, confs, bbox = self.net.detect(img, confThreshold=LIMITE_CONF)  # detection des objets
            bbox = list(bbox)  # liste des postions
            confs = list(np.array(confs).reshape(1, -1)[0])
            confs = list(map(float, confs))  # liste des degrés de confiance

            # Pour eviter le chevauchement des detections d'objet et eviter les doublons, on applique un algorithme NMS
            # (Non-Maximum Suppression) qui va essayer de creer une detection commune d'un meme objet
            indices = cv2.dnn.NMSBoxes(bbox, confs, LIMITE_CONF, LIMITE_CONF_NMS)

            # grace au NMS, la position d'un objet detecté est plsu stable, on peut odnc essayer de voir si l'objet
            # detecté a deja ete trouvé dans une frame precedente ou c'est un nouveau
            isNew = True

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
                for detect in classDetected[className]:
                    old_box = detect[0]
                    old_x, old_y, old_w, old_h = old_box[0], old_box[1], old_box[2], old_box[3]
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    offset_max = 20
                    if abs(old_x - x) < offset_max and abs(old_y - y) < offset_max and \
                            abs((old_w + old_x) - (w + x)) < offset_max and abs((old_h + old_y) - (h + y)) < offset_max:
                        classDetected[className].remove(detect)
                        isNew = False
                if not isNew:
                    color = (255, 0, 0)  # Bleu si l'objet est deja connu
                else:
                    color = (0, 255, 0)  # Vert so c'est un nouvel objet
                # Ajout du nouvel element detecté dans la liste
                classDetected[className].append((box.tolist(), time.time()))
                # ajout a la liste des objets detectés dans la frame
                detected.append((box, className, confs[i] * 100, color))

            # Dna sle cas de faux positifs, la detection est en general tres succinte, pour palier a ce probleme et
            # eviter que ces erreurs de detection influe sur les resultats de la detection, on supprime les objets
            # detectes il y a plus d'1 seconde et on supprime la cle du dictionnaire si besoin.
            toDelete = list()
            for className in classDetected:
                for detect in classDetected[className]:
                    if time.time() - detect[1] > 1:
                        print(className, "removed due to disapearance")
                        classDetected[className].remove(detect)
                        if len(classDetected[className]) == 0:
                            print("No more", className)
                            toDelete.append(className)
            for className in toDelete:
                del classDetected[className]

            # pour debug
            if self.display:
                # Affiche les rectangles
                display_detected(img, detected)
                # Affichage console des objets presents dans la scene
                for detect in classDetected:
                    print(detect, ":", len(classDetected[detect]))
                    # print(classDetected["person"])
                # Affiche l'image sur ecran
                cv2.imshow("Output", img)
                cv2.waitKey(1)
                success, img = self.cap.read()

            self.send_infos()

    def send_infos(self):
        # TODO Envoi les infos vers la BDD/front
        pass


if __name__ == '__main__':
    detection = Detection(display=True)
    detection.start()
