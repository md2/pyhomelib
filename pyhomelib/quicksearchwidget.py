# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore, QtGui


class QuickSearchWidget(QtGui.QWidget):

    returnPressed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(QtGui.QWidget, self).__init__(parent)

        layout = QtGui.QHBoxLayout(self)
        self.searchForLabel = QtGui.QLabel(self.tr("Search for:"), self)
        layout.addWidget(self.searchForLabel)
        self.searchForEdit = QtGui.QLineEdit(self)
        self.searchForEdit.keyPressEvent = self.searchForEdit_keyPressEvent
        self.searchForEdit.returnPressed.connect(self.on_searchForEdit_returnPressed)
        layout.addWidget(self.searchForEdit)
        self.hideButton = QtGui.QToolButton(self)
        self.hideButton.setIcon(QtGui.QIcon(QtGui.QPixmap(":/window-close.png")))
        self.hideButton.clicked.connect(self.on_hideButton_clicked)
        layout.addWidget(self.hideButton)

    def show(self):
        QtGui.QWidget.show(self)
        self.searchForEdit.selectAll()
        self.searchForEdit.setFocus()

    def text(self):
        return self.searchForEdit.text()

    def on_searchForEdit_returnPressed(self):
        self.returnPressed.emit()

    def on_hideButton_clicked(self):
        self.hide()

    def searchForEdit_keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.hideButton.click()
            event.accept()
        else:
            QtGui.QLineEdit.keyPressEvent(self.searchForEdit, event)

