import threading
import serial
import datetime
import time
import struct

# import protocol.main
from .main import checkSum
from .main import readPackage
from .main import BaseProtocol

def HexDump(a):
    s = "     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\r\n"
    for k, v in enumerate(a):
        if k % 0x10 == 0x0:
            s += "{0:02X}: ".format(k)

        s += "{0:02X} ".format(v)

        if k % 0x10 == 0xF:
            s += "\r\n"
    return s


class SerialThread (threading.Thread):
    def __init__(self, r, fn=None):
        threading.Thread.__init__(self)
        self.r = r
        self.fn = fn

    def run(self):
        while(1):
            if (not self.r.is_open) and (self.in_waiting > 4):
                time.delay(0.1)
            msg, body = readPackage(self.r)
            if msg != None:
                if msg == "EOF":
                    break
                # print("Msg: {0}".format(msg))
                continue
            if self.fn == None:
                self.packReadEvent(body)
            else:
                self.fn(body)

    def packReadEvent(self, body):
        print(body)


class SerialThreadSend(threading.Thread):
    def __init__(self, w, fn=None):
        threading.Thread.__init__(self)
        self.w = w
        self.delay = 1
        self.cnt = 1
        self.sTime = datetime.datetime.now()
        self.fn = fn

        self.A_time = None

    def run(self):
        self.sTime = datetime.datetime.now()

        self.A_time = self.sTime
        while(1):
            n = datetime.datetime.now()

            if ((n - self.sTime).total_seconds()) > (self.delay * (self.cnt)):
                self.cnt += 1
                if not self.fn is None:
                    # print("BBB: {0}".format((n - self.sTime).total_seconds()))
                    self.sendPackage(self.fn())

                    print("mmm: {0}".format((n - self.A_time).total_seconds()))
                    time.sleep(self.delay*(self.delay /
                                           (n - self.A_time).total_seconds()))
                    self.A_time = n
            # time.sleep(self.delay*0.01)


# 导入协议模块
M = []

from .device import VB_Mind_H2
from .device import UTM

M.append(UTM.USB_Temp_Monitor)
M.append(VB_Mind_H2.VB_Mind_H2)

print("load Protocol {}".format(len(M)))
for k, v in enumerate(M):
    print("\t{0}. {1} {2} {3}".format(k, v.Name, v.Device, v.Description))
