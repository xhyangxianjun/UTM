from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFontMetrics
from protocol.base import BaseProtocol, Btn_Base, Btn_Func, Btn_Func_Dir, Btn_Input, Btn_Input_Opt


class Btn_Input_Window(QMainWindow):
    def __init__(self, btn_input: Btn_Input, parent=None):
        super().__init__()
        self.setWindowTitle("USB temperature monitor XXXXX")
        self.args = {}
        self.btn_input: Btn_Input = btn_input
        self.vaild_ok = True
        self.textEdits = []

        for v in self.btn_input.opts:
            self.args[v.name] = v.default_value

        self.initUI()

    def initUI(self):
        mainWidget = QWidget()
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(0)
        # self.vbox.setContentsMargins(0, 0, 0, 0)
        mainWidget.setLayout(self.vbox)

        self.setCentralWidget(mainWidget)

        if self.btn_input.description != "":
            nameLabel = QLabel()
            nameLabel.setText(self.btn_input.description)
            self.vbox.addWidget(nameLabel)

        p_Widget = QWidget()
        self.vbox.addWidget(p_Widget)
        p_layout = QHBoxLayout()
        p_Widget.setLayout(p_layout)

        l_Widget = QWidget()
        l_layout = QVBoxLayout()
        p_layout.addWidget(l_Widget)
        l_Widget.setLayout(l_layout)
        l_layout.setContentsMargins(0, 0, 0, 0)

        r_Widget = QWidget()
        r_layout = QVBoxLayout()
        p_layout.addWidget(r_Widget)
        r_Widget.setLayout(r_layout)
        r_layout.setContentsMargins(0, 0, 0, 0)

        # err_Widget = QWidget()
        # err_layout = QVBoxLayout()
        # err_layout.addWidget(err_Widget)
        # err_Widget.setLayout(err_layout)
        # err_layout.setContentsMargins(0, 0, 0, 0)

        self.textEdits = []
        for k, v in enumerate(self.btn_input.opts):
            nameLabel = QLabel(v.name)
            l_layout.addWidget(nameLabel)
            valueLabel = QLineEdit()
            valueLabel.setText("{0}".format(self.args[v.name]))
            r_layout.addWidget(valueLabel)
            self.textEdits.append(valueLabel)

        accept_Widget = QWidget()
        self.vbox.addWidget(accept_Widget)
        accept_layout = QHBoxLayout()
        accept_Widget.setLayout(accept_layout)

        accept_layout.setSpacing(0)
        accept_layout.setContentsMargins(0, 0, 0, 0)

        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.on_ok_button_clicked)
        accept_layout.addWidget(ok_button)

        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.on_cannel_btn_clicked)
        accept_layout.addWidget(cancel_button)

    def on_ok_button_clicked(self):

        result = True
        self.args = {}

        for k, v in enumerate(self.btn_input.opts):
            r, d = v.Valid(self.textEdits[k].text())
            if r:
                self.args[v.name] = d
            else:
                result = False

        if result:
            try:
                if self.btn_input.func is not None:
                    self.btn_input.func(self.args)
            except KeyError as e:
                print("扩展动作错误 {0} {1} {2}".format(type(e), e, self.args))
            # self.accept()

    def on_cannel_btn_clicked(self):
        self.close()
        pass
        # self.reject()
