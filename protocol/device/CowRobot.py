import struct

import timer
import math

from ..base import BaseProtocol, Btn_Func, Btn_Func_Dir, Btn_Input, Btn_Input_Opt
from ..utils import HexDump


class CowRobot(BaseProtocol):
    Device = "CowRobot"
    Name = "CowRobot"
    Description = ""
    xAxis = [{
        "Name": "电机角度",
        "ID": "Angle",
        "Scale": 1,
    }, {
        "Name": "电机角度Sin",
        "ID": "Angle_Sin",
        "Scale": 1,
    }, {
        "Name": "转速",
        "ID": "Rotating_Speed",
        "Scale": 1,
    }, {
        "Name": "电机角度(弧度)",
        "ID": "Angle_Rad",
        "Scale": 1,
    }, {
        "Name": "电机速度等级",
        "ID": "SpeedLevel",
        "Scale": 1,
    }, {
        "Name": "AD0",
        "ID": "AD0",
        "Scale": 1,
    }, {
        "Name": "AD1",
        "ID": "AD1",
        "Scale": 1,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=0.2, acc=0.01, fn=self.onClock)
        self.M_Btn = [
            Btn_Func("正转 0x00", self.Motor_Direct(0x00)),
            Btn_Func("反转 0x01", self.Motor_Direct(0x01)),
            Btn_Func("停转 0x02", self.Motor_Direct(0x02)),
            Btn_Func("最大速度 0", self.Motor_Speed(0x00)),
            Btn_Func("速度:1 speed=10", self.Motor_Speed(10)),
            Btn_Func("速度:2 spedd=20", self.Motor_Speed(20)),
            Btn_Func("速度:3 speed=30", self.Motor_Speed(30)),
            Btn_Input(
                "自定义速度",
                self.Motor_Speed_Custom,
                "设定速度，单位：1ms/step\n0:5ms",
                [
                    Btn_Input_Opt("速度", 0),
                ]),
            Btn_Input(
                "转动方向",
                self.Motor_Direct_Custom,
                "设定转动方向\t0:正转\t1:正转\t2:停转\t",
                [
                    Btn_Input_Opt("方向", 0),
                ]),
        ]

    def Motor_Speed_Custom(self, event):
        self.Motor_Speed(event["速度"])()

    def Motor_Direct_Custom(self, event):
        self.Motor_Direct(event["方向"])()

    def Motor_Speed(self, speed):
        def aaa():
            self.sendPackage(b'\x03' + struct.pack(
                r">BB",
                0x10,
                speed,
            ))
        return aaa

    def Motor_Direct(self, direct):
        def aaa():
            self.sendPackage(b'\x03' + struct.pack(
                r">BB", 0x11, direct))
        return aaa

    def onOpen(self):
        # self.tt.Run()
        pass

    def onClock(self):
        self.sendPackage(b"\x01\x00\x0A")

    def onClose(self):
        self.tt.Stop()

    def parsePkg(self, body):

        p = 0
        (cmd, ) = struct.unpack(r">B", body[p:p+1])
        p += 1

        if cmd == 0x02:
            (
                Angle,
                Angle_Sin,
                Rotating_Speed,
                SpeedLevel,
                AD0, AD1,
            ) = struct.unpack(r">HhhBHH", body[p:p+11])

            return [
                Angle/100,
                Angle_Sin/100,
                Rotating_Speed/100,
                int(math.sin(Angle/100/180*math.pi)*100)/100,
                SpeedLevel,
                AD0, AD1,
            ]

        return []
