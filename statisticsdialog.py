# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore, QtGui
from ui_statisticsdialog import Ui_StatisticsDialog


class StatisticsDialog(QtGui.QDialog, Ui_StatisticsDialog):

    def __init__(self, db, parent=None):
        super(StatisticsDialog, self).__init__(parent)

        self.setupUi(self)

        numberOfBooks = db.getBookCount()
        numberOfAuthors = db.execScalar("SELECT COUNT(*) FROM libauthorname").toInt()[0]
        numberOfSequences = db.execScalar("SELECT COUNT(*) FROM libseqname").toInt()[0]
        totalSize = db.execScalar("SELECT SUM(filesize) FROM libbook").toLongLong()[0]

        self.numberOfBooksLabel.setNum(numberOfBooks)
        self.numberOfAuthorsLabel.setNum(numberOfAuthors)
        self.numberOfSequencesLabel.setNum(numberOfSequences)
        self.totalSizeLabel.setText(QtCore.QLocale.system().toString(totalSize)
                                    + " " + self.tr("bytes"))

