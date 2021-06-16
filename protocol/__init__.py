from .device import TestMath
from .device import VB_Mind_H2
from .device import UTM
from .device import T8775
from .device import MotorPluse
from .device import testa
from .device import TDS_AB
from .device import Heat980
from .device import CowRobot
import threading
import serial
import datetime
import time
import struct

# import protocol.main
from .utils import checkSum
from .utils import HexDump
# from .main import readPackage
from .base import BaseProtocol, recvFM


class SerialThread (threading.Thread):
    def __init__(self, r, fn=None, ProtType=BaseProtocol.ProtocolType_Std_1):
        threading.Thread.__init__(self)
        self.r = r
        self.fn = fn
        self.ProtType = ProtType

    def run(self):
        while(1):
            if (not self.r.is_open) and (self.in_waiting > 4):
                time.delay(0.1)
            msg, body = recvFM[self.ProtType](self.r)
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

M.append(UTM.USB_Temp_Monitor)
M.append(VB_Mind_H2.VB_Mind_H2)
M.append(T8775.T8775)
M.append(MotorPluse.MotorPluse)
M.append(testa.testA)
M.append(TestMath.TestMath)
M.append(TDS_AB.TDS_AB)
M.append(Heat980.Heat980)
M.append(CowRobot.CowRobot)


def find(name):
    for k, v in enumerate(M):
        if name == v.Device:
            return M[k]


print("load Protocol {}".format(len(M)))
for k, v in enumerate(M):
    print("\t{0}. {1} {2} {3}".format(k, v.Name, v.Device, v.Description))
