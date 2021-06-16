import timer

from ..base import BaseProtocol


class TestMath(BaseProtocol):
    Device = "TestMathSin"
    Name = "测试数据三角函数"
    Description = ""
    xAxis = [{
        "Name": "Sin",
        "ID": "CH1",
        "Scale": 1,
    }, {
        "Name": "Cos",
        "ID": "CH2",
        "Scale": 1,
    }, {
        "Name": "Sin10",
        "ID": "CH3",
        "Scale": 1,
    }, {
        "Name": "Cos10",
        "ID": "CH4",
        "Scale": 1,
    }]

    def __init__(self, serial):
        super().__init__(serial)
        self.tt = timer.Timer(delay=0.2, acc=0.001, fn=self.onClock)

    def parsePkg(self, body):
        pass

    def onOpen(self, opts=None):
        pass

    def onClose(self):
        pass

    def onClock(self):
        pass
