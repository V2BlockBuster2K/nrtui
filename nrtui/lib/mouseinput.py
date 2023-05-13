import os
from ctypes import *

libc = CDLL("libc.so.6")


class TimeVal(Structure):
    _fields_ = [("sec", c_long), ("u_sec", c_long)]


class InputEvent(Structure):
    _fields_ = [("time", TimeVal), ("type", c_uint16),
                ("code", c_uint16), ("value", c_int)]


class MouseInput:
    def __init__(self):
        self.handle = -1
        device_name = "event-mouse"
        for device in os.listdir("/dev/input/by-path/"):
            if device[-device_name.__len__():] == device_name:
                self.handle = os.open(
                    "/dev/input/by-path/" + device, os.O_WRONLY)
                return
        raise Exception("Input [" + device_name + "] not found!")

    def __del__(self):
        if self.handle != -1:
            os.close(self.handle)

    def __send_input(self, input_type, code, value):
        start = InputEvent()
        end = InputEvent()
        libc.gettimeofday(pointer(start.time), 0)
        start.type = input_type
        start.code = code
        start.value = value
        libc.gettimeofday(pointer(end.time), 0)
        libc.write(self.handle, pointer(start), sizeof(start))
        libc.write(self.handle, pointer(end), sizeof(end))

    def move(self, y):
        self.__send_input(0x02, 1, y)
