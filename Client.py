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
        self.socket.bind(QtNetwork.QHostAddress.LocalHost, 45454, QtNetwork.QUdpSocket.ReuseAddressHint)

        self.socket.errorOccurred.connect(self.socketHasError)

        self.socket.readyRead.connect(self.processPendingDatagrams)
        QtWidgets.QMessageBox.information(self, "A connection error has occurred", self.socket.errorString())


        self.minimizeAction = QtWidgets.QAction("Minimize", self)
        self.restoreAction = QtWidgets.QAction("Restore", self)
        self.quitAction = QtWidgets.QAction("Exit", self)

        self.trayicon = QtWidgets.QSystemTrayIcon(self)
        self.icon = QtGui.QIcon('alert.jpg')

        self.trayIconMenu = QtWidgets.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addAction(self.quitAction)

        self.setTrayIconActions()
        self.showTrayIcon()

    def socketHasError(self):
        QtWidgets.QMessageBox.information(self, "A connection error has occurred", self.socket.errorString())

    def showTrayIcon(self):

        self.trayicon.setIcon(self.icon)
        self.trayicon.setContextMenu(self.trayIconMenu)

        self.model.dataChanged.connect(self.trayActionExecute)

        self.trayicon.show()

    def trayActionExecute(self):
        data = ""
        row = self.model.rowCount() - 1
        column = 2
        index = self.model.index(row, column)

        data += self.model.data(index)

        QtWidgets.QSystemTrayIcon.showMessage(self.trayicon, "Alert", data)

    def setTrayIconActions(self):
        self.minimizeAction.triggered.connect(self.hide)
        self.restoreAction.triggered.connect(self.showNormal)
        self.quitAction.triggered.connect(QtWidgets.QApplication.quit)

    def processPendingDatagrams(self):

        while self.socket.hasPendingDatagrams():
            datagram = int(self.socket.pendingDatagramSize())
            jbytes, host, intik = self.socket.readDatagram(datagram)

            data = json.loads(jbytes)

            row = self.model.rowCount()
            self.model.insertRow(row)
            index = self.model.index(row, 0)
            self.model.setData(index, data)

    def changeEvent(self, a0: QtCore.QEvent) -> None:
        if a0.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client = Client_MainWindow()
    client.show()
    sys.exit(app.exec())
