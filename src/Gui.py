import sys
from PyQt4 import QtGui

from .Globals import print1, print2, print3


class Gui(QtGui.QWidget):
    def __init__(self, code):
        super(Gui, self).__init__()
        self.init_ui(self, code)

    @staticmethod
    def on_click(self, code, vbox, l):
        k = self.sender().objectName()
        code = code[int(k)]
        n = len(code)
        i = 0
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        while i < n:
            line = str(code[i])
            button1 = QtGui.QPushButton(line)
            button1.setMaximumWidth(1980 / (n + 0.01))
            button1.setObjectName(str(i))
            if type(code[i]) is list:
                button1.clicked.connect(lambda: self.on_click(self, code, vbox, i))
            button1.setStyleSheet("Text-align:left")
            hbox.addWidget(button1)
            i += 1
        hbox.addStretch(1)
        vbox.addLayout(hbox)


    @staticmethod
    def init_ui(self, code):
        n = len(code)
        i = 0
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        vbox = QtGui.QVBoxLayout()
        while i < n:
            line = str(code[i])
            button1 = QtGui.QPushButton(line)
            button1.setMaximumWidth(1980 / (n + 0.01))
            button1.setObjectName(str(i))
            if type(code[i]) is list:
                button1.clicked.connect(lambda: self.on_click(self, code, vbox, i))
            button1.setStyleSheet("Text-align:left")
            hbox.addWidget(button1)
            i += 1

        hbox.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(00, 00, 1980, 150)
        self.setWindowTitle('Program Debug')


def main(code):
    app = QtGui.QApplication(sys.argv)
    ex = Gui(code)
    ex.show()
    sys.exit(app.exec_())


def make_ui(code):
    main(code)
