from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

import asserts


class WebChart(QWidget):
    ViewMode_All = 0
    ViewMode_Last = 1

    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.viewmode = WebChart.ViewMode_All
        self.viewModeLast = 0

        # parent.statusBar().showMessage('启动完成')

        # self.setMessage = parent.statusBar().showMessage

        vbox = QVBoxLayout()

        self.web = QWebEngineView()
        self.web.setContextMenuPolicy(Qt.NoContextMenu)
        # htmlF = open("render.html", "r")
        # self.initData()
        # self.web.setHtml(htmlF.read())
        self.web.load(QUrl("qrc:///html/render.html"))

        # vbox.setSpacing(0)
        # vbox.setContentsMargins(0, 0, 0, 0)
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
                { renderer: 'canvas' },
                );
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
        self.web.page().runJavaScript(
            r"view_mode={0};view_latest={1};".format(
                self.viewmode,
                self.viewModeLast,
            ))
        self.web.page().runJavaScript(r"set_data({})".format(data))

    def push_data(self, data):
        self.web.page().runJavaScript(
            r"view_mode={0};view_latest={1};".format(
                self.viewmode,
                self.viewModeLast,
            ))
        self.web.page().runJavaScript(r"push_data({})".format(data))

    def runJs(self, str):
        self.web.page().runJavaScript(str)

    def set_channels(self, chan):
        self.web.page().runJavaScript(r"set_channel({})".format(chan))

    def reload(self):
        pass
        # self.web.reload()
        self.initChart()

    # def initData(self):
    #     bar = (
    #         Line()
    #         .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    #         .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    #         .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    #         .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
    #     )

    #     bar.render()
