# coding:utf-8

import datetime
import json
import sys
# import traceback
import typing

# import PyQt5
import serial
# from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (
    qApp, QApplication,
    QHBoxLayout,
    QWidget, QDockWidget,
    QFileDialog, QMainWindow, QMessageBox,
    QMenu, QAction,
)

from window.dockbar import (
    livedata, extpanel,
)

import config
from config import CFG
import protocol
import timer
from protocol.base import (BaseProtocol, Btn_Base, Btn_Func, Btn_Func_Dir,
                           Btn_Input)
from window import SerialSettingWindow, WebChart


def round(a):
    if a % 1 > 0.4:
        return int(a)+1
    else:
        return int(a)


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.hbox = QHBoxLayout()

        self.web = WebChart(self)
        self.hbox.addWidget(self.web)
        self.setLayout(self.hbox)

        self.f1 = livedata.LiveData(self, "实时数据")
        self.ext_panels = []
        # self.f3 = Sub1_Window(self, "f3")

        self.parent = parent

        parent.addDockWidget(Qt.LeftDockWidgetArea, self.f1)
        # parent.addDockWidget(Qt.RightDockWidgetArea, self.f2)
        # parent.addDockWidget(Qt.RightDockWidgetArea, self.f3)

        if not CFG.gCfg.view.showLiveData:
            self.f1.hide()
        # self.f2.hide()
        # self.f3.hide()
        self.initUI()

    def initUI(self):
        pass

    def add_Ext_Panel(self, panel):
        self.ext_panels.append(panel)
        self.parent.addDockWidget(Qt.RightDockWidgetArea, panel)

    def closeAll_Ext_Panel(self):
        for p in self.ext_panels:
            p.hide()
            p.close()


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("USB temperature monitor")
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
                msgBox.exec()
                subW = SerialSettingWindow()
                subW.exec()
                print("config init OK")
        self.w = MainWidget(self)
        self.initUI()
        self.cp = []

        self.ttt_data = []
        self.ttt_live_data = []
        self.ttt = timer.Timer(
            delay=CFG.gCfg.chart.chartRefreshInterval,
            acc=0.01,
            fn=self.onClock)
        self.ttt_liveData = timer.Timer(
            delay=1, acc=0.01, fn=self.onClock_LiveData)

        self.resize(900, 600)

        self.data = []
        self.onceU = 0
        self.startTime = None
        self.A_time = None
        self.nn = 0
        self.nnn = 0

        self.sss = []

        self.att = None

        self.viewmode = WebChart.ViewMode_All

    def onClock_LiveData(self):
        dur = None
        n = datetime.datetime.now()

        if self.startTime is not None:
            dur = n - self.startTime
            dur = datetime.timedelta(
                milliseconds=round(dur.total_seconds())*1000)
        self.w.f1.push_meta_data([dur, len(self.data)])
        self.w.f1.push_data(self.ttt_live_data)

    def onClock(self):
        n = datetime.datetime.now()
        dur = None

        if self.onceU == 0:
            is_empty = False
            for v in self.ttt_data:
                if v in [None, ""]:
                    is_empty = True
                    break

            if is_empty:
                return
            else:
                self.onceU += 1
                self.startTime = n
                dur = datetime.timedelta(seconds=0)
                self.A_time = n
        dur = n-self.startTime
        self.A_time = n
        dur = datetime.timedelta(
            milliseconds=round(dur.total_seconds()*100)*10)
        ss = "{0}".format(dur)

        # qb.web.push_data(self.ttt_data)
        self.w.web.push_data({
            "timestamp": ss,
            "data": self.ttt_data,
        })

        self.data.append({
            "timestamp": dur.total_seconds(),
            "data": self.ttt_data,
        })
        self.ttt_live_data = self.ttt_data

        self.ttt_data = []
        for _ in config.CFG.getAllCurChannel_Comp():
            self.ttt_data.append("")

    def initUI(self):

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("文件")
        settingMenu = menubar.addMenu("设置")
        ProtocolMenu = menubar.addMenu("通讯协议")
        ChartMenu = menubar.addMenu("图表显示")
        helpMenu = menubar.addMenu("帮助")

        saveAction = QAction(self)
        saveAction.setText("保存数据")
        saveAction.triggered.connect(self.on_save)
        fileMenu.addAction(saveAction)

        loadAction = QAction(self)
        loadAction.setText("加载数据")
        loadAction.triggered.connect(self.on_import)
        fileMenu.addAction(loadAction)

        exitAction = QAction(self)
        exitAction.setText("退出")
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.btnsMenu = settingMenu.addMenu("扩展")
        self.btnsMenu.setDisabled(True)

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

        def aaa(checked):
            if checked:
                self.w.f1.show()
                CFG.gCfg.view.showLiveData = True
            else:
                self.w.f1.hide()
                CFG.gCfg.view.showLiveData = False

        self.dockBarMenu = ChartMenu.addMenu("侧边栏")

        self.dockAction_LiveData = QAction("实时数据", self)
        self.dockAction_LiveData.setCheckable(True)
        if CFG.gCfg.view.showLiveData:
            self.dockAction_LiveData.setChecked(True)
        self.dockAction_LiveData.triggered.connect(aaa)
        self.dockBarMenu.addAction(self.dockAction_LiveData)

        self.EtxDockMenu = self.dockBarMenu.addMenu("扩展面板")
        self.EtxDockMenu.setDisabled(True)

        self.viewLastAction_list = []

        def on_set_view_last(num, viewLastAction_list):
            def aaa(checked):
                if checked:
                    for k, v in enumerate(viewLastAction_list):
                        if v.text() == "x={0}".format(num):
                            v.setChecked(True)
                        else:
                            v.setChecked(False)
                    CFG.gCfg.view.showLatestView = num
                    self.w.web.viewmode = WebChart.ViewMode_Last
                    self.w.web.viewModeLast = num
            return aaa

        def on_set_view_all(viewLastAction_list):
            def aaa(checked):
                for k, v in enumerate(viewLastAction_list):
                    if k == 0:
                        v.setChecked(True)
                    else:
                        v.setChecked(False)
                self.w.web.viewmode = WebChart.ViewMode_All
            return aaa

        viewLastMenu = ChartMenu.addMenu("显示最后x个数据")
        self.viewAllAction = QAction("显示全部", self)
        self.viewAllAction.setCheckable(True)
        self.viewAllAction.triggered.connect(
            on_set_view_all(self.viewLastAction_list))
        self.viewLastAction_list.append(self.viewAllAction)
        viewLastMenu.addAction(self.viewAllAction)
        for i in [20, 50, 100, 200, 500, 1000, 5000, 10000]:
            viewLastAction = QAction("x={}".format(i), self)
            viewLastAction.setCheckable(True)
            viewLastAction.triggered.connect(
                on_set_view_last(i, self.viewLastAction_list))
            viewLastMenu.addAction(viewLastAction)
            self.viewLastAction_list.append(viewLastAction)

        if CFG.gCfg.view.showLatestView == 0:
            self.viewAllAction.setChecked(True)
        else:
            on_set_view_last(CFG.gCfg.view.showLatestView,
                             self.viewLastAction_list)(True)

        refreshAction = QAction("刷新视图", self)
        refreshAction.triggered.connect(self.on_refresh)
        ChartMenu.addAction(refreshAction)

        aboutAction = QAction(self)
        aboutAction.setText("关于这个软件")
        helpMenu.addAction(aboutAction)

        self.setCentralWidget(self.w)

    def closeEvent(self, event):
        config.saveConfig()
        event.accept()

    def on_refresh(self):
        self.w.web.set_data(self.data)

    def on_update_btn_list(self):
        pass

    def on_click_serial_setting(self):
        subW = SerialSettingWindow(self)
        subW.exec()

    def on_start(self):
        all_chan = config.CFG.getAllCurChannel_Comp()
        all_chan_a = config.CFG.getAllCurChannel()
        self.ttt_data = []
        self.cp = []
        self.w.closeAll_Ext_Panel()

        for _ in all_chan:
            self.ttt_data.append("")
        try:
            # self.w.web.reload()
            self.w.web.set_data([])
            self.w.web.set_channels(all_chan)

            self.w.f1.set_channels(all_chan_a)

            self.sss = self.openSerial()
            self.serialAction.setDisabled(True)
            self.startAction.setDisabled(True)
            self.pauseAction.setDisabled(False)
            self.btnsMenu.setDisabled(False)
            self.statusBar().showMessage("启动采样")
            self.data = []
            self.ttt.Run()
            self.ttt_liveData.Run()
            self.setWindowTitle("USB temperature monitor | 数据采样启动")

        except serial.serialutil.SerialException as e:
            # subW = SerialSettingWindow(self)
            # returnValue = subW.exec()
            print("e: {0}".format(e))
            pass
            # raise e

    def on_pause(self):
        self.ttt.Stop()
        self.ttt_liveData.Stop()
        self.onceU = 0
        self.btnsMenu.clear()
        for k, v in enumerate(self.cp):
            try:
                v.onClose()
            except serial.serialutil.SerialException as e:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText(
                    "错误：{0}".format(e))
                msgBox.setWindowTitle("关闭串口发生错误")
                msgBox.setStandardButtons(QMessageBox.Ok)
                _ = msgBox.exec()
        self.cp = None
        self.ttt_data = None
        for k, v in enumerate(self.sss):
            v.close()
        # closeSerial()
        self.serialAction.setDisabled(False)
        self.startAction.setDisabled(False)
        self.pauseAction.setDisabled(True)
        self.btnsMenu.setDisabled(True)
        self.statusBar().showMessage("暂停采样")
        self.setWindowTitle("USB temperature monitor | 数据采样暂停")

    def on_import(self):
        fpath, flit = QFileDialog.getOpenFileName(
            parent=self,
            caption="导入数据，格式：{0}".format(
                format),
            filter='csv文件(*.csv)',
        )
        import_data = []
        all_chan = []

        lines = []

        if fpath == "":
            return

        with open(fpath, 'r') as f:
            lines = f.readlines()

        for k, line in enumerate(lines):
            lines[k] = line[:-1]

        for item in lines[0].split(',')[1:]:
            all_chan.append({
                "Name": item,
            },)

        # t_start = datetime.datetime.strptime(
        #     '2021-01-06 20:00:00',
        #     "%Y-%m-%d %H:%M:%S") - datetime.timedelta(seconds=109395)

        datetime.datetime.strptime

        for item in lines[1:]:
            item_data = []
            items = item.split(',')
            for k, i in enumerate(items[1:]):
                if k >= len(all_chan):
                    break
                if i == "":
                    item_data.append("")
                else:
                    item_data.append(float(i))

            t = float(items[0])

            # t_a = datetime.timedelta(milliseconds=round(t*100)*10)
            # t_a = t_start + datetime.timedelta(milliseconds=round(t*100)*10)

            import_data.append({
                'timestamp': "{0:02d}:{1:02d}:{2:02d}.{3:02d}".format(
                    int(t / 60 / 60),
                    int(t % 60 / 60),
                    int(t % 60 % 60),
                    int(t*100 % 100),
                ),
                'data': item_data,
            })

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        s = ""
        s += "文件路径：{0}\n".format(fpath)
        s += "通道数：{0}\n".format(len(all_chan))
        s += "数据量：{0}\n".format(len(import_data))
        msgBox.setText(s)
        msgBox.setWindowTitle("导入文件信息")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Ok:
            print("数据导入 len:{0} path:{1}".format(len(import_data), fpath))
            self.w.web.reload()
            self.w.web.set_channels(all_chan)
            self.w.web.set_data(import_data)
            self.setWindowTitle(
                "USB temperature monitor | 导入文件 | {0}".format(fpath))
            self.data = import_data
        elif returnValue == QMessageBox.Cancel:
            print("数据导入 取消")

    def on_save(self):
        fpath, flit = QFileDialog.getSaveFileName(
            parent=self, caption="保存数据", filter='csv文件(*.csv);;json文件(*.json)')
        # print("Path: {0} {1}".format(fpath, flit))
        if fpath == "":
            return
        if flit == "csv文件(*.csv)":
            with open(fpath, 'w+') as f:

                tit = "time"

                for i in config.CFG.getAllCurChannel_Comp():
                    tit += ",{0}".format(i["Name"])

                # print("通道：{0}".format(tit))

                f.write(tit+"\n")
                for a in self.data:
                    f.write("{0},".format(a["timestamp"]))
                    for ii in a["data"]:
                        f.write("{0},".format(ii))
                    f.write("\n")
        elif flit == "json文件(*.json)":
            with open(fpath, 'w+') as f:
                f.write(json.dumps({
                    "channels": config.CFG.getAllCurChannel_Comp(),
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
        _ = msgBox.exec()
        return None

    def gen_ser_recv(self, index):
        padding = 0
        for k1, v1 in enumerate(config.CFG.data["serial"]):
            if k1 == index:
                break
            padding += len(v1["chann"])
        chann = config.CFG.data["serial"][index]["chann"]

        def fn(body):
            dd = self.cp[index].parsePkg(body)
            if len(dd) == 0:
                return

            for k, v in enumerate(chann):
                if k >= len(dd):
                    self.ttt_data[padding+k] = 0
                else:
                    self.ttt_data[padding+k] = dd[v]
        return fn

    def _addExtBtnMenu_Intput(self, menu: QMenu, Btn_Input: Btn_Input):
        btn_act = QAction(Btn_Input.name, self)
        menu.addAction(btn_act)
        # w = Btn_Input_Window(Btn_Input)

        w = extpanel.ExtPanel(
            Btn_Input,
            # name="{0}-{1}".format(Btn_Input.name),
            parent=self)
        self.w.add_Ext_Panel(w)

        def aaa():
            w.close()
            w.show()
            # if w.exec() != 0:
            #     print("{0} {1} args {2}".format(
            #         menu.title(), Btn_Input.name, w.args))
        btn_act.triggered.connect(aaa)

    def _addExtBtnMenu(self, menu: QMenu, btn_func_dir: typing.List[Btn_Base]):
        for i in btn_func_dir:
            if not isinstance(i, Btn_Base):
                continue
            if type(i) is Btn_Func:
                btn_act = QAction(self)
                menu.addAction(btn_act)
                if i.func is not None:
                    btn_act.setText(i.name)
                    btn_act.triggered.connect(i.func)
                else:
                    btn_act.setText("{0} NoFunc".format(i.name))
            elif type(i) is Btn_Func_Dir:
                self._addExtBtnMenu(menu.addMenu(i.name), i.btn_items)
            elif type(i) is Btn_Input:
                self._addExtBtnMenu_Intput(menu, i)
            else:
                btn_act = QAction(
                    "??? {0} {1}".format(i.name, type(i)), self)
                btn_act.setDisabled(True)
                menu.addAction(btn_act)

    def addExtBtnMenu(self):
        for k, v in enumerate(config.CFG.data["serial"]):
            c = self.cp[k]
            btn_menu = self.btnsMenu.addMenu("{0}".format(v["name"]))
            if c.M_Btn is not None:
                self._addExtBtnMenu(btn_menu, c.M_Btn)

    def openSerial(self):
        try:
            sss = []
            chann_index = 0
            for k, v in enumerate(config.CFG.data["serial"]):

                if v["port"] == "NaN":
                    sss.append(None)
                else:
                    s = serial.Serial(
                        port=v["port"],
                        baudrate=v["baud"],
                    )
                    sss.append(s)

                c = protocol.find(v["deviceType"])(s)
                c.onOpen()
                self.cp.append(c)

                def on_serialPackage(body):
                    dd = c.parsePkg(body)
                    print("k {0} aa {1} {2}".format(k, v["chann"], dd))
                    # for k1, v1 in enumerate(v["chann"]):
                    #     self.ttt_data[chann_index+k1] = dd[v1]
                    # self.uData(dd)
                chann_index += len(v["chann"])

                if v["deviceType"] == "Tool8775C1":
                    self.aat = protocol.SerialThread(s, self.gen_ser_recv(
                        k), BaseProtocol.ProtocolType_T87_RS232)
                else:
                    self.aat = protocol.SerialThread(s, self.gen_ser_recv(k))
                self.aat.setDaemon(True)
                self.aat.start()
            self.addExtBtnMenu()

            # def s_fn():
            #     return b"\x01"

            # aat = protocol.SerialThreadSend(sss, fn=s_fn)
            # aat.setDaemon(True)
            # aat.start()
            return sss

        except serial.serialutil.SerialException as e:

            for k, v in enumerate(sss):
                if v != "None":
                    v.close()

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(
                "错误：{0}".format(e))
            msgBox.setWindowTitle("打开串口发生错误")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            raise e


def app_panic_hook(exctype, value, ttraceback):
    print('My Error Information')
    print('Type:', exctype)
    print('Value:', value)

    log_file = "panic.log"

    msg_txt = ""
    msg_txt += "崩溃日志文件：{0}\r\n".format(log_file)
    tb_txt = ""
    tb_txt += "="*79+"\n"
    tb_txt += "exception:\n  {0}\n  {1}\n".format(exctype, value)
    tb_txt += "="*79+"\n"
    tb_txt += "trace:\n"
    while ttraceback:
        tb_txt += "  {0}\n".format(ttraceback.tb_frame)
        ttraceback = ttraceback.tb_next
    msg_txt += tb_txt

    with open(log_file, 'w+') as f:
        f.write(tb_txt)

    print(msg_txt)
    msgBox = QMessageBox()
    # msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText(msg_txt)
    msgBox.setWindowTitle("程序崩溃")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()
    sys.exit(1)


if __name__ == '__main__':
    sys.excepthook = app_panic_hook
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    qb = MyMainWindow()
    print("Start Done")

    qb.show()
    sys.exit(app.exec())
