# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import sys
from PyQt4 import QtCore, QtGui
from db import DatabaseError
from ui.dbpropertiesdialog import Ui_DbPropertiesDialog


class DbPropertiesDialog(QtGui.QDialog, Ui_DbPropertiesDialog):

    def __init__(self, db, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self._db = db

        self.setupUi(self)

        self.name = db.getDbProperty('name').toString()
        self.description = db.getDbProperty('description').toString()
        self.filenameEdit.setText(db.name)
        self.nameEdit.setText(self.name)
        self.descriptionEdit.setText(self.description)

    def on_buttonBox_accepted(self):
        db = self._db
        try:
            if self.nameEdit.text() != self.name:
                db.setDbProperty('name', self.nameEdit.text())
            if self.descriptionEdit.text() != self.description:
                db.setDbProperty('description',
                                 self.descriptionEdit.text())
        except DatabaseError, msg:
            QtGui.QMessageBox.critical(self, self.tr("Error"),
                                       QtCore.QString("%1: %2")
                                       .arg(sys.exc_info()[0].__name__)
                                       .arg(msg))
        else:
            self.accept()

