# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore, QtGui


class TreeView(QtGui.QTreeView):

    rowSelected = QtCore.pyqtSignal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

    def selectionChanged(self, selected, deselected):
        QtGui.QTreeView.selectionChanged(self, selected, deselected)
        if selected.indexes():
            self.rowSelected.emit(selected.indexes()[0])

