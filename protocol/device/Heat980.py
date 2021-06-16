import struct

import timer

from ..base import BaseProtocol, Btn_Func, Btn_Func_Dir, Btn_Input, Btn_Input_Opt
from ..utils import HexDump


class Heat980(BaseProtocol):
    Device = "Heat980"
    Name = "加热机980"
    Description = ""
    xAxis = [{
        "Name": "热罐温度",
        "ID": "Temp1",
        "Scale": 1,
    }, {
        "Name": "热罐温度斜率",
        "ID": "Temp1_K",
        "Scale": 1,
    }, {
        "Name": "当地沸点",
        "ID": "Boiling_Point",
        "Scale": 1,
    }, {
        "Name": "加热模式",
        "ID": "Heat_Step",
        "Scale": 1,
    }, {
        "Name": "加热状态",
        "ID": "Heat_State",
        "Scale": 1,
    }, {
        "Name": "全功率加热",
        "ID": "Total_Time",
        "Scale": 1,
    }, {
        "Name": "保温加热",
        "ID": "Total_Pluse",
        "Scale": 1,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=0.2, acc=0.01, fn=self.onClock)
        self.M_Btn: Btn_Func_Dir = [
            Btn_Func_Dir("head_step", [
                Btn_Func("3. KEEP_WARM", self.HeadStep(0x03)),
                Btn_Func("4. HEATING", self.HeadStep(0x04)),
                Btn_Func("5. NOHEATING", self.HeadStep(0x05)),
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

    def HeadStep(self, step):
        def aaa():
            self.sendPackage(b"\x02"+struct.pack(
                r">BB",
                0x20,
                step,
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

        # print(HexDump(body))
        p = 0
        (cmd, _) = struct.unpack(r">BH", body[p:p+3])
        p += 3

        if cmd == 0x01:
            (
                热罐温度,
                热罐温度斜率,
                当地沸点,
                加热模式,
                加热状态,
                全功率加热,
                保温加热,
            ) = struct.unpack(r">BBBBBBB", body[p:p+7])

            return [
                热罐温度,
                热罐温度斜率,
                当地沸点,
                加热模式,
                加热状态,
                全功率加热,
                保温加热,
            ]

        else:
            print(HexDump(body))

        return []
