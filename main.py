import sqlite3
import sys
import threading

import cv2
import nfc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gtts import gTTS
from playsound import playsound

IDRFID: str
IDUSER: int


class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Añadir")

        self.setWindowTitle("Añadir Tarea")
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Nombre")
        layout.addWidget(self.nameinput)

        self.branchinput = QComboBox()
        self.branchinput.addItem("Música")
        self.branchinput.addItem("Video")
        self.branchinput.addItem("Imágen")
        self.branchinput.addItem("Documento")
        self.branchinput.addItem("Videollamada")
        layout.addWidget(self.branchinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Dirección")
        layout.addWidget(self.addressinput)

        self.QBtnFile = QPushButton()
        self.QBtnFile.setText("Seleccionar archivo")
        self.QBtnFile.clicked.connect(self.open_file)
        layout.addWidget(self.QBtnFile)

        self.QBtnFind = QPushButton()
        self.QBtnFind.setText("Leer tarjeta")
        self.QBtnFind.clicked.connect(self.getRfid)

        card = QLabel("Tarjeta:")
        self.cardinput = QLineEdit()

        layout.addWidget(card)
        layout.addWidget(self.cardinput)
        layout.addWidget(self.QBtnFind)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def getRfid(self):
        clf = nfc.ContactlessFrontend()
        if not clf.open('usb'):
            raise RuntimeError("Failed to open NFC device.")

        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        tag_id = str(tag).split('ID=')[1]
        self.cardinput.setText(str(tag_id))

    def addstudent(self):
        name = ""
        branch = ""
        address = ""

        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        address = self.addressinput.text()
        idCard = self.cardinput.text()
        global IDUSER
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO task (name,branch,address,card,idUser) VALUES (?,?,?,?,?)",
                           (name, branch, address, idCard, IDUSER))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Éxito', 'La tarea ha sido añadida con éxito a la base de datos.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'No se puede añadir la tarea a la base de datos.')

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open image", "/Users", "Images (*.png *)jpg *.txt")
        self.addressinput.setText(file_path)


class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Buscar")

        self.setWindowTitle("Buscar tarea")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchstudent)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Identificador.")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchstudent(self):

        searchrol = ""
        searchrol = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from task WHERE idTask=" + str(searchrol))
            row = result.fetchone()
            serachresult = "Identificador : " + str(row[0]) + '\n' + "Nombre : " + str(
                row[1]) + '\n' + "Tipo de tarea : " + str(row[2]) + '\n' + '\n' + "dirección : " + str(row[3])
            QMessageBox.information(QMessageBox(), 'Éxito', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'No se puede encontrar la tarea en la base de datos.')


class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Borrar")

        self.setWindowTitle("Borrar tarea")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Identificador.")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):

        delrol = ""
        delrol = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from task WHERE idTask=" + str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Éxito', 'Tarea eliminada con éxito en la base de datos.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'La tarea no puede ser borrada de la base de datos.')


class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(120)

        layout = QVBoxLayout()

        self.userinput = QLineEdit()
        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.userinput.setPlaceholderText("Introduce usuario")
        self.passinput.setPlaceholderText("Introduce contraseña")
        self.QBtn = QPushButton()
        self.QBtn.setText("Acceso")
        self.setWindowTitle('Inicio de sesión')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Inicio de sesión")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.userinput)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):

        self.connection = sqlite3.connect("database2.db")
        query = "SELECT user,pass,idUser FROM user"
        result = self.connection.execute(query)
        result = result.fetchall()
        global IDUSER
        for row_number, row_data in enumerate(result):
            if (self.userinput.text() == str(row_data[0]) and self.passinput.text() == str(row_data[1])):
                self.accept()
                IDUSER = str(row_data[2])
                break
        if (self.userinput.text() == str(row_data[0]) and self.passinput.text() == str(row_data[1])):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Credenciales inválidas, vuelve a intentarlo.')
        self.connection.close()


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Pasos")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap('icon/add.png')
        pixmap = pixmap.scaledToWidth(275)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(150)

        layout.addWidget(title)

        layout.addWidget(QLabel("Primer paso: seleccione añadir tarea."))
        layout.addWidget(QLabel("Segundo paso: introduce los valores solicitados."))
        layout.addWidget(QLabel("Tercer paso: pulse el botón 'Añadir'."))
        layout.addWidget(QLabel("¡ENHORABUENA! La tarea ha sido añadida con éxito."))
        layout.addWidget(labelpic)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class AboutDialog2(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Pasos")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap('icon/pair.png')
        pixmap = pixmap.scaledToWidth(275)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(150)

        layout.addWidget(title)

        layout.addWidget(QLabel("Primer paso: seleccione la tarea que desee."))
        layout.addWidget(QLabel("Segundo paso: acerque tarjeta al lector."))
        layout.addWidget(QLabel("Tercer paso: pulse el botón 'Vincular'."))
        layout.addWidget(QLabel("¡ENHORABUENA! La tarea ha sido vinculada con éxito."))
        layout.addWidget(labelpic)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class rfidDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(rfidDialog, self).__init__(*args, **kwargs)

        self.QBtnPair = QPushButton()
        self.QBtnPair.setText("Vincular")

        self.setFixedWidth(500)
        self.setFixedHeight(300)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Vincular tarjeta con tarea")
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)
        title.setFixedHeight(50)

        labelpic = QLabel()
        pixmap = QPixmap('icon/rfid.png')
        pixmap = pixmap.scaledToWidth(300)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(100)
        labelpic.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        task = QLabel("Tareas:")
        layout.addWidget(task)
        self.branchinput = QComboBox()

        self.connection = sqlite3.connect("database.db")
        query = "SELECT name FROM task "
        result = self.connection.execute(query)
        result = result.fetchall()
        for row_number, row_data in enumerate(result):
            for column_number, data in enumerate(row_data):
                self.branchinput.addItem(str(data))
        self.connection.close()
        layout.addWidget(self.branchinput)

        card = QLabel("Tarjeta:")
        self.cardinput = QLineEdit()

        layout.addWidget(card)
        layout.addWidget(self.cardinput)
        layout.addWidget(labelpic)
        layout.addWidget(self.QBtnPair)

        self.QBtnPair.clicked.connect(self.escucha)

        self.setLayout(layout)

    def escucha(self):
        clf = nfc.ContactlessFrontend()
        if not clf.open('usb'):
            raise RuntimeError("Failed to open NFC device.")

        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        tag_id = str(tag).split('ID=')[1]

        self.connection = sqlite3.connect("database.db")
        global IDUSER 
        result = self.connection.execute("SELECT card,branch,address FROM task WHERE idUser=?", (IDUSER))
        result = result.fetchall()
        for row_number, row_data in enumerate(result):
            if (row_data[0] == tag_id):
                if (row_data[1] == 'Documento'):
                    self.fn_activarNotas(row_data[2])
        self.connection.close()

    def fn_activarNotas(self, address):
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


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS task(idTask INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR ,branch TEXT,address TEXT,card VARCHAR, idUser INTEGER)")
        self.c.close()

        self.conn = sqlite3.connect("database2.db")
        self.c = self.conn.cursor()
        # nam = "Ejemplo"
        # passw = "1234"
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS user(idUser INTEGER PRIMARY KEY AUTOINCREMENT,user VARCHAR ,pass VARCHAR)")
        # self.c.execute("INSERT INTO user (user,pass) VALUES (?,?)", (nam, passw))
        # self.conn.commit()
        self.c.close()
        # self.conn.close()

        file_menu = self.menuBar().addMenu("&Tarea")
        rfid_menu = self.menuBar().addMenu("&Tarjeta")
        help_menu = self.menuBar().addMenu("&Ayuda")

        self.setWindowTitle("TaskMate")

        self.setMinimumSize(800, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            ("identificador.", "Nombre", "Tipo de tarea", "Dirección", "Tarjeta"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Añadir tarea", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Añadir tarea")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"), "Refrescar", self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refrescar datos")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Buscar", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Buscar tarea")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Borrar", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Borrar tarea")
        toolbar.addAction(btn_ac_delete)

        adduser_action = QAction(QIcon("icon/add.png"), "Insertar tarea", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Buscar tarea", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Borrar tarea", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

        about_action = QAction(QIcon("icon/info.png"), "Crear nueva tarea", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)
        about_action2 = QAction(QIcon("icon/info.png"), "Vincular tarjeta con tarea", self)
        about_action2.triggered.connect(self.about2)
        help_menu.addAction(about_action2)

        rfid_action = QAction(QIcon("icon/pair.png"), "Vincular tarjeta con tarea", self)
        rfid_action.triggered.connect(self.rfid)
        rfid_menu.addAction(rfid_action)

    def loaddata(self):
        self.connection = sqlite3.connect("database.db")
        global IDUSER
        result = self.connection.execute("SELECT * FROM task WHERE idUser=?", (IDUSER))
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()
        self.loaddata()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()
        self.loaddata()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def about2(self):
        dlg = AboutDialog2()
        dlg.exec_()

    def rfid(self):
        dlg = rfidDialog()
        dlg.exec_()

def fn_activarNotas(address):
    print("LIBRO:dirección del objeto: ",address)
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
    print("VIDEO:dirección del objeto: ",address)
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
def listen():
    print(threading.currentThread().getName(), 'Lanzado')
    clf = nfc.ContactlessFrontend()
    if not clf.open('usb'):
        raise RuntimeError("Failed to open NFC device.")

    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    tag_id = str(tag).split('ID=')[1]

    connection = sqlite3.connect("database.db")

    result = connection.execute("SELECT card,branch,address FROM task WHERE idUser=1")
    result = result.fetchall()
    for row_number, row_data in enumerate(result):
        if (row_data[0] == tag_id):
            address = (row_data[2])
            if (row_data[1] == 'Documento'):
                fn_activarNotas(address)
            if (row_data[1] == "Video"):
                fn_activarVideo(address)
    connection.close()

    print(threading.currentThread().getName(), 'Deteniendo')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    passdlg = LoginDialog()
    if (passdlg.exec_() == QDialog.Accepted):

        window = MainWindow()
        window.show()
        window.loaddata()

    sys.exit(app.exec_())

