import serial
import serial.tools.list_ports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextCursor
from PyQt5.QtWidgets import QLineEdit, QApplication, QAbstractItemView


def serial_ports():
    ports = serial.tools.list_ports.comports()
    result = []
    event = 1
    for port, desc, hwid in sorted(ports):
        try:
            if (desc.find('MOXA') != -1):
                # print("{}: {}".format(port, desc, hwid))
                result.append(port)
                # s = serial.Serial(port)
                # s.close()
        except (OSError, serial.SerialException):
            pass
    return result


ts_names = ["Наличие питания на вх. Канале 1", "Наличие питания на вх. Канале 2",
            "Наличие питания на вх. Канале 3", "Наличие питания на вх. Канале 4",
            "Перегрузка по току", "Наличие питания на выходе",
            "Активность вх. Канала 1", "Активность вх. Канала 2", "Активность вх. Канала 3",
            "Активность вх. Канала 4", "Таймаут работы канала 1", "Таймаут работы канала 2",
            "Таймаут работы канала 3", "Таймаут работы канала 4", "Тип напряжения на канале 1 (AC/DC)",
            "Тип напряжения на канале 2 (AC/DC)", "Тип напряжения на канале 3 (AC/DC)", "Тип напряжения на канале 4 (AC/DC)",
            "Превышение мгн. значения I", "Превышение старт. значения I", "Превышение ном. значения I",
            "Превышение экстр. значения I"]

ti_names = ["Напряжение входного канала 1","Напряжение входного канала 2","Напряжение входного канала 3", "Напряжение входного канала 4",
            "Величина Тока","Текущее время работы канала 1","Текущее время работы канала 2",
            "Текущее время работы канала 3", "Текущее время работы канала 4", "Напряжение на выходе"]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        ports = serial_ports()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(805, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(490, 680, 141, 31))
        self.pushButton.setObjectName("pushButton")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(190, 680, 141, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setText("104")

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(340, 680, 141, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setText("1")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(640, 680, 141, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.tableView_model = QStandardItemModel()
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setModel(self.tableView_model)
        self.tableView.setGeometry(QtCore.QRect(200, 50, 281, 450))
        self.tableView.setObjectName("tableView")

        self.tableView.horizontalHeader().setDefaultSectionSize(70)
        self.tableView.horizontalHeader().setMinimumSectionSize(10)
        # self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setDefaultSectionSize(10)
        self.tableView.verticalHeader().setMinimumSectionSize(10)

        self.tableView.setFont(QtGui.QFont('Arial', 7))
        self.tableView_model.setVerticalHeaderLabels(ts_names)

        self.tableView_2_model = QStandardItemModel()
        self.tableView_2 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_2.setModel(self.tableView_2_model)
        self.tableView_2.setGeometry(QtCore.QRect(490, 50, 291, 450))
        self.tableView_2.setObjectName("tableView_2")

        self.tableView_2.horizontalHeader().setDefaultSectionSize(70)
        self.tableView_2.horizontalHeader().setMinimumSectionSize(10)
        self.tableView_2.verticalHeader().setDefaultSectionSize(10)
        self.tableView_2.verticalHeader().setMinimumSectionSize(10)
        self.tableView_2.setFont(QtGui.QFont('Arial', 7))
        self.tableView_2_model.setVerticalHeaderLabels(ti_names)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(340, 660, 141, 16))
        self.label_2.setObjectName("label_2")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 680, 161, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(ports)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 660, 141, 16))
        self.label_3.setObjectName("label_3")

        self.ch1 = QtWidgets.QPushButton(self.centralwidget)
        self.ch1.setGeometry(QtCore.QRect(20, 50, 161, 41))
        self.ch1.setStyleSheet("")
        self.ch1.setCheckable(False)
        self.ch1.setObjectName("ch1")
        self.ch1.setEnabled(False)

        self.ch4 = QtWidgets.QPushButton(self.centralwidget)
        self.ch4.setGeometry(QtCore.QRect(20, 200, 161, 41))
        self.ch4.setObjectName("ch4")
        self.ch4.setEnabled(False)

        self.rs_to_rs = QtWidgets.QPushButton(self.centralwidget)
        self.rs_to_rs.setGeometry(QtCore.QRect(20, 250, 161, 41))
        self.rs_to_rs.setObjectName("rs_to_rs")
        self.rs_to_rs.setEnabled(False)

        self.kz = QtWidgets.QPushButton(self.centralwidget)
        self.kz.setGeometry(QtCore.QRect(20, 300, 161, 41))
        self.kz.setObjectName("kz")
        self.kz.setEnabled(False)

        self.ch2 = QtWidgets.QPushButton(self.centralwidget)
        self.ch2.setGeometry(QtCore.QRect(20, 100, 161, 41))
        self.ch2.setObjectName("ch2")
        self.ch2.setEnabled(False)

        self.ch3 = QtWidgets.QPushButton(self.centralwidget)
        self.ch3.setGeometry(QtCore.QRect(20, 150, 161, 41))
        self.ch3.setObjectName("ch3")
        self.ch3.setEnabled(False)

        self.ts_lbl_4 = QtWidgets.QLabel(self.centralwidget)
        self.ts_lbl_4.setGeometry(QtCore.QRect(490, 10, 310, 31))
        self.ts_lbl_4.setObjectName("ts_lbl_4")

        self.ts_lbl_3 = QtWidgets.QLabel(self.centralwidget)
        self.ts_lbl_3.setGeometry(QtCore.QRect(200, 10, 251, 31))
        self.ts_lbl_3.setObjectName("ts_lbl_3")
        self.ts_lbl_5 = QtWidgets.QLabel(self.centralwidget)
        self.ts_lbl_5.setGeometry(QtCore.QRect(40, 10, 131, 31))
        self.ts_lbl_5.setObjectName("ts_lbl_5")

        self.start_logic = QtWidgets.QPushButton(self.centralwidget)
        self.start_logic.setGeometry(QtCore.QRect(20, 350, 161, 30))
        self.start_logic.setObjectName("start_logic")
        self.start_logic.setEnabled(False)

        self.end_logic = QtWidgets.QPushButton(self.centralwidget)
        self.end_logic.setGeometry(QtCore.QRect(20, 380, 161, 30))
        self.end_logic.setText("Остановить проверку")
        self.end_logic.setObjectName("end_logic")
        self.end_logic.setEnabled(False)

        self.ts_ti_on = QtWidgets.QPushButton(self.centralwidget)
        self.ts_ti_on.setGeometry(QtCore.QRect(20, 430, 161, 30))
        self.ts_ti_on.setObjectName("ts_ti_on")
        self.ts_ti_on.setText("Включить ТС/ТИ")
        self.ts_ti_on.setEnabled(False)

        self.ts_ti_off = QtWidgets.QPushButton(self.centralwidget)
        self.ts_ti_off.setGeometry(QtCore.QRect(20, 460, 161, 30))
        self.ts_ti_off.setObjectName("ts_ti_off")
        self.ts_ti_off.setText("Отключить ТС/ТИ")
        self.ts_ti_off.setEnabled(False)



        self.stringlistmodel = QStringListModel()  # Create stringlistmodel object
        self.string_list = []
        self.stringlistmodel.setStringList(self.string_list)  # assign data to model
        self.listView = QtWidgets.QListView(self.centralwidget)

        self.listView.setGeometry(QtCore.QRect(20, 530, 760, 120))
        self.listView.setObjectName("listView")
        self.listView.setModel(self.stringlistmodel)  # Associate view with model

        # self.listView.setDragDropMode(1)

        # setting auto scroll property
        self.listView.setAutoScroll(True)
        self.listView.setAutoScrollMargin(False)
        # self.listView.setVerticalScrollMode(QAbstractItemView.scrollP)

        # # setting word wrap property
        # self.listView.setWordWrap(True)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 510, 141, 16))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(190, 660, 141, 16))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Стенд ASR"))
        self.pushButton.setText(_translate("MainWindow", "Соединить"))
        self.pushButton_2.setText(_translate("MainWindow", "Разъединить"))
        self.label_2.setText(_translate("MainWindow", "Адрес ASR"))
        self.label_3.setText(_translate("MainWindow", "COM порт"))
        self.ch1.setText(_translate("MainWindow", "Канал 1"))
        self.ch4.setText(_translate("MainWindow", "Канал 4"))
        self.rs_to_rs.setText(_translate("MainWindow", "Порт связи"))
        self.kz.setText(_translate("MainWindow", "Короткое замыкание"))
        self.ch2.setText(_translate("MainWindow", "Канал 2"))
        self.ch3.setText(_translate("MainWindow", "Канал 3"))
        self.ts_lbl_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Телеизмерения</span></p></body></html>"))
        self.ts_lbl_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Телесигналы</span></p></body></html>"))
        self.ts_lbl_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Управление</span></p></body></html>"))
        self.start_logic.setText(_translate("MainWindow", "Начать проверку"))
        self.label_4.setText(_translate("MainWindow", "Лог"))
        self.label_5.setText(_translate("MainWindow", "Адрес dout"))
