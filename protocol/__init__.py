import threading
from . import main
from .main import M
import serial
import datetime
import time
import struct


class SerialThread (threading.Thread):
    def __init__(self, r, fn=None):
        threading.Thread.__init__(self)
        self.r = r
        self.fn = fn

    def run(self):
        while(1):
            msg, body = main.readPackage(self.r)
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
                    time.sleep(self.delay*(self.delay/ (n - self.A_time).total_seconds()))
                    self.A_time=n
            # time.sleep(self.delay*0.01)

    def sendPackage(self, body):
        s = b"\xF5\xFA"
        s += struct.pack(">B", len(body)+4)
        s += body
        s += struct.pack(">B", main.checkSum(s))

        self.w.write(s)
        self.w.flush()


if __name__ == '__main__':
    aat = SerialThreadSend()
    aat.setDaemon(True)
    aat.start()

    while(1):
        pass
