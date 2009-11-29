# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importdialog.ui'
#
# Created: Sun Nov 29 16:54:13 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ImportDialog(object):
    def setupUi(self, ImportDialog):
        ImportDialog.setObjectName("ImportDialog")
        ImportDialog.resize(400, 444)
        self.cancelButton = QtGui.QPushButton(ImportDialog)
        self.cancelButton.setGeometry(QtCore.QRect(310, 400, 80, 26))
        self.cancelButton.setObjectName("cancelButton")
        self.textEdit = QtGui.QTextEdit(ImportDialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 80, 381, 281))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.label = QtGui.QLabel(ImportDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 29))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(ImportDialog)
        self.label_2.setGeometry(QtCore.QRect(200, 10, 121, 29))
        self.label_2.setObjectName("label_2")
        self.filesFoundLabel = QtGui.QLabel(ImportDialog)
        self.filesFoundLabel.setGeometry(QtCore.QRect(140, 10, 51, 29))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.filesFoundLabel.setFont(font)
        self.filesFoundLabel.setText("0")
        self.filesFoundLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.filesFoundLabel.setObjectName("filesFoundLabel")
        self.filesProcessedLabel = QtGui.QLabel(ImportDialog)
        self.filesProcessedLabel.setGeometry(QtCore.QRect(330, 10, 51, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.filesProcessedLabel.setFont(font)
        self.filesProcessedLabel.setText("0")
        self.filesProcessedLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.filesProcessedLabel.setObjectName("filesProcessedLabel")
        self.progressBar = QtGui.QProgressBar(ImportDialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 40, 381, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.closeAfterCompletingBox = QtGui.QCheckBox(ImportDialog)
        self.closeAfterCompletingBox.setGeometry(QtCore.QRect(12, 370, 381, 21))
        self.closeAfterCompletingBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.closeAfterCompletingBox.setChecked(True)
        self.closeAfterCompletingBox.setObjectName("closeAfterCompletingBox")

        self.retranslateUi(ImportDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("pressed()"), ImportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportDialog)
        ImportDialog.setTabOrder(self.closeAfterCompletingBox, self.cancelButton)
        ImportDialog.setTabOrder(self.cancelButton, self.textEdit)

    def retranslateUi(self, ImportDialog):
        ImportDialog.setWindowTitle(QtGui.QApplication.translate("ImportDialog", "Scanning directory", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("ImportDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ImportDialog", "Files found:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ImportDialog", "Files processed:", None, QtGui.QApplication.UnicodeUTF8))
        self.closeAfterCompletingBox.setText(QtGui.QApplication.translate("ImportDialog", "Close after completing", None, QtGui.QApplication.UnicodeUTF8))

