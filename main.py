# coding:utf-8

import sys
import random
import datetime
from PyQt5.QtCore import (
    Qt,
    QUrl,
    pyqtSlot,
    QCoreApplication,
)
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMessageBox,
    QFileDialog,
    QGridLayout,
    QVBoxLayout,
    QMainWindow,
    QPushButton,
    QAction,
    qApp,
)
from PyQt5.QtWebEngineWidgets import (
    # QWebEngineSettings,
    QWebEngineView,
    # QWebEnginePage,
)
# from PyQt5.QtGui import QIcon

# from pyecharts.charts import Line
# from pyecharts import options as opts

import asserts
import serialSetting
import protocol
import struct
import serial
import os
import json
import config


def round(a):
    if a % 1 > 0.4:
        return int(a)+1
    else:
        return int(a)


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.initUI()

        self.setWindowTitle("USB temperature monitor")

        self.cp = None

        self.web = WebChart(self)

        self.main_widget = self.web
        self.setCentralWidget(self.main_widget)
        self.resize(900, 600)

        self.data = []
        self.onceU = 0
        self.startTime = None
        self.A_time = None
        self.nn = 0

        self.sss = None

        self.att = None

    def uData(self, d):

        n = datetime.datetime.now()
        dur = None

        if self.onceU == 0:
            self.onceU += 1

            self.startTime = n
            dur = datetime.timedelta(seconds=0)

            self.A_time = n
        else:
            dur = n-self.startTime

            # print("nnn: {0}".format((n-self.A_time).total_seconds()))

            self.A_time = n

        # if self.onceU == 1:
        #     self.data = []
        #     self.onceU += 1

        dur = datetime.timedelta(
            milliseconds=round(dur.total_seconds()*10)*100)

        # if dur.total_seconds() != self.nn * 0.5:
        #     print("AAA: {0:.3f} {1}".format(
        #         dur.total_seconds(), self.nn))
        #     self.on_pause()
        # else:
        #     print("AAA: {0:.3f}".format(dur.total_seconds()))

        self.nn += 1

        self.data.append({
            "timestamp": "{0}".format(str(dur)),
            "data": d,
        })
        qb.web.set_data(self.data)

    def initUI(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("文件")
        settingMenu = menubar.addMenu("设置")
        ProtocolMenu = menubar.addMenu("通讯协议")
        helpMenu = menubar.addMenu("帮助")

        saveAction = QAction(self)
        saveAction.setText("保存数据")
        saveAction.triggered.connect(self.on_save)
        fileMenu.addAction(saveAction)

        loadAction = QAction(self)
        loadAction.setText("加载数据")
        fileMenu.addAction(loadAction)

        exitAction = QAction(self)
        exitAction.setText("退出")
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.serialAction = QAction(self)
        self.serialAction.setText("串口参数")
        self.serialAction.triggered.connect(self.on_click_serial_setting)
        settingMenu.addAction(self.serialAction)

        self.startAction = QAction(self)
        self.startAction.setText("启动采样")
        self.startAction.triggered.connect(self.on_start)
        settingMenu.addAction(self.startAction)

        self.pauseAction = QAction(self)
        self.pauseAction.setText("暂停采样")
        self.pauseAction.setDisabled(True)
        self.pauseAction.triggered.connect(self.on_pause)
        settingMenu.addAction(self.pauseAction)

        for a in protocol.M:

            aMenu = ProtocolMenu.addMenu(a.Name)
            aMenu.addMenu("名称：{}".format(a.Name))
            aMenu.addMenu("设备号：{}".format(a.Device))
            aMenu.addMenu("简介：{}".format(a.Description))

        aboutAction = QAction(self)
        aboutAction.setText("关于这个软件")
        helpMenu.addAction(aboutAction)

    def on_click_serial_setting(self):
        subW = serialSetting.SerialSettingWindow(self)
        subW.exec()

    def on_start(self):
        try:
            self.sss = self.openSerial()
            self.serialAction.setDisabled(True)
            self.startAction.setDisabled(True)
            self.pauseAction.setDisabled(False)
            self.statusBar().showMessage("启动采样")
            self.data = []
            self.web.set_data(self.data)
        except serial.serialutil.SerialException as e:
            # subW = serialSetting.SerialSettingWindow(self)
            # returnValue = subW.exec()
            # print("Fuuuuuck {}".format(returnValue))
            pass

    def on_pause(self):
        if not type(self.sss) is type(None):
            self.sss.close()
            self.serialAction.setDisabled(False)
            self.startAction.setDisabled(False)
            self.pauseAction.setDisabled(True)
            self.onceU = 0
        # closeSerial()
        self.statusBar().showMessage("暂停采样")

        self.cp.onClose()

    def on_save(self):
        fpath, flit = QFileDialog.getSaveFileName(parent=self, caption="保存数据，格式：{0}".format(
            format), filter='csv文件(*.csv);;json文件(*.json)')
        # print("Path: {0} {1}".format(fpath, flit))
        if fpath == "":
            return
        if flit == "csv文件(*.csv)":
            with open(fpath, 'w+') as f:
                f.write("time,CH1,CH2,CH3,CH4\n")
                for a in self.data:
                    f.write("{0},".format(a["timestamp"]))
                    for l in a["data"]:
                        f.write("{0},".format(l))
                    f.write("\n")
        elif flit == "json文件(*.json)":
            with open(fpath, 'w+') as f:
                f.write(json.dumps(self.data))
        self.statusBar().showMessage("存储采样数据，格式: {}".format(format))

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        s = ""
        s += "文件路径：{0}\n".format(fpath)
        s += "数据量：{0}".format(len(self.data))
        msgBox.setText(s)
        msgBox.setWindowTitle("保存成功")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
        return None

    def openSerial(self):

        while(config.CFG.data is None):
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
                subW = serialSetting.SerialSettingWindow()
                subW.exec()

        try:
            sss = serial.Serial(
                port=config.CFG.data["serial"]["port"],
                baudrate=config.CFG.data["serial"]["baud"],
            )

            serialPackage = None

            self.cp = config.CFG.currentProtocol()(sss)
            self.cp.onOpen()

            def a(body):
                dd = self.cp.parsePkg(body)
                self.uData(dd)

            serialPackage = a

            self.aat = protocol.SerialThread(sss, serialPackage)
            self.aat.setDaemon(True)
            self.aat.start()

            # def s_fn():
            #     return b"\x01"

            # aat = protocol.SerialThreadSend(sss, fn=s_fn)
            # aat.setDaemon(True)
            # aat.start()
            return sss

        except serial.serialutil.SerialException as e:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(
                "串口参数：{0}\r\n错误：{1}".format(
                    "port: {0} baud:{1}".format(
                        config.CFG.data["serial"]["port"],
                        config.CFG.data["serial"]["baud"],
                    ),
                    e))
            msgBox.setWindowTitle("打开串口发生错误")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            raise e


class WebChart(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        parent.statusBar().showMessage('启动完成')

        self.setMessage = parent.statusBar().showMessage

        vbox = QVBoxLayout()

        self.web = QWebEngineView()
        # self.web.setContextMenuPolicy(Qt.NoContextMenu)
        # htmlF = open("render.html", "r")
        # self.initData()
        # self.web.setHtml(htmlF.read())
        self.web.load(QUrl("qrc:///html/render.html"))

        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.web)

        # button = QPushButton('PyQt5 button', self)
        # button.clicked.connect(self.on_click)
        # vbox.addWidget(button)

        # button1 = QPushButton('button1', self)
        # button1.setToolTip('This is an example button')
        # button1.clicked.connect(self.on_click_serial_setting)
        # vbox.addWidget(button1)

        # self.data = [
        #     {
        #         "timestamp": 1,
        #         "data": [1, 2, 3, 4]
        #     },
        #     {
        #         "timestamp": 2,
        #         "data": [5, 6, 7, 8]
        #     },
        #     {
        #         "timestamp": 3,
        #         "data": [9, 10, 11, 12]
        #     },
        #     {
        #         "timestamp": 4,
        #         "data": [13, 14, 15, 16]
        #     },
        # ]
        self.setLayout(vbox)
        self.web.loadFinished.connect(self.initChart)

    def initChart(self):
        self.runJs(r"""
            var chart_b7e5870db3d84d4db9639909239acfd9 = echarts.init(
                document.getElementById('b7e5870db3d84d4db9639909239acfd9'),
                'white',
                { renderer: 'canvas' });
            chart_b7e5870db3d84d4db9639909239acfd9.setOption(option_b7e5870db3d84d4db9639909239acfd9);
        """)

    def resizeEvent(self, event):
        # self.setMessage(
        #     "resize {0} => {1}".format(event.oldSize(), event.size()))
        self.runJs(r"""if (typeof resize !== "undefined")resize();""")
        return super(WebChart, self).resizeEvent(event)

    # @pyqtSlot()
    # def on_click(self):

    #     self.data.append({
    #         "timestamp": "{0}".format(datetime.datetime.now().time()),
    #         "data": [
    #             int(random.random() * 100),
    #             int(random.random() * 100),
    #             int(random.random() * 100),
    #             int(random.random() * 100)
    #         ]
    #     })
    #     self.set_data(self.data)

    def set_data(self, data):
        self.web.page().runJavaScript(r"set_data({})".format(data))

    def runJs(self, str):
        self.web.page().runJavaScript(str)

    # def initData(self):
    #     bar = (
    #         Line()
    #         .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    #         .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    #         .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    #         .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
    #     )

    #     bar.render()


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    qb = MyMainWindow()
    print("Start Done")

    qb.show()
    sys.exit(app.exec_())
