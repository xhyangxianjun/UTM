import struct

import timer

from ..base import BaseProtocol, Btn_Func, Btn_Func_Dir, Btn_Input, Btn_Input_Opt
from ..utils import HexDump


class MotorPluse(BaseProtocol):
    Device = "MotorPluse"
    Name = "电机脉冲运放采样"
    Description = ""
    xAxis = [{
        "Name": "脉冲频率",
        "ID": "Pluse",
        "Scale": 1,
    }, {
        "Name": "负载控制字",
        "ID": "Load_Ctl",
        "Scale": 1,
    }, {
        "Name": "PWM",
        "ID": "PWm",
        "Scale": 1,
    }, {
        "Name": "设置累计脉冲",
        "ID": "Set_Total_Pluse",
        "Scale": 1,
    }, {
        "Name": "设置累计时间",
        "ID": "Set_Total_Time",
        "Scale": 1,
    }, {
        "Name": "累计时间",
        "ID": "Total_Time",
        "Scale": 1,
    }, {
        "Name": "累计脉冲",
        "ID": "Total_Pluse",
        "Scale": 1,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=1, acc=0.01, fn=self.onClock)
        self.M_Btn: Btn_Func_Dir = [
            Btn_Func("停止", self.Motor_Stop),
            Btn_Input(
                "PWM控制，一直开",
                self.Motor_Run_Always_Custom,
                "驱动方式：PWM\r\n一直开着",
                [
                    Btn_Input_Opt("占空比", 100),
                    Btn_Input_Opt("周期", 100),
                ]),
            Btn_Input(
                "自定义",
                self.Motor_Run_Pluse_on_custom,
                "驱动方式：PWM\r\n到达规定脉冲数停止出水",
                [
                    Btn_Input_Opt("占空比", 100),
                    Btn_Input_Opt("脉冲数", 20000),
                ]),
            Btn_Func_Dir("测试 PWM 脉冲数 5000", [
                Btn_Func("10", self.Motor_Run_Pluse(10, 5000)),
                Btn_Func("20", self.Motor_Run_Pluse(20, 5000)),
                Btn_Func("30", self.Motor_Run_Pluse(30, 5000)),
                Btn_Func("40", self.Motor_Run_Pluse(40, 5000)),
                Btn_Func("50", self.Motor_Run_Pluse(50, 5000)),
                Btn_Func("60", self.Motor_Run_Pluse(60, 5000)),
                Btn_Func("70", self.Motor_Run_Pluse(70, 5000)),
                Btn_Func("80", self.Motor_Run_Pluse(80, 5000)),
                Btn_Func("90", self.Motor_Run_Pluse(90, 5000)),
                Btn_Func("100", self.Motor_Run_Pluse(100, 5000)),
            ]),
            Btn_Func_Dir("定时器", [
                Btn_Func("启动", self.tt.Run),
                Btn_Func("停止", self.tt.Stop),
                Btn_Input(
                    "设置参数",
                    None,
                    "设置定时器参数",
                    [
                        Btn_Input_Opt("间隔时间（毫秒）", 100),
                    ]),
            ]),
        ]

    def Motor_Run_Always_Custom(self, event):
        self.Motor_Run_Always(event["占空比"], event["周期"])()

    def Motor_Run_Always(self, pwm_set=100, pwm_p=100):
        def aaa():
            self.sendPackage(b"\x02"+struct.pack(
                r">BHH",
                0x01,
                pwm_set,
                pwm_p,
            ))
        return aaa

    def Motor_Stop(self):
        self.sendPackage(b"\x02\x00\x00\x00\x00")

    def Motor_Run_Pluse_on_custom(self, event):
        self.Motor_Run_Pluse(event["占空比"], event["脉冲数"])()

    def Motor_Run_Pluse(self, pwm_set, pluse_set):
        def aaa():
            self.sendPackage(b"\x02"+struct.pack(
                r">BHHH",
                0xD3,
                pwm_set,
                pluse_set,
                0,
            ))
        return aaa

    def Motor_Run_Time(self, pwm_set, time_set):
        def aaa():
            self.sendPackage(b"\x02"+struct.pack(
                r">BHHH",
                0xD4,
                pwm_set,
                0,
                time_set,
            ))
        return aaa

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
                _,
                脉冲频率,
                负载控制字,
                PWM,
                设置累计脉冲, 设置累计时间,
            ) = struct.unpack(r">HHBHhH", body[p:p+11])

            return [
                脉冲频率/10,
                负载控制字,
                PWM/4095*5,
                设置累计脉冲, 设置累计时间/10,
            ]

        else:
            print(HexDump(body))

        return []
