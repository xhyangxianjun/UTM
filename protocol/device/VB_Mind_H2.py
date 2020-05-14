import struct

from protocol import BaseProtocol
from protocol import HexDump


class VB_Mind_H2(BaseProtocol):
    Device = "VB_Mind_H2"
    Name = "H2_VB_Mind-调试通讯协议"
    Description = "VB_Mind_H2"
    xAxis = [
        {"Name": "温度,入水口"},
        {"Name": "温度,出水口"},
        {"Name": "Bump_PWM_Duty"},
        {"Name": "Water_Temp_Set"},
        {"Name": "KeKongGui_DaoTon_Count"},
        {"Name": "All_Bit"},
        {"Name": "PID_P"},
        {"Name": "PID_I"},
        {"Name": "K"}
    ]

    def __init__(self, serial):
        super().__init__(serial)

    def parsePkg(self, body):
        # print("Fuuuuck {0}".format(body))
        # print(HexDump(body))

        M = [0, 0, 0, 0]

        (cmd, cnt) = struct.unpack(r">BH", body[:3])
        # M[0] = cnt

        if cmd == 0x01:

            (入水口温度, 出水口温度, 水泵PWM, 设定温度, 可控硅导通计数, 传感器状态,
             预热微调强度) = struct.unpack(r">BBHBBBH", body[3:12])
            M[0] = 入水口温度
            M[1] = 出水口温度
            M[2] = 水泵PWM
            M[3] = 设定温度

        return M

    def onOpen(self, opts=None):
        # self.sendPackage(b"\x00\x00\00")
        self.sendPackage(b"\x01\x10\x00")

    def onClose(self):
        self.sendPackage(b"\x00")
