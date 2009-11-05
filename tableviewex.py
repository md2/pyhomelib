# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

from PyQt4 import QtCore, QtGui

class HeaderViewEx(QtGui.QHeaderView):

    rightButtonPressed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(HeaderViewEx, self).__init__(QtCore.Qt.Horizontal, parent)
        self.setMovable(True)
        self.setClickable(True)
        self.setSortIndicatorShown(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.rightButtonPressed.emit()
            event.accept()
        else:
            QtGui.QHeaderView.mousePressEvent(self, event)


class TableViewEx(QtGui.QTableView):

    rowSelected = QtCore.pyqtSignal(QtCore.QModelIndex)
    rightButtonPressed = QtCore.pyqtSignal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(TableViewEx, self).__init__(parent)
        header = HeaderViewEx(self)
        header.rightButtonPressed.connect(self.on_header_rightButtonPressed)
        self.setHorizontalHeader(header)
        self.verticalHeader().hide()
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)

    def selectionChanged(self, selected, deselected):
        QtGui.QTableView.selectionChanged(self, selected, deselected)
        if selected.indexes():
            self.rowSelected.emit(selected.indexes()[0])

    def on_header_rightButtonPressed(self):
        menu = QtGui.QMenu()
        group = QtGui.QActionGroup(menu)
        group.setExclusive(False)
        group.triggered.connect(self.on_action_triggered)
        for index in xrange(self.horizontalHeader().count()):
            text = self.model().headerData(index, QtCore.Qt.Horizontal).toString()
            a = menu.addAction(text)
            a.setCheckable(True)
            a.index = index
            a.setChecked(not (self.isColumnHidden(index) or
                              self.horizontalHeader().sectionSize(index) == 0))
            group.addAction(a)
        menu.exec_(QtGui.QCursor.pos())

    def on_action_triggered(self, action):
        self.setColumnHidden(action.index, not action.isChecked())
        if action.isChecked() and self.horizontalHeader().sectionSize(action.index) == 0:
            self.horizontalHeader().resizeSection(action.index,
                                                  self.horizontalHeader().defaultSectionSize())

    def mousePressEvent(self, event):
        pressed = False
        if event.button() == QtCore.Qt.RightButton:
            index = self.indexAt(event.pos())
            pressed = True

        QtGui.QTableView.mousePressEvent(self, event)

        if pressed:
            self.rightButtonPressed.emit(index)

