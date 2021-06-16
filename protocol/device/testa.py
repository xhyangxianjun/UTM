import struct

import timer
import time

from ..base import BaseProtocol, Btn_Func, Btn_Func_Dir

from ..utils import HexDump


class testA(BaseProtocol):
    Device = "TestA"
    Name = "测试A"
    Description = "VB_Mind_H2"
    xAxis = [
        {"Name": "CH1", "ID": "CH1", "Scale": 1, },
        {"Name": "CH2", "ID": "CH2", "Scale": 1, },
        {"Name": "CH3", "ID": "CH3", "Scale": 1, },
        {"Name": "CH4", "ID": "CH4", "Scale": 1, },
        {"Name": "CH5", "ID": "CH5", "Scale": 1, },
        {"Name": "CH6", "ID": "CH6", "Scale": 1, },
        {"Name": "CH7", "ID": "CH7", "Scale": 1, }
    ]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=1, acc=0.01, fn=self.onClock)
        self.M_Btn = []

    def parsePkg(self, body):
        p = 0

        M = []

        (cmd,) = struct.unpack(r">B", body[p:p+1])
        # M[0] = cnt

        if cmd == 0x01:

            # print(HexDump(body))
            (
                CH1,
                CH2,
                CH3,
                CH4,
                CH5,
                CH6,
                CH7,
            ) = struct.unpack(r">HHHHHHH", body[p+3:p+17])
            p += 11

            # 01 cmd
            # 0F F8 cnt
            # 1B 入水口温度
            # 2B 出水口温度
            # 00 00 水泵PWM
            # 5E 设定温度
            # 00 可控硅导通计数
            # 01 传感器状态
            # 00 28 预热微调强度
            # 00 斜率

            M = [
                CH1,
                CH2,
                CH3,
                CH4,
                CH5,
                CH6,
                CH7,
            ]
            return M
        return []

    def onOpen(self, opts=None):
        self.sendPackage(b"\x00")
        time.sleep(0.5)
        # self.sendPackage(b"\x01\xFF\xFF")
        # self.sendPackage(b"\x00\x00\00")
        # self.tt.Run()
        # self.sendPackage(b"\x02\x10\x00")
        pass

    def onClose(self):
        self.sendPackage(b"\x00")
        self.tt.Stop()

    def onClock(self):
        # self.sendPackage(b"\x00")
        # time.sleep(1)
        self.sendPackage(b"\x01\x00\x0A")
