import sys,sqlite3
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

IDRFID: str

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
        self.branchinput.addItem("Alarma")
        layout.addWidget(self.branchinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Dirección")
        layout.addWidget(self.addressinput)

        self.QBtnFile = QPushButton()
        self.QBtnFile.setText("Seleccionar archivo")
        self.QBtnFile.clicked.connect(self.open_file)
        layout.addWidget(self.QBtnFile)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):

        name = ""
        branch = ""
        address = ""

        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        address = self.addressinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO task (name,branch,address) VALUES (?,?,?)",(name,branch,address))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Éxito','La tarea ha sido añadida con éxito a la base de datos.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'No se puede añadir la tarea a la base de datos.')

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open image","/Users","Images (*.png *jpg)")
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
            result = self.c.execute("SELECT * from task WHERE roll="+str(searchrol))
            row = result.fetchone()
            serachresult = "Identificador : "+str(row[0])+'\n'+"Nombre : "+str(row[1])+'\n'+"Tipo de tarea : "+str(row[2])+'\n'+'\n'+"dirección : "+str(row[3])
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
            self.c.execute("DELETE from task WHERE roll="+str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Éxito','Tarea eliminada con éxito en la base de datos.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'La tarea no puede ser borrada de la base de datos.')

class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(120)

        layout = QVBoxLayout()

        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Introduce contraseña.")
        self.QBtn = QPushButton()
        self.QBtn.setText("Acceso")
        self.setWindowTitle('Inicio de sesión')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Inicio de sesión")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        if(self.passinput.text() == "1234" or 1==1):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Wrong Password')





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
        query = "SELECT name FROM task"
        result = self.connection.execute(query)
        result = result.fetchall()
        for row_number, row_data in enumerate(result):
                for column_number, data in enumerate(row_data):
                    self.branchinput.addItem(str(data))
        self.connection.close()
        layout.addWidget(self.branchinput)


        card = QLabel("Tarjeta:")
        self.cardinput = QLineEdit()
        #D_Changed = pyqtSignal(float)
        #self.D_Changed.connect(self.on_D_Changed)


        layout.addWidget(card)
        layout.addWidget(self.cardinput)
        layout.addWidget(labelpic)
        layout.addWidget(self.QBtnPair)


        self.cardinput.setText('466849654')
        #cardinput.connectNotify(self.getRfid)


        self.setLayout(layout)


    def addpair(self):

        idTask = ""
        idTarjet = ""

        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        address = self.addressinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO task (name,branch,address) VALUES (?,?,?)", (name, branch, address))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Éxito',
                                    'La tarea ha sido añadida con éxito a la base de datos.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'No se puede añadir la tarea a la base de datos.')

    #@pyqtSlot(float)
    def getRfid(self):
        result = '546466166'
        self.cardinput.setText(result)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS task(roll INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR ,branch TEXT,address TEXT,card VARCHAR)")
        self.c.close()

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
        self.tableWidget.setHorizontalHeaderLabels(("identificador.", "Nombre", "Tipo de tarea","Dirección", "Tarjeta"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Añadir tarea", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Añadir tarea")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"),"Refrescar",self)
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

        adduser_action = QAction(QIcon("icon/add.png"),"Insertar tarea", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Buscar tarea", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Borrar tarea", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)


        about_action = QAction(QIcon("icon/info.png"),"Crear nueva tarea", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        rfid_action = QAction(QIcon("icon/pair.png"), "Vincular tarjeta con tarea", self)
        rfid_action.triggered.connect(self.rfid)
        rfid_menu.addAction(rfid_action)

    def loaddata(self):
        self.connection = sqlite3.connect("database.db")
        query = "SELECT * FROM task"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
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

    def rfid(self):
        dlg = rfidDialog()
        dlg.exec_()



app = QApplication(sys.argv)
passdlg = LoginDialog()
if(passdlg.exec_() == QDialog.Accepted):
    window = MainWindow()
    window.show()
    window.loaddata()
sys.exit(app.exec_())