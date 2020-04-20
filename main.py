# coding:utf-8

import sys
import random
import datetime
from PyQt5.QtCore import (
    Qt,
    QUrl,
    pyqtSlot,
)
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QGridLayout,
    QVBoxLayout,
    QMainWindow,
    QPushButton,
    QAction,
    qApp,
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineSettings,
    QWebEngineView,
    QWebEnginePage,
)
from PyQt5.QtGui import QIcon

from pyecharts.charts import Line
from pyecharts import options as opts

import asserts
import serialSetting


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.initUI()

        self.setWindowTitle("USB temperature monitor")

        self.main_widget = WebChart(self)
        self.setCentralWidget(self.main_widget)
        self.resize(900, 600)

    def initUI(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("文件")
        settingMenu = menubar.addMenu("设置")
        helpMenu = menubar.addMenu("帮助")

        saveCSVAction = QAction(self)
        saveCSVAction.setText("保存为CSV")
        fileMenu.addAction(saveCSVAction)

        saveJsonAction = QAction(self)
        saveJsonAction.setText("保存为Json")
        fileMenu.addAction(saveJsonAction)

        exitAction = QAction(self)
        exitAction.setText("退出")
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)


        serialAction = QAction(self)
        serialAction.setText("串口参数")
        settingMenu.triggered.connect(self.on_click_serial_setting)
        settingMenu.addAction(serialAction)

        aboutAction = QAction(self)
        aboutAction.setText("关于这个软件")
        helpMenu.addAction(aboutAction)

    @pyqtSlot()
    def on_click_serial_setting(self):
        subW = serialSetting.SerialSettingWindow(self)
        # subW.show()


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
        vbox.addWidget(self.web)

        button = QPushButton('PyQt5 button', self)
        button.clicked.connect(self.on_click)
        vbox.addWidget(button)

        # button1 = QPushButton('button1', self)
        # button1.setToolTip('This is an example button')
        # button1.clicked.connect(self.on_click_serial_setting)
        # vbox.addWidget(button1)

        self.data = [
            {
                "timestamp": 1,
                "data": [1, 2, 3, 4]
            },
            {
                "timestamp": 2,
                "data": [5, 6, 7, 8]
            },
            {
                "timestamp": 3,
                "data": [9, 10, 11, 12]
            },
            {
                "timestamp": 4,
                "data": [13, 14, 15, 16]
            },
        ]
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
        self.setMessage(
            "resize {0} => {1}".format(event.oldSize(), event.size()))
        self.runJs(r"""if (typeof resize !== "undefined")resize();""")
        return super(WebChart, self).resizeEvent(event)

    @pyqtSlot()
    def on_click(self):

        self.data.append({
            "timestamp": "{0}".format(datetime.datetime.now().time()),
            "data": [
                int(random.random() * 100),
                int(random.random() * 100),
                int(random.random() * 100),
                int(random.random() * 100)
            ]
        })

        self.set_data(self.data)

    def set_data(self, data):
        self.web.page().runJavaScript(r"set_data({})".format(self.data))

    def runJs(self, str):
        self.web.page().runJavaScript(str)

    def initData(self):
        bar = (
            Line()
            .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
            .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
            .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
        )

        bar.render()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qb = MyMainWindow()
    qb.show()
    sys.exit(app.exec_())
