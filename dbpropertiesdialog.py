# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import os
import sys
from PyQt4 import QtCore, QtGui
from bookdblayer import *
from ui_dbpropertiesdialog import Ui_DbPropertiesDialog

class DbPropertiesDialog(QtGui.QDialog, Ui_DbPropertiesDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        self.name = getDbProperty('name').toString()
        self.description = getDbProperty('description').toString()
        self.nameEdit.setText(self.name)
        self.descriptionEdit.setText(self.description)

    def on_buttonBox_accepted(self):
        filename = self.filenameEdit.text()
        if not filename.trimmed().isEmpty():
            try:
                if self.nameEdit.text() != self.name:
                    setDbProperty('name', self.nameEdit.text())
                if self.descriptionEdit.text() != self.description:
                    setDbProperty('description',
                                  self.descriptionEdit.text())
            except Exception, msg:
                QtGui.QMessageBox.critical(self, self.tr("Error"),
                                           QtCore.QString("%1: %2")
                                           .arg(sys.exc_info()[0].__name__)
                                           .arg(msg))
            else:
                self.accept()

