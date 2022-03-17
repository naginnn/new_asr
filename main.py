import time
from datetime import datetime

from PyQt5.QtGui import QStandardItem
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from mainform import Ui_MainWindow
import asr_calib
import sys
import devices
from PyQt5.QtWidgets import QMessageBox

import threading
lock = threading.Lock()
# время ожидания (перерыва)

class MyThreadCalib(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    dout = ()
    asr = ()
    flag = True

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running = False  # Флаг выполнения
        self.count = 0


    def set_devices(self, power_supply, ser, mode):
        self.mode = mode
        self.power_supply = power_supply
        self.ser = ser

    def run(self):
        self.running = True
        while self.running:  # Проверяем значение флага
            #####Thread code######
            ADC_IN1 = []
            ADC_IN2 = []
            ADC_IN3 = []
            ADC_IN4 = []
            ADC_OUT = []
            try:
                if self.mode:
                    self.mysignal.emit(message("Установить напряжение 220V"))
                    self.mysignal.emit("220")
                    while self.flag:
                        time.sleep(1)
                    self.flag = True

                    self.mysignal.emit(message("Переход в режим калибровки"))
                    self.ser.write_register(0x30, 0x33, [0x01, 0x00])
                    self.mysignal.emit(message("Сброс калибровочных коэффициэнтов"))
                    self.ser.write_register(0x2F, 0x01, [0x01])

                    self.mysignal.emit(message("Установить напряжение 50V"))
                    self.mysignal.emit("50")
                    while self.flag:
                        time.sleep(1)
                    self.flag = True

                    ADC_IN1.append(self.ser.read_float(257, 2))
                    ADC_IN2.append(self.ser.read_float(259, 2))
                    ADC_IN3.append(self.ser.read_float(261, 2))
                    ADC_IN4.append(self.ser.read_float(263, 2))
                    ADC_OUT.append(self.ser.read_float(275, 2))

                    self.mysignal.emit(message(ADC_IN1))
                    self.mysignal.emit(message(ADC_IN2))
                    self.mysignal.emit(message(ADC_IN3))
                    self.mysignal.emit(message(ADC_IN4))
                    self.mysignal.emit(message(ADC_OUT))

                    self.mysignal.emit(message("Установить напряжение 75V"))
                    self.mysignal.emit("75")
                    while self.flag:
                        time.sleep(1)
                    self.flag = True

                    ADC_IN1.append(self.ser.read_float(257, 2))
                    ADC_IN2.append(self.ser.read_float(259, 2))
                    ADC_IN3.append(self.ser.read_float(261, 2))
                    ADC_IN4.append(self.ser.read_float(263, 2))
                    ADC_OUT.append(self.ser.read_float(275, 2))

                    self.mysignal.emit(message(ADC_IN1))
                    self.mysignal.emit(message(ADC_IN2))
                    self.mysignal.emit(message(ADC_IN3))
                    self.mysignal.emit(message(ADC_IN4))
                    self.mysignal.emit(message(ADC_OUT))

                    self.mysignal.emit(message("Установить напряжение 85V"))
                    self.mysignal.emit("85")
                    while self.flag:
                        time.sleep(1)
                    self.flag = True

                    ADC_IN1.append(self.ser.read_float(257, 2))
                    ADC_IN2.append(self.ser.read_float(259, 2))
                    ADC_IN3.append(self.ser.read_float(261, 2))
                    ADC_IN4.append(self.ser.read_float(263, 2))
                    ADC_OUT.append(self.ser.read_float(275, 2))

                    self.mysignal.emit(message(ADC_IN1))
                    self.mysignal.emit(message(ADC_IN2))
                    self.mysignal.emit(message(ADC_IN3))
                    self.mysignal.emit(message(ADC_IN4))
                    self.mysignal.emit(message(ADC_OUT))

                    self.mysignal.emit(message("Установить напряжение 300V"))
                    self.mysignal.emit("300")
                    while self.flag:
                        time.sleep(1)
                    self.flag = True

                    ADC_IN1.append(self.ser.read_float(257, 2))
                    ADC_IN2.append(self.ser.read_float(259, 2))
                    ADC_IN3.append(self.ser.read_float(261, 2))
                    ADC_IN4.append(self.ser.read_float(263, 2))
                    ADC_OUT.append(self.ser.read_float(275, 2))

                    self.mysignal.emit(message(ADC_IN1))
                    self.mysignal.emit(message(ADC_IN2))
                    self.mysignal.emit(message(ADC_IN3))
                    self.mysignal.emit(message(ADC_IN4))
                    self.mysignal.emit(message(ADC_OUT))

                    self.mysignal.emit(message("Запись значений АЦП"))
                    g = 0
                    i = 1
                    j = 5
                    voltage = [50.000000, 75.000000, 85.000000, 300.000000]
                    for adc in ADC_IN1:
                        self.mysignal.emit(message(self.ser.write_register(0x28, i, asr_calib.float_to_hexfloat(float(ADC_IN1[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x28, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_IN1[g]), 7)))))

                        self.mysignal.emit(message(self.ser.write_register(0x29, i, asr_calib.float_to_hexfloat(float(ADC_IN2[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x29, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_IN2[g]), 7)))))

                        self.mysignal.emit(message(self.ser.write_register(0x2A, i, asr_calib.float_to_hexfloat(float(ADC_IN3[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x2A, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_IN3[g]), 7)))))

                        self.mysignal.emit(message(self.ser.write_register(0x2B, i, asr_calib.float_to_hexfloat(float(ADC_IN4[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x2B, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_IN4[g]), 7)))))

                        self.mysignal.emit(message(self.ser.write_register(0x2C, i, asr_calib.float_to_hexfloat(float(ADC_OUT[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x2C, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_OUT[g]), 7)))))

                        i = i + 1
                        j = j + 1
                        g = g + 1

                    self.mysignal.emit(message("Выход из режима калибровки"))
                    self.ser.write_register(0x30, 0x33, [0x00, 0x00])

                    time.sleep(3)

                    self.mysignal.emit(message("Установите напряжение 220V"))
                    self.mysignal.emit("220")
                    while self.flag:
                        time.sleep(1)
                    self.flag = True

                    self.mysignal.emit(message("Напряжение IN1: " + str(self.ser.read_float(257, 2))))
                    self.mysignal.emit(message("Напряжение IN2: " + str(self.ser.read_float(259, 2))))
                    self.mysignal.emit(message("Напряжение IN3: " + str(self.ser.read_float(261, 2))))
                    self.mysignal.emit(message("Напряжение IN4: " + str(self.ser.read_float(263, 2))))

                    self.mysignal.emit(message("Калибровка завершена"))
                    self.mysignal.emit("end")
                    time.sleep(3)
                else:
                    self.mysignal.emit(message("Соединение"))
                    assert self.power_supply.connection()
                    self.mysignal.emit(message("Включить удаленный доступ"))
                    assert self.power_supply.remote("ON")
                    self.mysignal.emit(message("Установить напряжение 220V"))
                    assert self.power_supply.set_voltage(220)
                    self.mysignal.emit(message("Включить выход"))
                    assert self.power_supply.output("ON")

                    time.sleep(3)

                    self.mysignal.emit(message("Переход в режим калибровки"))
                    self.mysignal.emit(message(self.ser.write_register(0x30, 0x33, [0x01, 0x00])))
                    self.mysignal.emit(message("Сброс калибровочных коэффициэнтов"))
                    self.mysignal.emit(message(self.ser.write_register(0x2F, 0x01, [0x01])))
                    self.mysignal.emit(message("Установить напряжение 50V"))
                    assert self.power_supply.set_voltage(50)

                    time.sleep(3)

                    ADC_IN1.append(self.ser.read_float(257, 2))
                    ADC_IN2.append(self.ser.read_float(259, 2))
                    ADC_IN3.append(self.ser.read_float(261, 2))
                    ADC_IN4.append(self.ser.read_float(263, 2))
                    ADC_OUT.append(self.ser.read_float(275, 2))

                    self.mysignal.emit(message(ADC_IN1))
                    self.mysignal.emit(message(ADC_IN2))
                    self.mysignal.emit(message(ADC_IN3))
                    self.mysignal.emit(message(ADC_IN4))
                    self.mysignal.emit(message(ADC_OUT))

                    self.mysignal.emit(message("Установить напряжение 75V"))
                    assert self.power_supply.set_voltage(75)

                    time.sleep(3)

                    ADC_IN1.append(self.ser.read_float(257, 2))
                    ADC_IN2.append(self.ser.read_float(259, 2))
                    ADC_IN3.append(self.ser.read_float(261, 2))
                    ADC_IN4.append(self.ser.read_float(263, 2))
                    ADC_OUT.append(self.ser.read_float(275, 2))

                    self.mysignal.emit(message(ADC_IN1))
                    self.mysignal.emit(message(ADC_IN2))
                    self.mysignal.emit(message(ADC_IN3))
                    self.mysignal.emit(message(ADC_IN4))
                    self.mysignal.emit(message(ADC_OUT))

                    self.mysignal.emit(message("Установить напряжение 85V"))
                    assert self.power_supply.set_voltage(85)

                    time.sleep(3)

                    ADC_IN1.append(self.ser.read_float(257, 2))
                    ADC_IN2.append(self.ser.read_float(259, 2))
                    ADC_IN3.append(self.ser.read_float(261, 2))
                    ADC_IN4.append(self.ser.read_float(263, 2))
                    ADC_OUT.append(self.ser.read_float(275, 2))

                    self.mysignal.emit(message(ADC_IN1))
                    self.mysignal.emit(message(ADC_IN2))
                    self.mysignal.emit(message(ADC_IN3))
                    self.mysignal.emit(message(ADC_IN4))
                    self.mysignal.emit(message(ADC_OUT))

                    self.mysignal.emit(message("Установить напряжение 300V"))
                    assert self.power_supply.set_voltage(300)

                    time.sleep(3)

                    ADC_IN1.append(self.ser.read_float(257, 2))
                    ADC_IN2.append(self.ser.read_float(259, 2))
                    ADC_IN3.append(self.ser.read_float(261, 2))
                    ADC_IN4.append(self.ser.read_float(263, 2))
                    ADC_OUT.append(self.ser.read_float(275, 2))

                    self.mysignal.emit(message(ADC_IN1))
                    self.mysignal.emit(message(ADC_IN2))
                    self.mysignal.emit(message(ADC_IN3))
                    self.mysignal.emit(message(ADC_IN4))
                    self.mysignal.emit(message(ADC_OUT))

                    # Записать
                    self.mysignal.emit(message("Запись значение АЦП"))
                    g = 0
                    i = 1
                    j = 5
                    voltage = [50.000000, 75.000000, 85.000000, 300.000000]
                    for adc in ADC_IN1:
                        self.mysignal.emit(
                            message(self.ser.write_register(0x28, i, asr_calib.float_to_hexfloat(float(ADC_IN1[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x28, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_IN1[g]), 7)))))

                        self.mysignal.emit(
                            message(self.ser.write_register(0x29, i, asr_calib.float_to_hexfloat(float(ADC_IN2[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x29, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_IN2[g]), 7)))))

                        self.mysignal.emit(
                            message(self.ser.write_register(0x2A, i, asr_calib.float_to_hexfloat(float(ADC_IN3[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x2A, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_IN3[g]), 7)))))

                        self.mysignal.emit(
                            message(self.ser.write_register(0x2B, i, asr_calib.float_to_hexfloat(float(ADC_IN4[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x2B, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_IN4[g]), 7)))))

                        self.mysignal.emit(
                            message(self.ser.write_register(0x2C, i, asr_calib.float_to_hexfloat(float(ADC_OUT[g])))))
                        self.mysignal.emit(message(self.ser.write_register(0x2C, j, asr_calib.float_to_hexfloat(
                            round(float(voltage[g] / ADC_OUT[g]), 7)))))

                        i = i + 1
                        j = j + 1
                        g = g + 1

                    self.mysignal.emit(message("Выход из режима калибровки"))
                    self.ser.write_register(0x30, 0x33, [0x00, 0x00])

                    self.mysignal.emit(message("Установить напряжение 220V"))
                    assert self.power_supply.set_voltage(220)
                    time.sleep(3)

                    self.mysignal.emit(message("Напряжение IN1: " + str(self.ser.read_float(257, 2))))
                    self.mysignal.emit(message("Напряжение IN2: " + str(self.ser.read_float(259, 2))))
                    self.mysignal.emit(message("Напряжение IN3: " + str(self.ser.read_float(261, 2))))
                    self.mysignal.emit(message("Напряжение IN4: " + str(self.ser.read_float(263, 2))))

                    self.mysignal.emit(message("Калибровка завершена"))
                    self.mysignal.emit(message("end"))

                self.mysignal.emit("end")
                time.sleep(1)
            except(AssertionError):
                self.mysignal.emit(message("Ошибка"))
                self.mysignal.emit("end")

            #####Thread code######

class MyThreadLogic(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    dout = ()
    asr = ()
    ser = ()
    flag = True
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
            self.mysignal.emit("start")
            while self.flag:
                time.sleep(1)
            self.flag = True


            self.dout.command("CH1")
            self.mysignal.emit(message("Снимаем напряжение с IN1"))
            w = 1
            while w <= 30:
                if self.running == False:
                    self.mysignal.emit(message("Принудительная остановка"))
                    break
                self.mysignal.emit(message("Ожидание " + str(w) + " секунд"))
                self.sleep(1)
                w = w + 1

            # проверяем переход на IN2

            self.dout.command("CH2")
            self.mysignal.emit(message("Снимаем напряжение с IN2"))
            w = 1
            while w <= 30:
                if self.running == False:
                    self.mysignal.emit(message("Принудительная остановка"))
                    break
                self.mysignal.emit(message("Ожидание " + str(w) + " секунд"))
                self.sleep(1)
                w = w + 1

            # проверяем переход на IN3
            # выдать окошко предупреждение о снижении нагрузки, иначе форпост не потянет
            self.mysignal.emit("load")
            while self.flag:
                time.sleep(1)
            self.flag = True

            self.dout.command("CH3")
            self.mysignal.emit(message("Снимаем напряжение с IN3"))
            w = 1
            while w <= 30:
                if self.running == False:
                    self.mysignal.emit(message("Принудительная остановка"))
                    break
                self.mysignal.emit(message("Ожидание " + str(w) + " секунд"))
                self.sleep(1)
                w = w + 1

            # проверяем переход на IN4
            # включаем IN1
            self.dout.command("CH1")
            self.mysignal.emit(message("Подаем напряжение на IN1"))

            time.sleep(3)

            # отключаем IN4
            self.dout.command("CH4")
            self.mysignal.emit(message("Снимаем напряжение с IN4"))
            w = 1
            while w <= 30:
                if self.running == False:
                    self.mysignal.emit(message("Принудительная остановка"))
                    break
                self.mysignal.emit(message("Ожидание " + str(w) + " секунд"))
                self.sleep(1)
                w = w + 1

            # проверяем переход на IN1
            # подключаем все оставшиеся каналы
            self.dout.command("CH2")
            self.mysignal.emit(message("Подаем напряжение на IN2"))
            self.dout.command("CH3")
            self.mysignal.emit(message("Подаем напряжение на IN3"))
            self.dout.command("CH4")
            self.mysignal.emit(message("Подаем напряжение на IN4"))

            # убеждаемся в их включении
            self.sleep(3)

            # даем и снимаем КЗ на 1ом канале и отключаем его
            self.dout.command("KZ")
            self.mysignal.emit(message("Подаем короткое замыкание на OUT"))
            self.sleep(2)
            self.dout.command("KZ")
            self.mysignal.emit(message("Снимаем короткое замыкание с OUT"))
            self.dout.command("CH1")
            self.mysignal.emit(message("Снимаем напряжение с IN1"))
            w = 1
            while w <= 30:
                if self.running == False:
                    self.mysignal.emit(message("Принудительная остановка"))
                    break
                self.mysignal.emit(message("Ожидание " + str(w) + " секунд"))
                self.sleep(1)
                w = w + 1

            # даем и снимаем КЗ на 2ом канале и отключаем его
            self.dout.command("KZ")
            self.mysignal.emit(message("Подаем короткое замыкание на OUT"))
            self.sleep(2)
            self.dout.command("KZ")
            self.mysignal.emit(message("Снимаем короткое замыкание с OUT"))
            self.dout.command("CH2")
            self.mysignal.emit(message("Снимаем напряжение с IN2"))
            w = 1
            while w <= 30:
                if self.running == False:
                    self.mysignal.emit(message("Принудительная остановка"))
                    break
                self.mysignal.emit(message("Ожидание " + str(w) + " секунд"))
                self.sleep(1)
                w = w + 1

            # проверяем переход на IN3

            # предупреждаем пользователя о снижении нагрузки, иначе форпост не заведется!
            # выдать окошко предупреждение о снижении нагрузки, иначе форпост не потянет
            self.mysignal.emit("load")
            while self.flag:
                time.sleep(1)
            self.flag = True

            # даем и снимаем КЗ на 3ом канале и отключаем его
            self.dout.command("KZ")
            self.mysignal.emit(message("Подаем короткое замыкание на OUT"))
            self.sleep(2)
            self.dout.command("KZ")
            self.mysignal.emit(message("Снимаем короткое замыкание с OUT"))
            self.dout.command("CH3")
            self.mysignal.emit(message("Снимаем напряжение с IN3"))
            w = 1
            while w <= 30:
                if self.running == False:
                    self.mysignal.emit(message("Принудительная остановка"))
                    break
                self.mysignal.emit(message("Ожидание " + str(w) + " секунд"))
                self.sleep(1)
                w = w + 1

            # проверяем переход на IN4
            # включаем IN1
            self.dout.command("CH1")
            self.mysignal.emit(message("Подаем напряжение на IN1"))

            # даем и снимаем КЗ на 4ом канале и отключаем его
            self.dout.command("KZ")
            self.mysignal.emit(message("Подаем короткое замыкание на OUT"))
            self.sleep(2)
            self.dout.command("KZ")
            self.mysignal.emit(message("Снимаем короткое замыкание с OUT"))
            self.dout.command("CH4")
            self.mysignal.emit(message("Снимаем напряжение с IN4"))
            w = 1
            while w <= 30:
                if self.running == False:
                    self.mysignal.emit(message("Принудительная остановка"))
                    break
                self.mysignal.emit(message("Ожидание " + str(w) + " секунд"))
                self.sleep(1)
                w = w + 1

            # проверяем переход на IN1
            # включем оставшиеся каналы
            self.dout.command("CH2")
            self.mysignal.emit(message("Подаем напряжение на IN2"))
            self.dout.command("CH3")
            self.mysignal.emit(message("Подаем напряжение на IN3"))
            self.dout.command("CH4")
            self.mysignal.emit(message("Подаем напряжение на IN4"))

            self.sleep(3)
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
    result = datetime.now().strftime('%H:%M:%S.%f')[:-4] + " " + str(event)
    return result

class mywindow(QtWidgets.QMainWindow):
    buttons = {}
    dout = ()
    asr = ()
    dout_modb = ()
    asr_modb = ()
    power_suplly = ()
    calib = ()

    def __init__(self):
        super(mywindow, self).__init__()
        self.setFixedSize(950, 735)

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
        self.ui.connection_bp.clicked.connect(self.connection_bp)

        # создание потоков
        self.mythread = MyThreadLogic()
        self.mythread_ts = MyThreadGetTs()
        self.mythread_ti = MyThreadGetTi()
        self.mythread_calib = MyThreadCalib()

        self.ui.start_logic.clicked.connect(self.start_logic)
        self.ui.end_logic.clicked.connect(self.stop_logic)

        self.ui.ts_ti_on.clicked.connect(self.update_ts_ti_on)
        self.ui.ts_ti_off.clicked.connect(self.update_ts_ti_off)

        self.ui.manual.clicked.connect(self.manual_or_auto)
        self.ui.calib.clicked.connect(self.calib)

        # назначение сигналов
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
        self.mythread_ts.mysignal.connect(self.update_ts, QtCore.Qt.QueuedConnection)
        self.mythread_ti.mysignal.connect(self.update_ti, QtCore.Qt.QueuedConnection)
        self.mythread_calib.mysignal.connect(self.calib_start, QtCore.Qt.QueuedConnection)

    def create_window(self, text):
        QMessageBox.about(self, "Внимание!", text)

    def calib(self):
        self.ser = asr_calib.Modbus(self.ui.comboBox.currentText(), 115200, int(self.ui.textEdit_2.toPlainText()))
        self.mythread_calib.set_devices(self.power_suplly, self.ser, self.ui.manual.isChecked())
        if not self.mythread_calib.isRunning():
            self.mythread_calib.start()  # Запускаем поток

    def calib_start(self, s):
        if s == "220":
            self.create_window("Подайте 220В и нажмите ок")
            self.mythread_calib.flag = False
        if s == "50":
            self.create_window("Подайте 50В и нажмите ок")
            self.mythread_calib.flag = False
        if s == "75":
            self.create_window("Подайте 75В и нажмите ок")
            self.mythread_calib.flag = False
        if s == "85":
            self.create_window("Подайте 85В и нажмите ок")
            self.mythread_calib.flag = False
        if s == "300":
            self.create_window("Подайте 300В и нажмите ок")
            self.mythread_calib.flag = False

        if s == "end":
            self.mythread_calib.running = False  # Изменяем флаг выполнения
        else:
            row = self.ui.stringlistmodel.rowCount()
            self.ui.stringlistmodel.insertRow(row)
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message(s))
            self.ui.listView.scrollToBottom()

    def manual_or_auto(self):
        self.connection_bp = False
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        try:
            if self.ui.manual.isChecked():
                self.ui.ip_adress.setEnabled(False)
                self.ui.port.setEnabled(False)
                self.ui.connection_bp.setEnabled(False)
                self.ui.calib.setEnabled(True)
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Включен ручной режим калибровки"))
            else:
                self.ui.ip_adress.setEnabled(True)
                self.ui.port.setEnabled(True)
                self.ui.connection_bp.setEnabled(True)
                self.ui.calib.setEnabled(False)
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row),message("Включен автоматический режим калибровки"))
            self.ui.listView.scrollToBottom()
        except:
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Неудалось изменить режим калибровки"))
            self.ui.listView.scrollToBottom()

    def connection_bp(self):
        row = self.ui.stringlistmodel.rowCount()
        self.ui.stringlistmodel.insertRow(row)
        if self.connection_bp == False:
            self.power_suplly = asr_calib.PowerSupply(self.ui.ip_adress.toPlainText(), int(self.ui.port.toPlainText()))
            if self.power_suplly.connection():
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Блок питания успешно подключен"))
                self.ui.calib.setEnabled(True)
                self.ui.manual.setEnabled(False)
                self.ui.ip_adress.setEnabled(False)
                self.ui.port.setEnabled(False)
                self.ui.connection_bp.setText("Разъединить")
                self.connection_bp = True
            else:
                self.connection_bp = False
                self.ui.connection_bp.setText("Соединить")
                self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Нет соединения с блоком питания проверьте ip адрес или порт"))
        else:
            self.power_suplly = ()
            self.connection_bp = False
            self.ui.manual.setEnabled(True)
            self.ui.ip_adress.setEnabled(True)
            self.ui.port.setEnabled(True)
            self.ui.connection_bp.setText("Соединить")
            self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Соединение разорвано"))

        self.ui.listView.scrollToBottom()

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

            self.ui.manual.setEnabled(True)
            if self.ui.manual.isChecked():
                self.ui.manual.setEnabled(True)
                self.ui.calib.setEnabled(True)
                self.ui.ip_adress.setEnabled(False)
                self.ui.port.setEnabled(False)
            else:
                self.ui.ip_adress.setEnabled(True)
                self.ui.port.setEnabled(True)
                self.ui.connection_bp.setEnabled(True)
                self.ui.calib.setEnabled(False)

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
        # self.dout.off_enabled()
        # self.ui.stringlistmodel.setData(self.ui.stringlistmodel.index(row), message("Управление сброшено"))
        # self.ui.listView.scrollToBottom()

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
        if s == "start":
            self.create_window("На все входные каналы должно быть подано соответствующее напряжение!")
            self.mythread.flag = False

        if s == "load":
            self.create_window("Понизьте нагрузку <5A!")
            self.mythread.flag = False

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