import struct

import timer

from ..base import (
    BaseProtocol,
)
from ..utils import HexDump


class TDS_AB(BaseProtocol):
    Device = "TDS_AB"
    Name = "TDS正反测定"
    Description = ""
    xAxis = [{
        "Name": "AD",
        "ID": "AD",
        "Scale": 1,
    }, {
        "Name": "TDS",
        "ID": "TDS",
        "Scale": 1,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=0.1, acc=0.01, fn=self.onClock)

    def onOpen(self):
        self.tt.Run()
        pass

    def onClock(self):
        self.sendPackage(b"\x01\x00\x0A")

    def onClose(self):
        self.tt.Stop()

    def parsePkg(self, body):

        p = 0
        (cmd,) = struct.unpack(r">B", body[p:p+1])
        p += 1

        if cmd == 0x01:
            # print(HexDump(body))
            (
                AD,
                TDS,
            ) = struct.unpack(r">HH", body[p:p+4])

            return [
                AD, TDS,
            ]

        else:
            print(HexDump(body))

        return []
