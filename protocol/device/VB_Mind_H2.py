import struct

import timer
import time

from ..base import BaseProtocol, Btn_Func, Btn_Func_Dir

from ..utils import HexDump


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
        "Name": "AC电压",
        "ID": "AC_V",
        "Scale": 0.5,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=1, acc=0.01, fn=self.onClock)
        self.M_Btn = [
            Btn_Func("停止出水", self.btn_test_0),
            Btn_Func("测试 常温 25℃ 250mL", self.btn_test_1(25, 20)),
            Btn_Func_Dir("测试 加热 250mL", [
                Btn_Func("45℃", self.btn_test_1(45, 20)),
                Btn_Func("55℃", self.btn_test_1(55, 20)),
                Btn_Func("65℃", self.btn_test_1(65, 20)),
                Btn_Func("75℃", self.btn_test_1(75, 20)),
                Btn_Func("85℃", self.btn_test_1(85, 20)),
                Btn_Func("90℃", self.btn_test_1(90, 20)),
                Btn_Func("94℃", self.btn_test_1(94, 20)),
                Btn_Func("95℃", self.btn_test_1(95, 20)),
                Btn_Func("98℃", self.btn_test_1(98, 20)),
                Btn_Func("99℃", self.btn_test_1(99, 20)),
                Btn_Func("100℃", self.btn_test_1(100, 20)),
            ]),
            Btn_Func_Dir("定时器发送", [
                Btn_Func("启动", self.tt.Run),
                Btn_Func("停止", self.tt.Stop),
                Btn_Func("参数 1秒 01-00-0A",
                         self.set_timer_interval_cmd(1, b"\x01\x00\x0A")),
            ]),
            Btn_Func("读取预存数据", self.read_Pre_Data),
        ]

    def btn_test_0(self):
        self.sendPackage(b"\xD0\x00")

    def set_timer_interval_cmd(self, interval, cmd):
        self.tt.delay = interval

        def aaa():
            self.sendPackage(cmd)
        self.tt.fn = aaa

    def btn_test_1(self, Water_Temp_Set, Set_Water_mil=0):

        def aaa():
            self.sendPackage(
                b"\xD1"+struct.pack(
                    r">BB",
                    Water_Temp_Set,
                    Set_Water_mil,
                ))
        return aaa

    def parsePkg(self, body):
        p = 0

        M = []

        (cmd,) = struct.unpack(r">B", body[p:p+1])
        # M[0] = cnt

        if cmd == 0x03:

            # print(HexDump(body))
            (
                入水口温度, 出水口温度,
                水泵PWM,
                设定温度,
                可控硅导通计数,
                传感器状态,
                预热微调强度,
                斜率,
                AC电压,
            ) = struct.unpack(r">BBHBBBHbB", body[p+3:p+14])
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
            ]
            return M

        elif cmd == 0x04:

            (
                预热微调时间,
                水泵PWM,
                page_cnt,
                可控硅导通计数,
            ) = struct.unpack(r">HHBB", body[p+3:p+9])

            (
                AC电压,
            ) = struct.unpack(r">B", body[p+13:p+14])

            M = [
                0,
                0,
                水泵PWM,
                0,
                可控硅导通计数,
                0,
                0,
                0,
                AC电压,
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

    def read_Pre_Data(self):
        self.sendPackage(b"\x02\x10\x00")