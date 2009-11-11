# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statisticsdialog.ui'
#
# Created: Fri Nov  6 14:42:12 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_StatisticsDialog(object):
    def setupUi(self, StatisticsDialog):
        StatisticsDialog.setObjectName("StatisticsDialog")
        StatisticsDialog.resize(319, 175)
        self.horizontalLayout = QtGui.QHBoxLayout(StatisticsDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(StatisticsDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(StatisticsDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(StatisticsDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(StatisticsDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.numberOfBooksLabel = QtGui.QLabel(StatisticsDialog)
        self.numberOfBooksLabel.setObjectName("numberOfBooksLabel")
        self.gridLayout.addWidget(self.numberOfBooksLabel, 0, 1, 1, 1)
        self.numberOfAuthorsLabel = QtGui.QLabel(StatisticsDialog)
        self.numberOfAuthorsLabel.setObjectName("numberOfAuthorsLabel")
        self.gridLayout.addWidget(self.numberOfAuthorsLabel, 1, 1, 1, 1)
        self.numberOfSequencesLabel = QtGui.QLabel(StatisticsDialog)
        self.numberOfSequencesLabel.setObjectName("numberOfSequencesLabel")
        self.gridLayout.addWidget(self.numberOfSequencesLabel, 2, 1, 1, 1)
        self.totalSizeLabel = QtGui.QLabel(StatisticsDialog)
        self.totalSizeLabel.setObjectName("totalSizeLabel")
        self.gridLayout.addWidget(self.totalSizeLabel, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(StatisticsDialog)
        QtCore.QMetaObject.connectSlotsByName(StatisticsDialog)

    def retranslateUi(self, StatisticsDialog):
        StatisticsDialog.setWindowTitle(QtGui.QApplication.translate("StatisticsDialog", "Statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StatisticsDialog", "Number of authors:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("StatisticsDialog", "Number of sequences:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("StatisticsDialog", "Number of books:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("StatisticsDialog", "Total size:", None, QtGui.QApplication.UnicodeUTF8))

