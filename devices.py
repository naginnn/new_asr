
import time
from datetime import datetime

import minimalmodbus
# переделать под ASR





class Modb:
    connect = ()
    def getConnection(self,  port, slave_adress, baudrate):
        try:
            self.instrument = minimalmodbus.Instrument(port, slave_adress)
            self.instrument.serial.baudrate = 115200  # Baud
            self.instrument.serial.bytesize = 8
            self.instrument.serial.stopbits = 1  # seconds
            self.instrument.close_port_after_each_call = True
            self.instrument.clear_buffers_before_each_transaction = True
            self.connect = self.instrument
            return True
        except:
            return False

    # если соединение заебато
    def getСonnectivity(self):
        return self.connect

class Dout:
    color = ""
    dout_names = {"KZ": 81, "RS1": 82, "RS2": 83, "RS3": 84, "CH1": 85,
                  "CH2": 86, "CH3": 87, "CH4": 88}
    remote_dout_names = ["KZ", "CH1", "CH2", "CH3", "CH4", "RS1", "RS2", "RS3"]
    dout_numbers = [81, 82, 83, 84, 85, 86, 87, 88]
    def __init__(self, instrument):
        self.instrument = instrument

    def get_key(self,value):
        for k, v in self.dout_names.items():
            if v == value:
                return k

    def check_tu_ti(self, signal):
        dout_signals = self.get_status()
        if (dout_signals != False):
            if (dout_signals[list(self.dout_names).index(signal)] == 1):
                self.color = "green"
                return True
            else:
                self.color = "red"
                return False

    def get_status(self):
        try:
            signals = self.instrument.read_registers(1, 8, 3)
            if (len(signals) == 8):
                return signals
        except:
            return False

    def off_enabled(self):
        i = 0
        try:
            dout_signals = self.get_status()
            if (dout_signals != False):
                for relay in dout_signals:
                    if relay == 1:
                        self.instrument.write_register(self.dout_numbers[i], 0, 4)
                    i = i + 1
                return True
        except:
            return False

    def command(self, relay):
        try:
            if (self.check_tu_ti(relay)):
                self.instrument.write_register(self.dout_names.get(relay), 0, 4)
                self.color = "red"
                return self.color
            else:
                self.instrument.write_register(self.dout_names.get(relay), 1, 4)
                self.color = "green"
                return self.color
        except:
            return False

class Asr:
    asr_numbers_ti = {"U_IN1": 257, "U_IN2": 259, "U_IN3": 261, "U_IN4": 263,
                      "I_OUT": 265,
                      "TIME1": 267, "TIME2": 269, "TIME3": 271, "TIME4": 273,
                      "U_OUT": 275}


    asr_measurements = {"U_IN1":0.0, "U_IN2":0.0, "U_IN3":0.0, "U_IN4":0.0,
                        "I_OUT":0.0,
                        "TIME1":0.0, "TIME2":0.0, "TIME3":0.0,"TIME4":0.0,
                        "U_OUT":0.0}
    measurement = 0.0
    device_status = False

    def __init__(self, instrument):
        self.instrument = instrument

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

# if __name__ == '__main__':
#     log = Log()
#     log.add("Соединение", "Соединение установленно", True)
#     print(log.get_log())





