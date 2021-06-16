
import timer

from ..base import BaseProtocol, Btn_Func, Btn_Func_Dir


class T8775(BaseProtocol):
    Device = "Tool8775C1"
    Name = "电参8775C1"
    Description = "实验室电参"
    xAxis = [{
        "Name": "电压",
        "ID": "kV",
        "Scale": 1,
    }, {
        "Name": "电流",
        "ID": "I",
        "Scale": 1,
    }, {
        "Name": "功率",
        "ID": "P",
        "Scale": 1,
    }, {
        "Name": "电能",
        "ID": "W",
        "Scale": 1,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.type = BaseProtocol.ProtocolType_T87_RS232
        self.tt = timer.Timer(delay=0.2, acc=0.001, fn=self.onClock)

        self.M_Btn = [
            Btn_Func("重新启动电能累计", self.Clear_Total_W),
        ]

    def Clear_Total_W(self):
        self.sendPackageRaw(b"\x11\x02\x30\x30\x31")
        self.sendPackageRaw(b"\x11\x03\x30\x30\x31")
        self.sendPackageRaw(b"\x11\x01\x30\x30\x31")

    def parsePkg(self, body):
        # print(body)
        # print(HexDump(body))

        Addr = int(body[0:3])

        # print("Addr: {0}".format(Addr))
        V = float(body[3:8])
        V_Unit = body[8:10]
        I = float(body[10:15])
        I_Unit = body[15:17]
        P = float(body[17:22])
        P_Unit = body[22:24]

        W = float(body[45:52])
        W_Unit = body[52:55]

        if V_Unit == b"\x20V":
            pass
        elif V_Unit == b"mV":
            V *= 1000
        elif V_Unit == b"kV":
            V /= 1000

        if I_Unit == b" A":
            pass
        elif I_Unit == b"mA":
            I /= 1000
        # else:
        #     I = ""

        if P_Unit == b"\x20W":
            pass
        elif P_Unit == b"kW":
            P *= 1000
        else:
            P = ""

        if W_Unit == b"\x20Wh":
            W /= 1000
        elif W_Unit == b"kWh":
            pass
        elif W_Unit == b"MWh":
            W *= 1000

        return [
            int(V/100)/100,
            int(I*100)/100,
            int(P*100)/100,
            int(W*10000)/10000,
        ]

    def onOpen(self, opts=None):
        self.tt.Run()

    def onClose(self):
        self.tt.Stop()

    def onClock(self):
        self.sendPackageRaw(b"\x10\x03\x30\x30\x31")
