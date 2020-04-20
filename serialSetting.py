from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,g
)

import sys
import serial.tools.list_ports


class SerialSettingWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SerialSettingWindow, self).__init__(parent)
        # super().__init__()
        self.setWindowTitle("串口参数设置")
        # self.setWindowModality(Qt.ApplicationModal)
        # self.setWindowFlags(
        #     # Qt.WindowCloseButtonHint |
        #     # Qt.MSWindowsFixedSizeDialogHint |
        #     Qt.Tool
        #     )
        self.resize(300, 200)
        self.initUI()
        self.show()

    def initUI(self):

        # button1 = QPushButton('button1', self)
        # button1.setToolTip('This is an example button')
        # hbox.addWidget(button1)
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)


    def on_list_serial(self):
        self.serial_list = list(serial.tools.list_ports.comports())

class MainWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # hbox = QHBoxLayout()
        # vbox.addWidget(hbox)
        # self.setLayout(hbox)

        model = QStandardItemModel()
        for a in serial.tools.list_ports.comports():
            it = QStandardItem("{0}".format(a))
            it.setData(a)
            model.appendRow(it)
        combobox_1 = QComboBox(self)
        combobox_1.clear()
        combobox_1.setModel(model)
        vbox.addWidget(combobox_1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qb = SerialSettingWindow()
    qb.show()
    sys.exit(app.exec_())
