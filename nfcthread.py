import nfc
import sqlite3

from gtts import gTTS
from playsound import playsound


def listen():
    clf = nfc.ContactlessFrontend()
    if not clf.open('usb'):
        raise RuntimeError("Failed to open NFC device.")

    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    tag_id = str(tag).split('ID=')[1]

    connection = sqlite3.connect("database.db")
    global IDUSER
    result = connection.execute("SELECT card,branch,address FROM task WHERE idUser=?", (IDUSER))
    result = result.fetchall()
    for row_number, row_data in enumerate(result):
        if (row_data[0] == tag_id):
            if (row_data[1] == 'Documento'):
                address = (row_data[2])
    connection.close()
    string = 'bloc de notas activado'
    print(address)
    long = ""
    with open(address, "r", encoding="UTF-8") as file:
        text = file.readlines()
    for row in text:
        long = long + row

    file = gTTS(text=long, lang="ES")
    filename = "salida.mp3"
    file.save(filename)
    playsound(filename)
