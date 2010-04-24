# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore, QtGui
from ui_settingsdialog import Ui_SettingsDialog

class SettingsDialog(QtGui.QDialog, Ui_SettingsDialog):

    rowHeightChanged = QtCore.pyqtSignal(int)

    def __init__(self, settings, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.settings = settings

        self.setupUi(self)

        self.readSettings()

    def readSettings(self):
        programs = self.settings.getPrograms()
        for index in xrange(min(len(programs), 9)):
            edit1 = self.findChild(QtGui.QLineEdit,
                                   QtCore.QString('titleEdit%1').arg(index + 1))
            edit2 = self.findChild(QtGui.QLineEdit,
                                   QtCore.QString('cmdEdit%1').arg(index + 1))
            edit1.setText(programs[index][0])
            edit2.setText(programs[index][1])

        self.dontSaveUiOnExitBox.setChecked(not self.settings.getSaveUiOnExitOption())
        self.rowHeightBox.setValue(self.settings.getRowHeight())

    def writeSettings(self):
        programs = []
        for index in xrange(9):
            edit1 = self.findChild(QtGui.QLineEdit,
                                   QtCore.QString('titleEdit%1').arg(index + 1))
            edit2 = self.findChild(QtGui.QLineEdit,
                                   QtCore.QString('cmdEdit%1').arg(index + 1))
            title = edit1.text().trimmed()
            cmd = edit2.text().trimmed()
            programs.append((title, cmd))
        self.settings.writePrograms(programs)

        self.settings.writeSaveUiOnExitOption(not self.dontSaveUiOnExitBox.isChecked())
        self.settings.writeRowHeight(self.rowHeightBox.value())

    @QtCore.pyqtSlot(int)
    def on_rowHeightBox_valueChanged(self, value):
        self.rowHeightChanged.emit(value)

    def on_buttonBox_accepted(self):
        self.writeSettings()
        self.accept()


