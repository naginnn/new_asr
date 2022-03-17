import struct
from datetime import datetime
import re
import socket
import time
import socket

import FloatToHex
import serial
import crcmod.predefined
from binascii import  unhexlify
import minimalmodbus

# from main import LOBYTE, HIBYTE

HIBYTE = b'\
\x00\xC0\xC1\x01\xC3\x03\x02\xC2\xC6\x06\x07\xC7\x05\xC5\xC4\x04\
\xCC\x0C\x0D\xCD\x0F\xCF\xCE\x0E\x0A\xCA\xCB\x0B\xC9\x09\x08\xC8\
\xD8\x18\x19\xD9\x1B\xDB\xDA\x1A\x1E\xDE\xDF\x1F\xDD\x1D\x1C\xDC\
\x14\xD4\xD5\x15\xD7\x17\x16\xD6\xD2\x12\x13\xD3\x11\xD1\xD0\x10\
\xF0\x30\x31\xF1\x33\xF3\xF2\x32\x36\xF6\xF7\x37\xF5\x35\x34\xF4\
\x3C\xFC\xFD\x3D\xFF\x3F\x3E\xFE\xFA\x3A\x3B\xFB\x39\xF9\xF8\x38\
\x28\xE8\xE9\x29\xEB\x2B\x2A\xEA\xEE\x2E\x2F\xEF\x2D\xED\xEC\x2C\
\xE4\x24\x25\xE5\x27\xE7\xE6\x26\x22\xE2\xE3\x23\xE1\x21\x20\xE0\
\xA0\x60\x61\xA1\x63\xA3\xA2\x62\x66\xA6\xA7\x67\xA5\x65\x64\xA4\
\x6C\xAC\xAD\x6D\xAF\x6F\x6E\xAE\xAA\x6A\x6B\xAB\x69\xA9\xA8\x68\
\x78\xB8\xB9\x79\xBB\x7B\x7A\xBA\xBE\x7E\x7F\xBF\x7D\xBD\xBC\x7C\
\xB4\x74\x75\xB5\x77\xB7\xB6\x76\x72\xB2\xB3\x73\xB1\x71\x70\xB0\
\x50\x90\x91\x51\x93\x53\x52\x92\x96\x56\x57\x97\x55\x95\x94\x54\
\x9C\x5C\x5D\x9D\x5F\x9F\x9E\x5E\x5A\x9A\x9B\x5B\x99\x59\x58\x98\
\x88\x48\x49\x89\x4B\x8B\x8A\x4A\x4E\x8E\x8F\x4F\x8D\x4D\x4C\x8C\
\x44\x84\x85\x45\x87\x47\x46\x86\x82\x42\x43\x83\x41\x81\x80\x40'

LOBYTE = b'\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\
\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40'

def number_func(str):
    try:
        num = re.findall(r'\d*\.\d+|\d+', str)
        num = [float(i) for i in num]
        return float(num[0])
    except:
        return float(0)

# время ожидания (перерыва)
def wait_time(timeout):
    print("Ожидание")
    for t in range(timeout):
        print("Ожидание " + str(t + 1) + " сек")
        time.sleep(1 - time.time() % 1)


# Парсим строку из FLOAT в HEXFLOAT32
def float_to_hexfloat(f):
    data = []
    if f == 0:
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
    else:
        temp2 = hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]
        data.append(int(temp2[6:8], 16))
        data.append(int(temp2[4:6], 16))
        data.append(int(temp2[2:4], 16))
        data.append(int(temp2[0:2], 16))
    return data
# класс соединения serial
class Modbus:
    frame = []
    def __init__(self, com, baudrate, slave_adress):
        self.com = com # string
        self.baudrate = baudrate # int
        self.slave_adress = slave_adress # int

    # сборщик фрейма
    def write_register(self, adress, subadress, data):
        self.frame = [0x55, 0xAA]
        self.frame.append(adress)
        self.frame.append(0x00)
        self.frame.append(subadress)
        for d in data:
            self.frame.append(d)
        self.frame[3] = len(self.frame) + 1
        self.frame.append(self.crc_calculate(self.frame))
        request = self.to_modbus(self.frame)
        self.sending(request)
        return self.frame

    # расчет crc для пакетов
    def crc_calculate(self, frame):
        i = 2
        crc = 0x00
        while i < len(frame):
            crc = crc + frame[i]
            i = i + 1
        while crc > 256:
            crc = crc - 256
        return crc

    # упаковщик фрейма в модбас реализация 17 функции
    def to_modbus(self, frame):
        wrapper = [0x01, 0x17, 0x40, 0x55, 0x00, 0x04, 0x40, 0xAA, 0x00, 0x04]
        # wrapper = [0x01, 0x17]
        wrapper.append(frame[3])
        for f in frame:
            wrapper.append(f)
        frame = []
        hi, lo = self.crc16(wrapper)
        wrapper.append(hi)
        wrapper.append(lo)
        return wrapper

    def read_float(self, start_address, quantity):
        request = [self.slave_adress, 0x03]

        start_address = (start_address).to_bytes(2, byteorder="big", signed=False)
        for b in start_address:
            request.append(b)
        quantity = (quantity).to_bytes(2, byteorder="big", signed=False)
        for c in quantity:
            request.append(c)

        hi, lo = self.crc16(request)
        request.append(hi)
        request.append(lo)

        request = bytes(request)
        # print(request)
        response = self.sending(request)
        # print(response)
        response = response.hex()[6:14]
        return struct.unpack('!f', bytes.fromhex(response))[0]
        # return request

    # расчет crc16 modbus
    def crc16(self, data):
        crchi = 0xFF
        crclo = 0xFF
        for byte in data:
            index = crchi ^ int(byte)
            crchi = crclo ^ LOBYTE[index]
            crclo = HIBYTE[index]
        # print("{0:02X} {1:02X}".format(crclo, crchi)),
        return crchi, crclo

    # пока без проверки пришедшего пакета
    def sending(self, request):
        ser = serial.Serial(self.com, self.baudrate, timeout=0.3)
        ser.write(request)
        response = ser.read(len(request))
        return response

# функции ASR
# создать карты сигналов
# встроить eeprom
class Asr:
    calib_map = {
                  0x28: {"ADC1": 0x01, "GAIN1": 0x05, "ADC2": 0x02, "GAIN2": 0x06, "ADC3": 0x03, "GAIN3": 0x07, "ADC4": 0x04, "GAIN4": 0x08},
                  0x29: {"ADC1": 0x01, "GAIN1": 0x05, "ADC2": 0x02, "GAIN2": 0x06, "ADC3": 0x03, "GAIN3": 0x07, "ADC4": 0x04, "GAIN4": 0x08},
                  0x2A: {"ADC1": 0x01, "GAIN1": 0x05, "ADC2": 0x02, "GAIN2": 0x06, "ADC3": 0x03, "GAIN3": 0x07, "ADC4": 0x04, "GAIN4": 0x08},
                  0x2B: {"ADC1": 0x01, "GAIN1": 0x05, "ADC2": 0x02, "GAIN2": 0x06, "ADC3": 0x03, "GAIN3": 0x07, "ADC4": 0x04, "GAIN4": 0x08},
                  0x2C: {"ADC1": 0x01, "GAIN1": 0x05, "ADC2": 0x02, "GAIN2": 0x06, "ADC3": 0x03, "GAIN3": 0x07, "ADC4": 0x04, "GAIN4": 0x08},
                  }

    asr_numbers_ti = {"U_IN1": 257, "U_IN2": 259, "U_IN3": 261, "U_IN4": 263,
                      "I_OUT": 265, "TIME1": 267, "TIME2": 269, "TIME3": 271,
                      "TIME4": 273, "U_OUT": 275}

    asr_measurements = {"U_IN1":0.0, "U_IN2":0.0, "U_IN3":0.0, "U_IN4":0.0,
                        "I_OUT":0.0,
                        "TIME1":0.0, "TIME2":0.0, "TIME3":0.0,"TIME4":0.0,
                        "U_OUT":0.0}
    measurement = 0.0
    device_status = False

    def __init__(self, instrument, serial):
        self.instrument = instrument
        self.ser = serial
    # получить
    def get_all_ti(self):
        self.check_all_ti()
        return self.asr_measurements

    def check_ti(self, name):
        try:
            self.measurement = round(self.instrument.read_float(self.asr_numbers_ti.get(name), 4), 2)
            if (self.measurement != None):
                return True
            return False
        except:
            return False

    def check_all_ti(self):
        for name in self.asr_measurements:
            result = self.check_ti(name)
            if result != False:
                self.asr_measurements[name] = self.measurement
            else:
                assert False
        return True

    def check_behaviour(self, alleged_behavior):
        try:
            behaviour_list = self.get_all_ts()
            if (behaviour_list != False):
                for alleged_name in alleged_behavior:
                    if alleged_behavior[alleged_name] != behaviour_list[alleged_name]:
                        assert False
                return True
            else:
                assert False
        except:
            return False

    def get_all_ts(self):
        i = 0
        behaviour_list = {"in1": 0, "in2": 0, "in3": 0, "in4": 0, "overload_i": 0, "u_out": 0,
                          "prior_in1": 0, "prior_in2": 0, "prior_in3": 0, "prior_in4": 0,
                          "t_o_in1": 0, "t_o_in2": 0, "t_o_in3": 0, "t_o_in4": 0,
                          "u_type_in1": 0, "u_type_in2": 0, "u_type_in3": 0, "u_type_in4": 0,
                          "instantly_i": 0,"instantly_i_start": 0, "instantly_i_nom": 0, "instantly_i_extra": 0}
        try:
            behaviour = self.instrument.read_registers(1, 22, 3)
            if (len(behaviour) == 22):
                for name in behaviour_list:
                    behaviour_list[name] = behaviour[i]
                    i = i + 1
                return behaviour_list
        except:
            return False

    def calib(self):
        print()

# функции ЛБП
class PowerSupply:
    def __init__(self, ip_adress, port):
        self.ip_adress = ip_adress
        self.port = port
        self.socket = ()
    # добавить 3 попытки
    def connection(self):
        try:
            self.socket = socket.socket()
            self.socket.connect((self.ip_adress, self.port))
            self.socket.send("*IDN?\n".encode())
            if (str(self.socket.recv(100)).find("Elektro-Automatik") != -1):
                self.socket.send("SYSTem:LOCK ON\n".encode())
                self.socket.close()
                return True
            else:
                self.socket.close()
                return False
        except:
            self.socket.close()
            return False

    def remote(self, on_off):
        i = 0
        while True:
            try:
                self.socket = socket.socket()
                self.socket.connect((self.ip_adress, int(self.port)))
                message = "SYSTem:LOCK " + on_off + "\n"
                self.socket.send(message.encode())
                self.socket.close()
                return True
            except:
                if i == 3:
                    return False
                i = i + 1

    def check_remote(self, on_off):
        i = 0
        while True:
            try:
                self.socket = socket.socket()
                self.socket.connect((self.ip_adress, int(self.port)))
                self.socket.send("SYSTem:LOCK:OWNer?".encode())
                param = str(self.socket.recv(100)).find(on_off)
                if (param != -1):
                    self.socket.close()
                    return True
                else:
                    self.socket.close()
                    return False
                i = i + 0.5
                time.sleep(i)
            except:
                if i == 3:
                    return False
                i = i + 1
                time.sleep(i)

    def set_voltage(self, value):
        i = 0
        voltage = str(value)
        while True:
            try:
                self.socket = socket.socket()
                self.socket.connect((self.ip_adress, int(self.port)))
                message = "SOURce:VOLTage " + voltage + "\n"
                self.socket.send(message.encode())
                # self.socket.recv(10)
                self.socket.close()
                return True
            except:
                if (i == 3):
                    self.socket.close()
                    return False
                i = i + 1
                time.sleep(i)

    def check_voltage(self,value):
        i = 0
        while True:
            try:
                self.socket = socket.socket()
                self.socket.connect((self.ip_adress, int(self.port)))
                self.socket.send("MEAS:VOLT?\n".encode())
                voltage = number_func(str(self.socket.recv(10)))
                if ((round(float(voltage)) == round(value)) and round(float(voltage)) != 0):
                    self.socket.close()
                    return True
                if ((round(float(voltage)) != round(value)) and round(float(voltage)) != 0):
                    if (i == 3):
                        self.socket.close()
                        return False
                    i = i + 1
                    time.sleep(i)
            except:
                if (i == 3):
                    return False
                i = i + 1
                time.sleep(i)

    def output(self, on_off):
        i = 0
        while True:
            try:
                self.socket = socket.socket()
                self.socket.connect((self.ip_adress, int(self.port)))
                message = "OUTPut " + on_off + "\n"
                self.socket.send(message.encode())
                self.socket.close()
                return True
            except:
                if i == 3:
                    return False
                i = i + 1
                time.sleep(i)

    def check_output(self, on_off):
        i = 0
        while True:
            try:
                self.socket = socket.socket()
                self.socket.connect((self.ip_adress, int(self.port)))
                self.socket.send("OUTPut?".encode())
                param = str(self.socket.recv(100)).find(on_off)
                if (param != -1):
                    self.socket.close()
                    return True
                else:
                    self.socket.close()
                    return False
            except:
                if i == 3:
                    return False
                i = i + 1
                time.sleep(i)

    # *IDN?
    # MEAS:VOLT? // текущее напряжение блока питания
    # VOLTage?
    # SOURce:VOLTage 10 // установить напряжение MIN/MAX
    # SOURce:CURRent 5 // установить ток MIN/MAX
    # OUTPut ON // включить выход
    # OUTPut OFF // отключить выход
    # MEAS:CURR? // текущий ток блока питания
    # SOUR:VOLTAGE 25 // текущее напряжение блока питания

# if __name__ == '__main__':

def main1(power_supply, ser):
    message = ""
    ADC_IN1 = []
    ADC_IN2 = []
    ADC_IN3 = []
    ADC_IN4 = []
    ADC_OUT = []
    try:
        message = message + "Соединение\n"
        assert power_supply.connection()
        message = message + "!Включить удаленный доступ\n"
        assert power_supply.remote("ON")
        message = message + "!Установить напряжение\n"
        assert power_supply.set_voltage(220)
        message = message + "!Включить выход\n"
        assert power_supply.output("ON")

        wait_time(3)

        message = message + "Переход в режим калибровки\n"
        print(ser.write_register(0x30, 0x33, [0x01, 0x00]))
        message = message + "Сброс калибровочных коэффициэнтов\n"
        print(ser.write_register(0x2F, 0x01, [0x01]))

        message = message + "!Установить напряжение 50V\n"
        assert power_supply.set_voltage(50)
        wait_time(3)

        message = message + "ADC_IN1_50V\n"
        ADC_IN1.append(ser.read_float(257, 2))
        message = message + "ADC_IN2_50V\n"
        ADC_IN2.append(ser.read_float(259, 2))
        message = message + "ADC_IN3_50V\n"
        ADC_IN3.append(ser.read_float(261, 2))
        print("ADC_IN4_50V\n")
        ADC_IN4.append(ser.read_float(263, 2))  #0x0101#0x0002
        print("ADC_OUT_50V\n")
        ADC_OUT.append(ser.read_float(275, 2))

        message = message + "!Установить напряжение 75V\n"
        assert power_supply.set_voltage(75)
        wait_time(3)

        ADC_IN1.append(ser.read_float(257, 2))
        ADC_IN2.append(ser.read_float(259, 2))
        ADC_IN3.append(ser.read_float(261, 2))
        ADC_IN4.append(ser.read_float(263, 2))  # 0x0101#0x0002
        ADC_OUT.append(ser.read_float(275, 2))

        message = message + "!Установить напряжение 85V\n"
        assert power_supply.set_voltage(85)
        wait_time(3)

        ADC_IN1.append(ser.read_float(257, 2))
        ADC_IN2.append(ser.read_float(259, 2))
        ADC_IN3.append(ser.read_float(261, 2))
        ADC_IN4.append(ser.read_float(263, 2))  # 0x0101#0x0002
        ADC_OUT.append(ser.read_float(275, 2))

        message = message + "!Установить напряжение 300V\n"
        assert power_supply.set_voltage(300)
        wait_time(3)

        ADC_IN1.append(ser.read_float(257, 2))
        ADC_IN2.append(ser.read_float(259, 2))
        ADC_IN3.append(ser.read_float(261, 2))
        ADC_IN4.append(ser.read_float(263, 2))
        ADC_OUT.append(ser.read_float(275, 2))

        # Записать
        message = message + "Сброс калибровочных коэффициэнтов\n"
        g = 0
        i = 1
        j = 5
        voltage = [50.000000, 75.000000, 85.000000, 300.000000]
        for adc in ADC_IN1:
            print(ser.write_register(0x28, i, float_to_hexfloat(float(ADC_IN1[g]))))
            print(ser.write_register(0x28, j, float_to_hexfloat(round(float(voltage[g] / ADC_IN1[g]), 7))))

            print(ser.write_register(0x29, i, float_to_hexfloat(float(ADC_IN2[g]))))
            print(ser.write_register(0x29, j, float_to_hexfloat(round(float(voltage[g] / ADC_IN2[g]), 7))))

            print(ser.write_register(0x2A, i, float_to_hexfloat(float(ADC_IN3[g]))))
            print(ser.write_register(0x2A, j, float_to_hexfloat(round(float(voltage[g] / ADC_IN3[g]), 7))))

            print(ser.write_register(0x2B, i, float_to_hexfloat(float(ADC_IN4[g]))))
            print(ser.write_register(0x2B, j, float_to_hexfloat(round(float(voltage[g] / ADC_IN4[g]), 7))))

            print(ser.write_register(0x2C, i, float_to_hexfloat(float(ADC_OUT[g]))))
            print(ser.write_register(0x2C, j, float_to_hexfloat(round(float(voltage[g] / ADC_OUT[g]), 7))))

            i = i + 1
            j = j + 1
            g = g + 1

        message = message + "Выход из режима калибровки\n"
        ser.write_register(0x30, 0x33, [0x00, 0x00])

        message = message + "!Установить напряжение 220V\n"
        assert power_supply.set_voltage(220)
        wait_time(3)

        print("Напряжение IN1", ser.read_float(257, 2))
        print("Напряжение IN2", ser.read_float(259, 2))
        print("Напряжение IN3", ser.read_float(261, 2))
        print("Напряжение IN4", ser.read_float(263, 2))  # 0x0101#0x0002

        message = message + "Калибровка завершена\n"

    except (AssertionError):
        message = message + "Ошибка\n"
############################################################################

    # print(struct.unpack('!f', bytes.fromhex())[0])
    # q = int('0x425c0000', 16)
    # b8 = struct.pack('i', q)
    # dec = struct.unpack('f', b8)


    # rs_232 = ser.to_rs232(адрес, суб_адрес, [данные])
    # rs_232 = ser.to_rs232(0x2f, 0x01, [0x01])
    # print(rs_232)
    # modbus = ser.to_modbus(rs_232)
    #
    # v = [0x01, 0x17 ,0x07, 0x55, 0xaa ,0x2f ,0x07 ,0x01 ,0x01 ,0x38, 0x13, 0xeb]
    # print(v)
    # print(modbus)

    # # 1. Переход в режим калибровки
    # rs_232 = ser.to_rs232(0x30, 0x33, [0x01, 0x00])
    # print(rs_232)
    # modbus = ser.to_modbus()
    # v = [0x01, 0x17, 0x40, 0x55, 0x00, 0x04, 0x40, 0xAA, 0x00, 0x04, 0x08, 0x55, 0xAA, 0x30, 0x08, 0x33, 0x01, 0x00,
    #      0x6C, 0x51, 0x8A]
    # print(v)
    # print(modbus)
    #
    # # 2. Сброс калибровочных коэффициэнтов
    # rs_232 = ser.to_rs232(0x2F, 0x01, [0x01])
    # print(rs_232)
    # modbus = ser.to_modbus()
    # v = [0x01, 0x17, 0x40, 0x55, 0x00, 0x04, 0x40, 0xAA, 0x00, 0x04, 0x07, 0x55, 0xAA, 0x2F, 0x07, 0x01, 0x01, 0x38, 0xFC, 0x5B]
    # print(v)
    # print(modbus)

    # разделить
    # e = 8
    # i = bytearray(e, 2)
    # print()
    #
    # g = e[2:]
    # print(g[:2])
    # print(g[2:])
    #
    # print(0x0008)

    # 3. Устанавливаем напряжение 50V считываем значения ADC на всех каналах





