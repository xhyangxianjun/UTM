import struct

import timer
import time

from protocol import BaseProtocol
from protocol import HexDump


class VB_Mind_H2(BaseProtocol):
    Device = "VB_Mind_H2"
    Name = "H2_VB_Mind-调试通讯协议"
    Description = "VB_Mind_H2"
    xAxis = [{
        "Name": "温度-入水口",
        "ID": "Water_Temp_In",
        "Scale": 1,
    }, {
        "Name": "温度-出水口",
        "ID": "Water_Temp_Out",
        "Scale": 1,
    }, {
        "Name": "水泵PWM",
        "ID": "Bump_PWM_Duty",
        "Scale": 0.1,
    }, {
        "Name": "设定温度",
        "ID": "Water_Temp_Set",
        "Scale": 1,
    }, {
        "Name": "可控硅导通计数",
        "ID": "KeKongGui_DaoTon_Count",
        "Scale": 5,
    }, {
        "Name": "传感器状态",
        "ID": "All_Bit",
        "Scale": 1,
    }, {
        "Name": "预热微调强度",
        "ID": "Contorl_XieLv_GuoChong_QiangDu",
        "Scale": 1,
    }, {
        "Name": "斜率",
        "ID": "K",
        "Scale": 0.1,
    }, {
        "Name": "交流电压",
        "ID": "AC_V",
        "Scale": 0.5,
    }, {
        "Name": "查表交流电压",
        "ID": "AC_V",
        "Scale": 0.5,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=1, acc=0.1, fn=self.onClock)
        

    def parsePkg(self, body):
        # print(HexDump(body))
        p = 0

        M = [0, 0, 0, 0]

        (cmd, cnt) = struct.unpack(r">BH", body[p:p+3])
        p += 3
        # M[0] = cnt

        if cmd == 0x01:

            (
                入水口温度, 出水口温度,
                水泵PWM,
                设定温度,
                可控硅导通计数,
                传感器状态,
                预热微调强度,
                斜率,
                AC电压,
                查表AC电压,
            ) = struct.unpack(r">BBHBBBHBHH", body[p:p+14])
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
                入水口温度,
                出水口温度,
                水泵PWM,
                设定温度,
                可控硅导通计数,
                传感器状态,
                预热微调强度,
                斜率,
                AC电压,
                查表AC电压,
            ]
            return M

        elif cmd == 0x02:

            (
                预热微调时间,
                水泵PWM,
            ) = struct.unpack(r">HH", body[p:p+4])
            

            M = [
                0,
                0,
                水泵PWM,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ]
            return M

        return M

    def onOpen(self, opts=None):
        # self.sendPackage(b"\x00")
        # time.sleep(0.1)
        # self.sendPackage(b"\x01\x00\x01")
        # self.sendPackage(b"\x00\x00\00")
        # self.tt.Run()
        self.sendPackage(b"\x02\x10\x00")

    def onClose(self):
        self.sendPackage(b"\x00")
        self.tt.Stop()

    def onClock(self):
        # self.sendPackage(b"\x00")
        # time.sleep(1)
        self.sendPackage(b"\x01\x00\x01")
