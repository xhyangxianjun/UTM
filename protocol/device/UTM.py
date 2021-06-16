import struct
from typing import List

import timer

from ..base import BaseProtocol, XAxis


class USB_Temp_Monitor(BaseProtocol):
    Device = "UTM"
    Name = "USB温度监控仪"
    Description = ""
    xAxis = [
        {"Name": "通道1", "ID": "CH1", "Scale": 1},
        {"Name": "通道2", "ID": "CH2", "Scale": 1},
        {"Name": "通道3", "ID": "CH3", "Scale": 1},
        {"Name": "通道4", "ID": "CH4", "Scale": 1},
        {"Name": "错误1", "ID": "Er1", "Scale": 1},
        {"Name": "错误2", "ID": "Er2", "Scale": 1},
        {"Name": "错误3", "ID": "Er3", "Scale": 1},
        {"Name": "错误4", "ID": "Er4", "Scale": 1},
    ]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=0.1, acc=0.1, fn=self.onClock)

    def parsePkg(self, body):

        # print(HexDump(body))

        (cmd, seq) = struct.unpack(r">BH", body[:3])

        # print("cmd {0:02X} seq {1:04X} ".format(cmd, seq))

        if cmd == 0x01:

            chs = [0, 0, 0, 0]
            ers = [0, 0, 0, 0]

            (
                ers[0], chs[0],
                ers[1], chs[1],
                ers[2], chs[2],
                ers[3], chs[3],
            ) = struct.unpack(
                r">BHBHBHBH", body[3:])

            ret = [
                chs[0]/100,
                chs[1]/100,
                chs[2]/100,
                chs[3]/100,
            ]

            # for k, v in enumerate(ers):
            #     if v != 0:
            #         ret[k] = ""
            ret.extend(ers)
            return ret
        return []

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
