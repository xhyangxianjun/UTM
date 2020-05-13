from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QDialog,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,

    QMessageBox
)
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QFontMetrics,
)

import sys
import serial.tools.list_ports
import protocol

import config


class SerialSettingWindow(QDialog):
    def __init__(self, parent=None):
        super(SerialSettingWindow, self).__init__(parent)
        # super().__init__()

        
        try:
            config.loadConfig()
        except FileNotFoundError as e:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            s = "{0}\r\n".format(e)
            s += "点击确定开始配置"
            msgBox.setText(s)
            msgBox.setWindowTitle("找不到配置文件")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            config.CFG.data = config.default_config

        self.setMinimumSize(300, 10)

        self.setWindowTitle("串口参数设置")
        # self.setWindowModality(Qt.ApplicationModal)
        # self.setWindowFlags(
        #     Qt.WindowCloseButtonHint |
        #     Qt.MSWindowsFixedSizeDialogHint |
        #     Qt.Tool
        # )
        # self.resize(300, 200)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        # vbox.setSpacing(0)
        # vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        # button1 = QPushButton('button1', self)
        # button1.setToolTip('This is an example button')
        # hbox.addWidget(button1)
        # self.main_widget = MainWidget(self)
        # self.setCentralWidget(MainWidget(self))

        portWidget = QWidget()
        vbox.addWidget(portWidget)
        hbox = QHBoxLayout()
        # hbox.setMargin(0)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        portWidget.setLayout(hbox)

        portLabel = QLabel()
        portLabel.setText("端口")
        hbox.addWidget(portLabel)

        self.combobox_1 = QComboBox(self)
        self.combobox_1.setEditable(True)

        self.refreshPortList()
        # def fn1(tag):
        #     print("self.combobox_1.currentTextChanged {0}".format(tag))
        # self.combobox_1.currentTextChanged.connect(fn1)
        # def fn2(tag):
        #     print("self.combobox_1.currentIndexChanged {0}".format(tag))
        # self.combobox_1.currentIndexChanged.connect(fn2)
        # self.combobox_1.setEditText("Fuuuuuck")
        hbox.addWidget(self.combobox_1)

        refreshPortBtn = QPushButton()
        refreshPortBtn.setText("刷新")
        fm = QFontMetrics(refreshPortBtn.font())
        # refreshPortBtn.setFixedWidth(fm.width(refreshPortBtn.text()))
        refreshPortBtn.setMaximumWidth(fm.width(refreshPortBtn.text())+10)
        refreshPortBtn.clicked.connect(self.refreshPortList)
        hbox.addWidget(refreshPortBtn)

        baudWidget = QWidget()
        vbox.addWidget(baudWidget)
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        baudWidget.setLayout(hbox)
        baudLabel = QLabel()
        baudLabel.setText("波特率")
        hbox.addWidget(baudLabel)
        baudCombobox = QComboBox(self)
        hbox.addWidget(baudCombobox)
        baudCombobox.setEditable(True)

        baudList = [
            "50", "75", "110", "134", "150", "200", "300", "600",
            "1200", "1800", "2400", "4800", "9600",
            "19200", "38400", "57600", "115200"]

        baudCombobox.addItems(baudList)
        try:
            baudCombobox.setEditText("{}".format(
                config.CFG.data["serial"]["baud"]))
            for k,v in enumerate(baudList):
                if int(v) == config.CFG.data["serial"]["baud"]:
                    baudCombobox.setCurrentIndex(k)
        except KeyError as e:
            pass

        deviceTypeWidget = QWidget()
        vbox.addWidget(deviceTypeWidget)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        deviceTypeWidget.setLayout(hbox)
        deviceTypeLabel = QLabel()
        deviceTypeLabel.setText("设备类型")
        hbox.addWidget(deviceTypeLabel)
        deviceTypeCombobox = QComboBox(self)
        hbox.addWidget(deviceTypeCombobox)
        deviceTypeCombobox.setEditable(True)
        # deviceTypeCombobox.addItems([
        #     "USB测温仪",
        #     "VB_Mid_H2",
        #     "测试设备1",
        #     "测试设备2",
        #     "测试设备3",
        #     "测试设备4",
        #     "测试设备5",
        # ])
        for a in protocol.M:
            deviceTypeCombobox.addItem(a.Name)

        try:
            cfgDeviceType = config.CFG.data["serial"]["deviceType"]
            deviceTypeCombobox.setEditText(
                "{}".format(cfgDeviceType))
            for i, a in enumerate(protocol.M):
                    if a.Device == cfgDeviceType:
                        deviceTypeCombobox.setCurrentIndex(i)
                        break
        except KeyError as e:
            pass

        OKBtn = QPushButton()
        OKBtn.setText("确定")

        def fn():
            s = self.combobox_1.currentText()
            for a in self.l:
                if "{}".format(a) == s:
                    s = a.device
            if config.CFG.data.get("serial", None) is None:
                config.CFG.data["serial"] = {}
            config.CFG.data["serial"]["port"] = s
            config.CFG.data["serial"]["baud"] = int(baudCombobox.currentText())

            s = deviceTypeCombobox.currentText()
            for a in protocol.M:
                if a.Name == s:
                    s = a.Device
            config.CFG.data["serial"]["deviceType"] = s
            config.saveConfig()
            self.accept()
        OKBtn.clicked.connect(fn)
        vbox.addWidget(OKBtn)

    def refreshPortList(self):
        self.l = serial.tools.list_ports.comports()
        if len(self.l) == 0:
            return
        model = QStandardItemModel()
        for a in self.l:
            it = QStandardItem()
            it.setText("{0}".format(a))
            it.setData(a, Qt.ForegroundRole)
            model.appendRow(it)
        # self.combobox_1.clear()
        self.combobox_1.setModel(model)
        try:
            currentPort = config.CFG.data["serial"]["port"]
            if not currentPort is None:
                self.combobox_1.setEditText(currentPort)
                for i, a in enumerate(self.l):
                    if a.device == currentPort:
                        self.combobox_1.setCurrentIndex(i)
                        break
        except KeyError as e:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qb = SerialSettingWindow()
    qb.show()
    sys.exit(app.exec_())
