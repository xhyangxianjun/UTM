import datetime
import json
import sys
import traceback
import typing

import PyQt5
import serial
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QLabel,
    QDockWidget, QAction, QApplication, QFileDialog, QMainWindow,
    QHBoxLayout, QVBoxLayout,
    QMenu, QMessageBox, qApp)


class LiveData(QDockWidget):
    def __init__(self, parent=None, name=None):
        super().__init__()
        self.main_setter = None
        self.field_setters = []
        if name is None:
            self.setWindowTitle("LiveData")
        else:
            self.setWindowTitle(name)
        self.QGroupBox_List = []
        self.abox = QVBoxLayout()
        self.aw = QWidget()
        self.aw.setLayout(self.abox)
        self.setWidget(self.aw)
        # self.setLayout(self.hbox)

    def clr_channels(self):
        self.main_setter = None
        self.field_setters = []
        for i in reversed(range(self.abox.count())):
            self.abox.itemAt(i).widget().setParent(None)

    def set_channels(self, channels):
        self.channels = channels
        self.channels_range = []
        channels_range_i = 0
        self.clr_channels()
        self.main_setter = self.add_group("数据统计", ["监控时长", "数据总数"])
        for k, v in enumerate(self.channels):
            self.channels_range.append(
                [channels_range_i, channels_range_i+len(v["xAxis"])])
            channels_range_i += len(v["xAxis"])
            fs = []
            for i in v["xAxis"]:
                fs.append("{0}({1})".format(i["Name"], i["ID"]))
            self.field_setters.append(self.add_group(
                group_name="{0}-{1}({2})".format(
                    v["Name"], v["DName"], v["Device"]),
                fields=fs,
                stretch=1,
            ))

    def add_group(self, group_name, fields, stretch=0):
        r_label_list = []
        qgb = QGroupBox(self)
        qgb.setTitle(group_name)
        self.abox.addWidget(qgb, stretch)
        hbox1 = QHBoxLayout()
        qgb.setLayout(hbox1)

        self.vbox1 = QVBoxLayout()
        w1 = QWidget()
        hbox1.addWidget(w1)
        w1.setLayout(self.vbox1)

        self.vbox2 = QVBoxLayout()
        w2 = QWidget()
        hbox1.addWidget(w2)
        w2.setLayout(self.vbox2)

        for i in fields:
            l_label = QLabel(i)
            self.vbox1.addWidget(l_label)
            r_label = QLabel("N/A")
            self.vbox2.addWidget(r_label)
            r_label_list.append(r_label)

        def aaa(value_list):
            min_len = len(fields)
            if len(value_list) < len(fields):
                min_len = len(value_list)
            for i in range(min_len):
                r_label_list[i].setText("{0}".format(value_list[i]))
        return aaa

    def push_meta_data(self, datas):
        self.main_setter(datas)

    def push_data(self, datas):
        for k, v in enumerate(self.channels_range):
            self.field_setters[k](datas[v[0]:v[1]])
