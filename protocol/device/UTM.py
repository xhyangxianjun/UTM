import struct

import timer

from protocol import BaseProtocol
from protocol import HexDump


class USB_Temp_Monitor(BaseProtocol):
    Device = "UTM"
    Name = "USB温度监控仪"
    Description = ""
    xAxis = [{
        "Name": "通道1",
        "Scale": 1,
    }, {
        "Name": "通道2",
        "Scale": 1,
    }, {
        "Name": "通道3",
        "Scale": 1,
    }, {
        "Name": "通道4",
        "Scale": 1,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=0.5, acc=0.001, fn=self.onClock)

    def parsePkg(self, body):

        # print(HexDump(body))

        (cmd, seq) = struct.unpack(r">BH", body[:3])

        # print("cmd {0:02X} seq {1:04X} ".format(cmd, seq))

        if cmd in b'\x01':

            (h1f, h1, h2f, h2, h3f, h3, h4f, h4) = struct.unpack(
                r">BHBHBHBH", body[3:])

            # if (h1f != 0) or (h2f != 0) or (h3f != 0) or (h4f != 0):
            #     print(HexDump(body))
            # if (h1f != 0) :
            #     print(HexDump(body))

            return [
                h1/100,
                h2/100,
                h3/100,
                h4/100,
            ]

    def onOpen(self, opts=None):
        self.tt.Run()

    def onClose(self):
        self.sendPackage(b"\x00")
        self.tt.Stop()
        pass

    def onClock(self):
        self.sendPackage(b"\x01")


if __name__ == '__main__':
    a = b'\x01\x01\x01\x00\x08\xfc\x10\x00\x00\x10\x00\x00\x10\x00\x00'

    print("{0}".format(USB_Temp_Monitor.parsePkg(a)))
