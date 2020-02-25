import sqlite3
import sys
import threading
import webbrowser

import cv2
import nfc
import pyautogui as pyautogui
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from gtts import gTTS
from playsound import playsound

IDRFID: str
IDUSER: int


def fn_activarNotas(address):
    print("LIBRO:dirección del objeto: ", address)
    long = ""
    with open(address, "r", encoding="UTF-8") as file:
        text = file.readlines()
    for row in text:
        long = long + row

    file = gTTS(text=long, lang="ES")
    filename = "salida.mp3"
    file.save(filename)
    playsound(filename)


def fn_activarVideo(address):
    print("VIDEO:dirección del objeto: ", address)
    cap = cv2.VideoCapture(address)
    window_name = "window"
    interframe_wait_ms = 30
    if not cap.isOpened():
        exit()
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while (True):
        ret, frame = cap.read()
        if ret:
            cv2.imshow(window_name, frame)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def fn_skypeCallProcess(address):
    uri = 'skype:' + address

    webbrowser.open(uri, new=2)
    pyautogui.sleep(5)
    pyautogui.click(700, 550)
    pyautogui.click(700, 505)


def listen():
    print(threading.currentThread().getName(), 'Lanzado')

    clf = nfc.ContactlessFrontend()
    if not clf.open('usb'):
        raise RuntimeError("Failed to open NFC device.")

    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    tag_id = str(tag).split('ID=')[1]

    connection = sqlite3.connect("database.db")
    result = connection.execute("SELECT card,branch,address FROM task")
    result = result.fetchall()
    for row_number, row_data in enumerate(result):
        if (row_data[0] == tag_id):
            address = (row_data[2])
            if (row_data[1] == 'Documento'):
                fn_activarNotas(address)
            if (row_data[1] == "Video"):
                fn_activarVideo(address)
            if (row_data[1] == "Videollamada"):
                fn_skypeCallProcess(address)
            if (row_data[1] == "Imágen"):
                fn_activarVideo(address)

    connection.close()

    print(threading.currentThread().getName(), 'Deteniendo')


class TaskMate(QWidget):
    def __init__(self):
        super().__init__()
        # titulo ventana
        self.setWindowTitle("--TaskMate--")
        # Mensaje principal
        self.title = QLabel("Acerque tarjeta a lector")
        self.title.setAlignment(Qt.AlignCenter)
        font = self.title.font()
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setStyleSheet("background-color: black;""font-size: 25px; color: #A0184B;")
        # Imagen = Logo
        self.pixmap = QPixmap("icon/logo.png")
        self.label = QLabel()
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        # Layout con Items
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.setGeometry(250, 50, 800, 200)
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskMate()

    QCoreApplication.processEvents()
    listen()

    sys.exit(app.exec_())
