from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex, QVariant, Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super(TableModel, self).__init__()
        self.mylist = []

    def rowCount(self, parent=QModelIndex()) -> int:

        return len(self.mylist)

    def columnCount(self, parent=QModelIndex()) -> int:

        return 3

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        data = None
        row = index.row()
        column = index.column()

        if not index.isValid():
            return QVariant()

        if row >= len(self.mylist) or row < 0:
            return QVariant()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if column == 0:
                data = self.mylist[index.row()]['time']
            elif column == 1:
                data = self.mylist[index.row()]['date']
            elif column == 2:
                data = self.mylist[index.row()]['message']

        return data

    def setData(self, index: QModelIndex, value: dict, role: int = ...) -> bool:
        if not index.isValid():
            return False

        row = index.row()

        self.mylist[row] = value

        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount() - 1, 2))
        return True

    def insertRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
        self.beginInsertRows(parent, row, count + row - 1)

        for i in range(count):
            self.mylist.insert(row, {"time": "", "date": "", "message": ""})

        self.endInsertRows()
        return True

    def insertRow(self, row: int, parent=QModelIndex()) -> bool:
        self.insertRows(row, 1, parent)
        return True

    def removeRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, count + row - 1)

        for i in range(count):
            self.mylist.pop(row)

        self.endRemoveRows()
        return True

    def removeRow(self, row: int, parent=QModelIndex()) -> bool:
        self.removeRows(row, 1, parent)
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemIsEnabled

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if not role == Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            if section == 0:
                return self.tr("time")
            if section == 1:
                return self.tr("date")
            if section == 2:
                return self.tr("Message")

    def getList(self):
        return self.mylist

    def clear(self):
        self.mylist.clear()
