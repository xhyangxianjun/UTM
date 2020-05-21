# coding:utf-8

import sys
import datetime
import protocol
import serial
import os
import json
import config
import time
import math
import threading

from PyQt5.QtCore import (
    Qt,
    QCoreApplication,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QFileDialog,
    QMainWindow,
    QAction,
    qApp,
)

from window import SerialSettingWindow
from window import WebChart


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

        self.setCentralWidget(self.web)
        self.resize(900, 600)

        self.data = []
        self.onceU = 0
        self.startTime = None
        self.A_time = None
        self.nn = 0
        self.nnn = 0

        self.sss = None

        self.att = None

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
                subW = SerialSettingWindow()
                subW.exec()

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


        if dur.total_seconds() > datetime.timedelta(seconds=self.nnn * 60).total_seconds():
            self.nnn += 1

            # print("min {0}".format(dur.total_seconds()))

        dd = {
            "timestamp": "{0}".format(str(dur)),
            "data": d,
        }
        self.data.append(dd)

        ss = "{0}".format(dur)

        # print("ss: [{0},{1}],".format(ss,d))
        # qb.web.set_data(self.data)

        qb.web.push_data({
            "timestamp": ss,
            "data": d,
        })

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

        saveAction = QAction(self)
        saveAction.setText("测试")
        saveAction.triggered.connect(self.random_data)
        fileMenu.addAction(saveAction)

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
            channels = aMenu.addMenu("通道数目：{}".format(len(a.xAxis)))

            for ii in a.xAxis:
                nn = channels.addMenu(ii["Name"])

                for k in ii.keys():
                    nn.addMenu("{0}: {1}".format(k, ii[k]))

        aboutAction = QAction(self)
        aboutAction.setText("关于这个软件")
        helpMenu.addAction(aboutAction)

    def random_data(self):

        self.data = []
        self.web.set_channels(config.CFG.currentProtocol().xAxis)
        cnt = 1000

        def ffff():
            for i in range(cnt):

                z1 = datetime.datetime(year=2000,month=1,day=1)

                ss = (z1+datetime.timedelta(seconds=i)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

                dd = {
                    "timestamp": ss,
                    "data": [
                        math.sin(i/100),
                        math.cos(i/100),
                        math.sin(i/100) * 0.5,
                        math.cos(i/100) * 0.5,
                    ]
                }
                self.web.push_data(dd)

                self.statusBar().showMessage("测试数据: {0:05d}".format(i))
                time.sleep(0.1)

        ttt = threading.Thread(target=ffff)
        ttt.setDaemon(True)
        ttt.start()

    def on_click_serial_setting(self):
        subW = SerialSettingWindow(self)
        subW.exec()

    def on_start(self):
        try:
            self.sss = self.openSerial()
            self.serialAction.setDisabled(True)
            self.startAction.setDisabled(True)
            self.pauseAction.setDisabled(False)
            self.statusBar().showMessage("启动采样")
            self.data = []

            self.web.set_channels(config.CFG.currentProtocol().xAxis)
            self.web.set_data(self.data)
        except serial.serialutil.SerialException as e:
            # subW = serialSetting.SerialSettingWindow(self)
            # returnValue = subW.exec()
            pass

    def on_pause(self):
        self.cp.onClose()
        if not type(self.sss) is type(None):
            self.sss.close()
            self.serialAction.setDisabled(False)
            self.startAction.setDisabled(False)
            self.pauseAction.setDisabled(True)
            self.onceU = 0
        # closeSerial()
        self.statusBar().showMessage("暂停采样")


    def on_save(self):
        fpath, flit = QFileDialog.getSaveFileName(parent=self, caption="保存数据，格式：{0}".format(
            format), filter='csv文件(*.csv);;json文件(*.json)')
        # print("Path: {0} {1}".format(fpath, flit))
        if fpath == "":
            return
        if flit == "csv文件(*.csv)":
            with open(fpath, 'w+') as f:

                tit = "time"

                for  i in config.CFG.currentProtocol().xAxis:
                    tit += ",{0}".format(i["Name"])

                print("通道：{0}".format(tit))

                f.write(tit+"\n")
                for a in self.data:
                    f.write("{0},".format(a["timestamp"]))
                    for l in a["data"]:
                        f.write("{0},".format(l))
                    f.write("\n")
        elif flit == "json文件(*.json)":
            with open(fpath, 'w+') as f:
                f.write(json.dumps({
                    "device": config.CFG.currentProtocol().Device,
                    "channels": config.CFG.currentProtocol().xAxis,
                    "data": self.data,
                }))
        self.statusBar().showMessage("存储采样数据，格式: {}".format(flit))

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
                subW = SerialSettingWindow()
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

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    qb = MyMainWindow()
    print("Start Done")

    qb.show()
    sys.exit(app.exec_())
