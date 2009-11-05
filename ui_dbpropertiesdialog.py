# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dbpropertiesdialog.ui'
#
# Created: Thu Nov  5 15:18:19 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DbPropertiesDialog(object):
    def setupUi(self, DbPropertiesDialog):
        DbPropertiesDialog.setObjectName("DbPropertiesDialog")
        DbPropertiesDialog.resize(357, 186)
        self.verticalLayout = QtGui.QVBoxLayout(DbPropertiesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.nameEdit = QtGui.QLineEdit(DbPropertiesDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 2, 1, 1, 1)
        self.descriptionEdit = QtGui.QLineEdit(DbPropertiesDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridLayout.addWidget(self.descriptionEdit, 3, 1, 1, 1)
        self.label = QtGui.QLabel(DbPropertiesDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(DbPropertiesDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.filenameEdit = QtGui.QLineEdit(DbPropertiesDialog)
        self.filenameEdit.setEnabled(False)
        self.filenameEdit.setObjectName("filenameEdit")
        self.gridLayout.addWidget(self.filenameEdit, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(DbPropertiesDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.selectFileButton = QtGui.QToolButton(DbPropertiesDialog)
        self.selectFileButton.setEnabled(False)
        self.selectFileButton.setText("...")
        self.selectFileButton.setObjectName("selectFileButton")
        self.gridLayout.addWidget(self.selectFileButton, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(DbPropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DbPropertiesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DbPropertiesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DbPropertiesDialog)
        DbPropertiesDialog.setTabOrder(self.filenameEdit, self.selectFileButton)
        DbPropertiesDialog.setTabOrder(self.selectFileButton, self.nameEdit)
        DbPropertiesDialog.setTabOrder(self.nameEdit, self.descriptionEdit)
        DbPropertiesDialog.setTabOrder(self.descriptionEdit, self.buttonBox)

    def retranslateUi(self, DbPropertiesDialog):
        DbPropertiesDialog.setWindowTitle(QtGui.QApplication.translate("DbPropertiesDialog", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DbPropertiesDialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DbPropertiesDialog", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DbPropertiesDialog", "Database File:", None, QtGui.QApplication.UnicodeUTF8))

