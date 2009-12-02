# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

import sys
from PyQt4 import QtCore, QtGui
import pyhomelib_rc


class XmlValidatorDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.tr('Validator'))
        self.resize(500, 600)
        desktopGeometry = QtGui.qApp.desktop().screenGeometry()
        self.move((desktopGeometry.width() - self.width()) / 2,
                  (desktopGeometry.height() - self.height()) / 2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pyhomelib.png"), QtGui.QIcon.Normal,
                                                         QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.textEdit = QtGui.QTextEdit(self)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
        QtCore.QTimer.singleShot(100, self.validate)

    def validate(self):
        process = QtCore.QProcess(self)
        process.readyReadStandardOutput.connect(self.readStandardOutput)
        process.readyReadStandardError.connect(self.readStandardError)
        self.process = process
        args = [QtCore.QString.fromUtf8(arg) for arg in sys.argv[1:]]
        process.start("xmllint", args)
        if not process.waitForStarted(10000):
            self.textEdit.append("<span style='color:red'>" +
                                 self.tr("Could not launch xmllint.") +
                                 "</span>")

    def readStandardOutput(self):
        text = QtCore.QString.fromUtf8(self.process.readAllStandardOutput())
        for par in text.split("\n"):
            self.textEdit.append(QtCore.QString("<p>%1</p>").arg(par))

    def readStandardError(self):
        text = QtCore.QString.fromUtf8(self.process.readAllStandardError())
        for par in text.split("\n"):
            self.textEdit.append(QtCore.QString("<p>%1</p>").arg(par))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(-1)
    app = QtGui.QApplication(sys.argv)
    qttranslator = QtCore.QTranslator()
    if qttranslator.load("qt_" + QtCore.QLocale.system().name(),
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
        app.installTranslator(qttranslator)
    translator = QtCore.QTranslator()
    if translator.load("pyhomelib_" + QtCore.QLocale.system().name()):
        app.installTranslator(translator)
    dlg = XmlValidatorDialog()
    dlg.show()
    sys.exit(app.exec_())

