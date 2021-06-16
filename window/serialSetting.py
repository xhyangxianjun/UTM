from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QApplication,QMainWindow,QDialog,QComboBox,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QListWidget,QTableWidget,QTableWidgetItem,QHeaderView,QAbstractItemView,QMessageBox
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QFontMetrics

import sys
import serial.tools.list_ports
import protocol

import config


class SerialSettingWindow(QDialog):
    def __init__(self, parent=None):
        self.device_list = {}
        self.device_list_current_item_text = None
        self.l = None

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

        self.device_list = config.CFG.data["serial"]

        self.setMinimumSize(300, 100)

        self.setWindowTitle("串口参数设置")
        # self.setWindowModality(Qt.ApplicationModal)
        # self.setWindowFlags(
        #     Qt.WindowCloseButtonHint |
        #     Qt.MSWindowsFixedSizeDialogHint |
        #     Qt.Tool
        # )
        # self.resize(300, 200)
        self.initUI()
        # for i in protocol.M:
        #     self.deviceListW.addItem(i.Name)
        for k, v in enumerate(self.device_list):
            self.deviceListW.addItem(self.device_list[k]["name"])

        self.resize(600, 500)

    def getCurDeviceCfg(self):
        for v in self.device_list:
            if v["name"] == self.device_list_current_item_text:
                return v

    def setCurDeviceCfg(self, val):
        for k, v in enumerate(self.device_list):
            if v["name"] == self.device_list_current_item_text:
                self.device_list[k] = val
                return

    def listwidgetclicked(self, item):
        if self.device_list_current_item_text == item.text():
            return
        self.device_list_current_item_text = item.text()
        self.switchDevice(self.device_list_current_item_text)

    def on_add_device(self):
        ii = 0
        while(True):
            ii += 1
            dName = "设备{0}".format(ii)
            is_already = False
            for v in self.device_list:
                if dName == v['name']:
                    is_already = True
                    break
            if not is_already:
                self.add_default_device(dName)
                break

    def add_default_device(self, name):
        cloneCfg = config.default_config_device.copy()
        cloneCfg["name"] = name
        self.add_device(cloneCfg)

    def add_device(self, val):
        self.device_list.append(val)
        self.deviceListW.addItem(val["name"])

    def delete_device(self):
        cr = self.deviceListW.currentItem()
        cri = self.deviceListW.currentRow()
        if cr is None:
            return
        # if len(self.device_list.keys()) == 1:
        #     return
        self.deviceListW.takeItem(cri)
        del self.device_list[cri]

    def initUI_rw(self):
        self.rightWidget.setParent(None)
        self.rightWidget = QWidget()
        self.hbox.addWidget(self.rightWidget)
        self.hbox.setStretchFactor(self.rightWidget, 4)
        rvbox = QVBoxLayout()

        rvbox.setSpacing(0)
        rvbox.setContentsMargins(0, 0, 0, 0)
        self.rightWidget.setLayout(rvbox)

        DeviceNameWidget = QWidget()
        rvbox.addWidget(DeviceNameWidget)
        hbox = QHBoxLayout()
        DeviceNameWidget.setLayout(hbox)

        DeviceNameLabel = QLabel()
        hbox.addWidget(DeviceNameLabel)
        DeviceNameLabel.setText("名称:")
        hbox.addStretch()
        self.DeviceNameText = QLabel()
        hbox.addWidget(self.DeviceNameText)
        self.DeviceNameText.setText("NaN")

        # 设备类型
        DeviceTypeWidget = QWidget()
        rvbox.addWidget(DeviceTypeWidget)
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        DeviceTypeWidget.setLayout(hbox)
        DeviceTypeLabel = QLabel()
        hbox.addWidget(DeviceTypeLabel)
        DeviceTypeLabel.setText("类型:")
        # hbox.addStretch()
        self.DeviceTypeComboBox = QComboBox(self)
        # self.DeviceTypeComboBox.setEditable(True)
        hbox.addWidget(self.DeviceTypeComboBox)

        # 设备端口
        DevicePortWidget = QWidget()
        rvbox.addWidget(DevicePortWidget)
        hbox = QHBoxLayout()
        DevicePortWidget.setLayout(hbox)
        DevicePortLabel = QLabel()
        hbox.addWidget(DevicePortLabel)
        DevicePortLabel.setText("端口:")
        # hbox.addStretch()
        refreshPortBtn = QPushButton()
        refreshPortBtn.setText("刷新")
        fm = QFontMetrics(refreshPortBtn.font())
        refreshPortBtn.setMaximumWidth(fm.width(refreshPortBtn.text())+10)
        refreshPortBtn.clicked.connect(self.refreshPortList)
        hbox.addWidget(refreshPortBtn)
        self.DevicePortListComboBox = QComboBox(self)
        self.DevicePortListComboBox.setEditable(True)
        hbox.addWidget(self.DevicePortListComboBox)

        # 波特率
        DeviceBaudWidget = QWidget()
        rvbox.addWidget(DeviceBaudWidget)
        hbox = QHBoxLayout()
        DeviceBaudWidget.setLayout(hbox)
        DeviceBaudLabel = QLabel()
        hbox.addWidget(DeviceBaudLabel)
        DeviceBaudLabel.setText("波特率:")
        # hbox.addStretch()
        self.DeviceBaudComboBox = QComboBox(self)
        self.DeviceBaudComboBox.setEditable(True)
        hbox.addWidget(self.DeviceBaudComboBox)

        # 通道选择
        DeviceChanWidget = QWidget()
        rvbox.addWidget(DeviceChanWidget)
        hbox = QHBoxLayout()
        DeviceChanWidget.setLayout(hbox)
        DeviceChanLabel = QLabel()
        hbox.addWidget(DeviceChanLabel)
        DeviceChanLabel.setText("通道:")
        # hbox.addStretch()

        self.DeviceChannTaable = QTableWidget()
        hbox.addWidget(self.DeviceChannTaable)
        self.DeviceChannTaable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        def onCellChanged(row, column):
            selected_chann = []
            for k, v in enumerate(self.getCurrentDeviceEx().xAxis):
                it = self.DeviceChannTaable.item(k, 0)

                if it is None:
                    return
                if it.checkState():
                    selected_chann.append(k)
            self.getCurDeviceCfg()["chann"] = selected_chann
        self.DeviceChannTaable.cellChanged.connect(onCellChanged)

        # rvbox.addStretch()

    def getDeviceTypeEx(self, cur):
        for a in protocol.M:
            if a.Name == cur:
                return a
        for a in protocol.M:
            if a.Device == cur:
                return a
        return None

    def getCurrentDeviceEx(self):
        return self.getDeviceTypeEx(self.getCurDeviceCfg()["deviceType"])

    def switchChannTable(self, prot):
        if prot is None:
            return

        self.DeviceChannTaable.setRowCount(len(prot.xAxis))

        for k, v in enumerate(prot.xAxis):
            chk = QTableWidgetItem(v["Name"])

            if k in self.getCurDeviceCfg()["chann"]:
                chk.setCheckState(Qt.Checked)
            else:
                chk.setCheckState(Qt.Unchecked)

            self.DeviceChannTaable.setItem(k, 0, chk)
            self.DeviceChannTaable.setItem(k, 1, QTableWidgetItem(v["ID"]))
            self.DeviceChannTaable.setItem(
                k, 2, QTableWidgetItem("{0}".format(v["Scale"])))

    def switchDevice(self, dName):
        if dName is None:
            return

        self.initUI_rw()
        self.DeviceNameText.setText(dName)
        self.DeviceTypeComboBox.clear()

        for a in protocol.M:
            self.DeviceTypeComboBox.addItem(a.Name)
        for k, v in enumerate(protocol.M):
            if v.Device == self.getCurDeviceCfg()["deviceType"]:
                self.DeviceTypeComboBox.setCurrentIndex(k)
                break

        def ChooseType(ii):
            tt = self.getDeviceTypeEx(ii)
            self.getCurDeviceCfg()["deviceType"] = tt.Device
            self.switchChannTable(tt)
        self.DeviceTypeComboBox.currentTextChanged.connect(ChooseType)

        self.refreshPortList()
        self.DevicePortListComboBox.setEditText(self.getCurDeviceCfg()["port"])
        for k, v in enumerate(self.l):
            if v.device == self.getCurDeviceCfg()["port"]:
                self.DevicePortListComboBox.setCurrentIndex(k)

        def ChoosePort(ii):
            print("ChoosePort {0}".format(ii))
            curPort = None
            for k, v in enumerate(self.l):
                if "{0}".format(v) == ii:
                    curPort = v.device
                    break
            if not curPort is None:
                self.getCurDeviceCfg()["port"] = curPort
            print("ChoosePort A {0}".format(curPort))
            # self.getCurDeviceCfg()["port"] = self.l[ii].device
        self.DevicePortListComboBox.currentTextChanged.connect(ChoosePort)

        self.DeviceBaudComboBox.addItems(config.baudList)
        self.DeviceBaudComboBox.setEditText(
            self.getCurDeviceCfg()["baud"])

        def ChooseBaud(ii):
            self.getCurDeviceCfg()["baud"] = ii
        self.DeviceBaudComboBox.currentTextChanged.connect(ChooseBaud)

        self.DeviceChannTaable.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.DeviceChannTaable.setSelectionBehavior(
            QAbstractItemView.SelectRows)
        self.DeviceChannTaable.setColumnCount(3)
        self.DeviceChannTaable.setHorizontalHeaderLabels(
            ["通道名称", "ID", "缩放"])

        self.switchChannTable(self.getCurrentDeviceEx())

    def initUI(self):
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)

        leftWidget = QWidget()
        self.hbox.addWidget(leftWidget)
        self.hbox.setStretchFactor(leftWidget, 1)
        vbox = QVBoxLayout()
        leftWidget.setLayout(vbox)

        self.deviceListW = QListWidget()
        self.deviceListW.itemClicked.connect(self.listwidgetclicked)
        vbox.addWidget(self.deviceListW)

        op_widget = QWidget()
        vbox.addWidget(op_widget)
        op_hbox = QHBoxLayout()
        op_hbox.setSpacing(0)
        op_hbox.setContentsMargins(0, 0, 0, 0)
        op_widget.setLayout(op_hbox)

        btn1 = QPushButton()
        btn1.setText("+")
        btn1.clicked.connect(self.on_add_device)
        op_hbox.addWidget(btn1)

        btn2 = QPushButton()
        btn2.setText("-")
        btn2.clicked.connect(self.delete_device)
        op_hbox.addWidget(btn2)

        self.btn_ok = QPushButton()
        self.btn_ok.setText("确定")
        vbox.addWidget(self.btn_ok)

        def on_Btn_OK():
            all_chan = config.CFG.getAllCurChannel()
            if (all_chan is None) or (len(all_chan) == 0):
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Critical)
                s = "{0}\r\n".format("至少要选择1个通道")
                msgBox.setText(s)
                msgBox.setWindowTitle("配置错误")
                msgBox.setStandardButtons(QMessageBox.Ok)
                returnValue = msgBox.exec()
                return
            config.CFG.data["serial"] = self.device_list
            config.saveConfig()
            self.accept()
        self.btn_ok.clicked.connect(on_Btn_OK)

        self.rightWidget = QWidget()
        self.hbox.addWidget(self.rightWidget)
        self.hbox.setStretchFactor(self.rightWidget, 4)

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
        # self.combobox_1.setModel(model)
        self.DevicePortListComboBox.setModel(model)
        # try:
        #     currentPort = config.CFG.data["serial"]["port"]
        #     if not currentPort is None:
        #         self.combobox_1.setEditText(currentPort)
        #         for i, a in enumerate(self.l):
        #             if a.device == currentPort:
        #                 self.combobox_1.setCurrentIndex(i)
        #                 break
        # except KeyError as e:
        #     pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qb = SerialSettingWindow()
    qb.show()
    sys.exit(app.exec_())
