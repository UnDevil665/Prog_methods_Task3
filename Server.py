import sys
import datetime
import json
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from MyTableModel import TableModel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(400, 300))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 400))
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textedit = QtWidgets.QTextEdit(self.centralwidget)
        self.textedit.setObjectName("textedit")
        self.textedit.setLineWrapMode(QtWidgets.QTextEdit.FixedColumnWidth)
        self.textedit.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.textedit.setMaximumWidth(771)
        self.horizontalLayout_2.addWidget(self.textedit, 0, QtCore.Qt.AlignVCenter)
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setObjectName("send_button")
        self.horizontalLayout_2.addWidget(self.send_button)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.tableview = QtWidgets.QTableView(self.centralwidget)
        self.tableview.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tableview.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tableview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableview.setObjectName("tableview")
        self.tableview.setMaximumSize(982, 283)
        self.tableview.setWordWrap(True)
        self.gridLayout.addWidget(self.tableview, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alert Server"))
        self.send_button.setText(_translate("MainWindow", "Send"))


class Server_MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Server_MainWindow, self).__init__()
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        self.tablemodel = TableModel()
        self.tableview.setModel(self.tablemodel)
        self.tableview.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.tableview.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.socket = QtNetwork.QUdpSocket(self)

        self.send_button.pressed.connect(self.addMessage)

    def addMessage(self):
        row = self.tablemodel.rowCount()
        self.tablemodel.insertRow(row)
        index = self.tablemodel.index(row, 0)
        today = datetime.datetime.today()

        self.tablemodel.setData(index, {"time": today.strftime("%H:%M"), "date": today.strftime("%d.%m.%Y"),
                                        "message": self.textedit.toPlainText()})
        self.textedit.clear()

        data = {"time": self.tablemodel.data(self.tablemodel.index(row, 0)),
                "date": self.tablemodel.data(self.tablemodel.index(row, 1)),
                "message": self.tablemodel.data(self.tablemodel.index(row, 2))}

        jdata = json.dumps(data)

        jbytes = bytearray(jdata, encoding='utf-8')

        self.socket.writeDatagram(jbytes, QtNetwork.QHostAddress.Broadcast, 45454)

    def test(self):
        self.tablemodel.insertRow(0)
        index = self.tablemodel.index(0, 0)

        self.tablemodel.setData(index, {"time": "1", "date": "2", "message": "3"})


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    server_window = Server_MainWindow()
    server_window.show()
    sys.exit(app.exec())
