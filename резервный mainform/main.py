from datetime import datetime

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QStandardItem
from PyQt5 import QtCore, QtWidgets
from mainform import Ui_MainWindow
import sys
import devices

class MyThreadLogic(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    dout = ()
    asr = ()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running = False  # Флаг выполнения
        self.count = 0

    def set_devices(self, dout, asr):
        self.dout = dout
        self.asr = asr

    def run(self):
        self.running = True
        while self.running:  # Проверяем значение флага
            #####Thread code######
            self.count += 1
            print(self.count)
            self.dout.command("CH1")
            self.mysignal.emit(message("Подаем напряжение на IN1"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 1 секунда"))
            if self.running == False:
                self.mysignal.emit(message("Принудительная остановка"))
                break
            self.dout.command("CH2")
            self.mysignal.emit(message("Подаем напряжение на IN2"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 1 секунда"))

            if self.running == False:
                self.mysignal.emit(message("Принудительная остановка"))
                break
            self.dout.command("CH3")
            self.mysignal.emit(message("Подаем напряжение на IN3"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 1 секунда"))
            self.sleep(1)

            if self.running == False:
                self.mysignal.emit(message("Принудительная остановка"))
                break
            self.mysignal.emit(message("Ожидание 5 секунд"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 4 секунды"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 3 секунды"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 2 секунды"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 1 секунда"))
            self.sleep(1)

            if self.running == False:
                self.mysignal.emit(message("Принудительная остановка"))
                break
            self.mysignal.emit(message("Дать короткое замыкание"))
            self.dout.command("KZ")
            self.mysignal.emit(message("Ожидание 1 секунда"))
            self.sleep(1)

            if self.running == False:
                self.mysignal.emit(message("Принудительная остановка"))
                break
            self.mysignal.emit(message("Снять короткое замыкание"))
            self.dout.command("KZ")
            self.mysignal.emit(message("Ожидание 1 секунда"))
            self.sleep(1)

            if self.running == False:
                self.mysignal.emit(message("Принудительная остановка"))
                break
            self.mysignal.emit(message("Снять напряжение с IN1"))
            self.dout.command("CH1")

            self.mysignal.emit(message("Ожидание 10 секунд"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 9 секунд"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 8 секунд"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 7 секунд"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 6 секунд"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 5 секунд"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 4 секунды"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 3 секунды"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 2 секунды"))
            self.sleep(1)
            self.mysignal.emit(message("Ожидание 1 секунда"))
            self.sleep(1)
            if self.running == False:
                self.mysignal.emit(message("Принудительная остановка"))
                break

            # self.mysignal.emit("count = %s" % self.count) # вызов метода on_change

            self.sleep(3)  # Имитируем процесс
            self.mysignal.emit(message("Конец сценария"))
            self.mysignal.emit("end")
            self.running = False
            break
            #####Thread code######

class MyThreadGetTs(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    asr = ()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.update = False  # Флаг выполнения
        self.count = 0

    def set_devices(self, asr):
        self.asr = asr

    def run(self):
        self.update = True
        while self.update:  # Проверяем значение флага
            #####Thread code######
            self.mysignal.emit("")
            self.sleep(5)
            #####Thread code######

class MyThreadGetTi(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    asr = ()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.update = False  # Флаг выполнения
        self.count = 0

    def set_devices(self, asr):
        self.asr = asr

    def run(self):
        self.update = True
        while self.update:  # Проверяем значение флага
            #####Thread code######
            self.mysignal.emit("")
            self.sleep(5)
            #####Thread code######

def message(event):
    result = datetime.now().strftime('%H:%M:%S.%f')[:-4] + " " + event
    return result

class mywindow(QtWidgets.QMainWindow):
    buttons = {}
    dout = ()
    asr = ()
    dout_modb = ()
    asr_modb = ()
    def __init__(self):
        super(mywindow, self).__init__()
        self.setFixedSize(800, 740)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.connection)
        self.ui.pushButton_2.clicked.connect(self.disconnection)

        self.ui.kz.clicked.connect(self.manage_kz)
        self.ui.ch1.clicked.connect(self.manage_ch1)
        self.ui.ch2.clicked.connect(self.manage_ch2)
        self.ui.ch3.clicked.connect(self.manage_ch3)
        self.ui.ch4.clicked.connect(self.manage_ch4)
        self.ui.rs_to_rs.clicked.connect(self.manage_rs_to_rs)

        self.mythread = MyThreadLogic()
        self.mythread_ts = MyThreadGetTs()
        self.mythread_ti = MyThreadGetTi()

        self.ui.start_logic.clicked.connect(self.start_logic)
        self.ui.end_logic.clicked.connect(self.stop_logic)

        self.ui.ts_ti_on.clicked.connect(self.update_ts_ti_on)
        self.ui.ts_ti_off.clicked.connect(self.update_ts_ti_off)

        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
        self.mythread_ts.mysignal.connect(self.update_ts, QtCore.Qt.QueuedConnection)
        self.mythread_ti.mysignal.connect(self.update_ti, QtCore.Qt.QueuedConnection)

    def connection(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        self.buttons = {"CH1": self.ui.ch1, "CH2": self.ui.ch2, "CH3": self.ui.ch3, "CH4": self.ui.ch4,
                   "KZ": self.ui.kz, "RS1": self.ui.rs_to_rs, "RS2": self.ui.rs_to_rs, "RS3": self.ui.rs_to_rs}
        try:
            # print(self.ui.comboBox.currentText())
            self.dout_modb = devices.Modb()
            self.asr_modb = devices.Modb()
            com = self.ui.textEdit.toPlainText()
            assert self.dout_modb.getConnection(self.ui.comboBox.currentText(), int(self.ui.textEdit.toPlainText()), 115200)
            assert self.asr_modb.getConnection(self.ui.comboBox.currentText(), int(self.ui.textEdit_2.toPlainText()), 115200)
            self.dout = devices.Dout(self.dout_modb.getСonnectivity())
            self.asr = devices.Asr(self.asr_modb.getСonnectivity())

            dout_status = self.dout.get_status()
            if dout_status == False:
                assert False

            for name in self.dout.remote_dout_names:
                self.dout.check_tu_ti(name)
                self.buttons[name].setStyleSheet('background:' + self.dout.color + ';')

            self.ui.ch1.setEnabled(True)
            self.ui.ch2.setEnabled(True)
            self.ui.ch3.setEnabled(True)
            self.ui.ch4.setEnabled(True)
            self.ui.kz.setEnabled(True)
            self.ui.start_logic.setEnabled(True)
            self.ui.rs_to_rs.setEnabled(True)

            self.ui.comboBox.setEnabled(False)
            self.ui.textEdit.setEnabled(False)
            self.ui.textEdit_2.setEnabled(False)

            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.ts_ti_on.setEnabled(True)
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Соединение установленно"))
            self.ui.listView.scrollToBottom()
        except(AssertionError):
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Неудалось установить соединение"))
            self.ui.listView.scrollToBottom()


        # self.ui.label.setFont(
        #     QtGui.QFont('SansSerif', 30)
        # )  # Изменение шрифта и размера
        # kw = self.ui.line_edit.text()

    def update_ts_ti_on(self):
        self.mythread_ti.set_devices(self.asr)  # передал объект asr'a в поток
        if not self.mythread_ti.isRunning():
            self.mythread_ti.start()  # Запускаем поток

        self.mythread_ts.set_devices(self.asr)  # передал объект asr'a в поток
        if not self.mythread_ts.isRunning():
            self.mythread_ts.start()  # Запускаем поток

        self.ui.ts_ti_on.setEnabled(False)
        self.ui.ts_ti_off.setEnabled(True)
    def update_ts_ti_off(self):
        self.mythread_ts.update = False  # Изменяем флаг выполнения
        self.mythread_ti.update = False  # Изменяем флаг выполнения
        self.ui.ts_ti_on.setEnabled(True)
        self.ui.ts_ti_off.setEnabled(False)

    def update_ti(self, asr_ti):
        try:
            self.ui.tableView_2_model.setColumnCount(1)
            i = 0
            asr_ti = self.asr.get_all_ti()
            for ti_name in asr_ti:
                item = QStandardItem(str(asr_ti[ti_name]))
                self.ui.tableView_2_model.setItem(i, item)
                i += 1
        except:
            self.mythread_ti.update = False  # Изменяем флаг выполнения
            self.mythread_ts.update = False
            row = self.ui.stringlistmodel.rowCount()
            self.ui.stringlistmodel.insertRow(row)
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Невозможно считать ТИ"))
            self.ui.listView.scrollToBottom()
            self.ui.ts_ti_on.setEnabled(True)
            self.ui.ts_ti_off.setEnabled(False)

    def update_ts(self, asr_ts):
        try:
            self.ui.tableView_model.setColumnCount(1)
            i = 0
            asr_ts = self.asr.get_all_ts()
            for ts_name in asr_ts:
                item = QStandardItem(str(asr_ts[ts_name]))
                self.ui.tableView_model.setItem(i, item)
                i += 1
        except:
            self.mythread_ti.update = False  # Изменяем флаг выполнения
            self.mythread_ts.update = False
            row = self.ui.stringlistmodel.rowCount()
            self.ui.stringlistmodel.insertRow(row)
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Невозможно считать ТС"))
            self.ui.listView.scrollToBottom()
            self.ui.ts_ti_on.setEnabled(True)
            self.ui.ts_ti_off.setEnabled(False)

    def disconnection(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        self.mythread_ts.update = False  # Изменяем флаг выполнения
        self.mythread_ti.update = False  # Изменяем флаг выполнения
        self.ui.ch1.setEnabled(False)
        self.ui.ch2.setEnabled(False)
        self.ui.ch3.setEnabled(False)
        self.ui.ch4.setEnabled(False)
        self.ui.kz.setEnabled(False)
        self.ui.start_logic.setEnabled(False)
        self.ui.rs_to_rs.setEnabled(False)

        self.ui.comboBox.setEnabled(True)
        self.ui.textEdit.setEnabled(True)
        self.ui.textEdit_2.setEnabled(True)

        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.ts_ti_on.setEnabled(False)
        self.ui.ts_ti_off.setEnabled(False)
        self.dout = ()
        self.asr = ()
        self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Соединение разорвано"))
        self.ui.listView.scrollToBottom()

    def manage_kz(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        try:
            status = self.dout.command("KZ")
            self.ui.kz.setStyleSheet('background:' + status + ';')
            if status == "green":
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Коротокое замыкание подано"))
                self.ui.listView.scrollToBottom()
            else:
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Коротокое замыкание снято"))
                self.ui.listView.scrollToBottom()
        except:
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Ошибка подачи коротокого замыкания"))
            self.ui.listView.scrollToBottom()

    def manage_ch1(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        try:
            status = self.dout.command("CH1")
            self.ui.ch1.setStyleSheet('background:' + status + ';')
            if status == "green":
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Напряжение на IN1 подано"))
                self.ui.listView.scrollToBottom()
            else:
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Напряжение c IN1 снято"))
                self.ui.listView.scrollToBottom()
        except:
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Ошибка управления IN1"))
            self.ui.listView.scrollToBottom()

    def manage_ch2(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        try:
            status = self.dout.command("CH2")
            self.ui.ch2.setStyleSheet('background:' + status + ';')
            if status == "green":
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Напряжение на IN2 подано"))
                self.ui.listView.scrollToBottom()
            else:
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Напряжение c IN2 снято"))
                self.ui.listView.scrollToBottom()
        except:
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Ошибка управления IN2"))
            self.ui.listView.scrollToBottom()

    def manage_ch3(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        try:
            status = self.dout.command("CH3")
            self.ui.ch3.setStyleSheet('background:' + status + ';')
            if status == "green":
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Напряжение на IN3 подано"))
                self.ui.listView.scrollToBottom()
            else:
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Напряжение c IN3 снято"))
                self.ui.listView.scrollToBottom()
        except:
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Ошибка управления IN3"))
            self.ui.listView.scrollToBottom()

    def manage_ch4(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        try:
            status = self.dout.command("CH4")
            self.ui.ch4.setStyleSheet('background:' + status + ';')
            if status == "green":
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Напряжение на IN4 подано"))
                self.ui.listView.scrollToBottom()
            else:
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Напряжение c IN4 снято"))
                self.ui.listView.scrollToBottom()
        except:
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Ошибка управления IN4"))
            self.ui.listView.scrollToBottom()

    def manage_rs_to_rs(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        try:
            status = self.dout.command("RS1")
            status1 = self.dout.command("RS2")
            status2 = self.dout.command("RS3")

            self.ui.rs_to_rs.setStyleSheet('background:' + status + ';')
            if status == "green" and status1 == "green" and status2 == "green":
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Интерфейс связи RS-485-2"))
                self.ui.listView.scrollToBottom()
            else:
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Интерфейс связи RS-485-1"))
                self.ui.listView.scrollToBottom()
        except:
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Неудалось переключить интерфес связи"))
            self.ui.listView.scrollToBottom()

    def start_logic(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)

        self.ui.ch1.setEnabled(False)
        self.ui.ch2.setEnabled(False)
        self.ui.ch3.setEnabled(False)
        self.ui.ch4.setEnabled(False)
        self.ui.kz.setEnabled(False)
        self.ui.start_logic.setEnabled(False)
        self.ui.rs_to_rs.setEnabled(False)

        self.ui.comboBox.setEnabled(False)
        self.ui.textEdit.setEnabled(False)
        self.ui.textEdit_2.setEnabled(False)

        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.end_logic.setEnabled(True)
        self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Старт сценария"))
        self.ui.listView.scrollToBottom()
        row += 1
        self.ui.stringlistmodel.insertRow(row)
        # отключить все
        self.dout.off_enabled()
        self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Управление сброшено"))
        self.ui.listView.scrollToBottom()

        self.ui.start_logic.setEnabled(False)
        self.ui.end_logic.setEnabled(True)

        self.mythread.set_devices(self.dout, self.asr) # передал объект dout'a в поток
        if not self.mythread.isRunning():
            self.mythread.start()  # Запускаем поток

    def stop_logic(self):
        self.mythread.running = False  # Изменяем флаг выполнения
        self.ui.start_logic.setEnabled(True)

        self.ui.end_logic.setEnabled(False)

        self.ui.ch1.setEnabled(True)
        self.ui.ch2.setEnabled(True)
        self.ui.ch3.setEnabled(True)
        self.ui.ch4.setEnabled(True)
        self.ui.kz.setEnabled(True)
        self.ui.rs_to_rs.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)

        status = self.dout.get_status()
        if status == False:
            assert False
        for name in self.dout.remote_dout_names:
            self.dout.check_tu_ti(name)
            self.buttons[name].setStyleSheet('background:' + self.dout.color + ';')

    def on_change(self, s):
        if s == "end":
            self.stop_logic()
            self.mythread.running = False  # Изменяем флаг выполнения
        else:
            row = self.ui.stringlistmodel.rowCount()
            self.ui.stringlistmodel.insertRow(row)
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message(s))
            self.ui.listView.scrollToBottom()

    def closeEvent(self, event):  # Вызывается при закрытии окна
        self.hide()  # Скрываем окно
        self.mythread.running = False  # Изменяем флаг выполнения
        self.mythread.wait(5000)  # Даем время, чтобы закончить
        event.accept()  # Закрываем окно


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())

# l = [[i + j for i in range(3)] for j in range(4)]
# self.ui.tableView_model.setRowCount(4)
# self.ui.tableView_model.setColumnCount(3)
# for i in range(4):
#     for j in range(3):
#         item = QStandardItem(str(l[i][j]))
#         self.ui.tableView_model.setItem(i, j, item)