# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

from PyQt4 import QtCore, QtGui
from bookdblayer import db, execScalar
from ui_statisticsdialog import Ui_StatisticsDialog


class StatisticsDialog(QtGui.QDialog, Ui_StatisticsDialog):

    def __init__(self, parent=None):
        super(StatisticsDialog, self).__init__(parent)

        self.setupUi(self)

        numberOfBooks = execScalar(db(), "SELECT COUNT(*) FROM libbook").toInt()[0]
        numberOfAuthors = execScalar(db(), "SELECT COUNT(*) FROM libauthorname").toInt()[0]
        numberOfSequences = execScalar(db(), "SELECT COUNT(*) FROM libseqname").toInt()[0]
        totalSize = execScalar(db(), "SELECT SUM(filesize) FROM libbook").toLongLong()[0]

        self.numberOfBooksLabel.setNum(numberOfBooks)
        self.numberOfAuthorsLabel.setNum(numberOfAuthors)
        self.numberOfSequencesLabel.setNum(numberOfSequences)
        self.totalSizeLabel.setText(QtCore.QLocale.system().toString(totalSize)
                                    + " " + self.tr("bytes"))

