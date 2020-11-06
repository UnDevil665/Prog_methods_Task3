from MyTableModel import TableModel
import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork


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
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableview = QtWidgets.QTableView(self.centralwidget)
        self.tableview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableview.setObjectName("tableview")
        self.gridLayout.addWidget(self.tableview, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alert Client"))


class Client_MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Client_MainWindow, self).__init__()
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        self.model = TableModel()
        self.tableview.setModel(self.model)
        self.tableview.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.tableview.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.socket = QtNetwork.QUdpSocket(self)
        self.socket.bind(45454, QtNetwork.QUdpSocket.ShareAddress)

        self.socket.readyRead.connect(self.processPendingDatagrams)

    def processPendingDatagrams(self):

        while self.socket.hasPendingDatagrams():
            datagram = int(self.socket.pendingDatagramSize())
            bytes, host, intik = self.socket.readDatagram(datagram)

            data = json.loads(bytes)

            row = self.model.rowCount()
            self.model.insertRow(row)
            index = self.model.index(row, 0)
            self.model.setData(index, data)

    def test(self):

        self.model.insertRow(0)
        index = self.model.index(0, 0)
        self.model.setData(index, {"time": "1", "date": "2", "message": "3"})

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client = Client_MainWindow()
    client.show()
    sys.exit(app.exec())
