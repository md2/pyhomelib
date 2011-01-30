# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import sys
import os

from PyQt4 import QtCore, QtGui

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
        if '--schema' not in args:
            path_to_schema = self.get_schema()
            if path_to_schema:
                args.append(QtCore.QString.fromUtf8('--schema'))
                args.append(QtCore.QString.fromUtf8(path_to_schema))
        process.start("xmllint", args)
        if not process.waitForStarted(10000):
            self.textEdit.append("<span style='color:red'>" +
                                 self.tr("Could not launch xmllint.") +
                                 "</span>")
    def get_schema(self, files=None):
        schema_files = files or []
        data_dirs = ['..']
        data_dirs.extend(os.environ.get('XDG_DATA_DIRS',
            '/usr/share/').split(':'))
        schema_files.extend([os.path.join(d, 'pyhomelib', 'schema2.21',
            'FictionBook2.21.xsd') for d in data_dirs])
        for sf in schema_files:
            if os.path.exists(sf):
                return sf

    def readStandardOutput(self):
        text = QtCore.QString.fromUtf8(self.process.readAllStandardOutput())
        for par in text.split("\n"):
            self.textEdit.append(QtCore.QString("<p>%1</p>").arg(par))

    def readStandardError(self):
        text = QtCore.QString.fromUtf8(self.process.readAllStandardError())
        for par in text.split("\n"):
            self.textEdit.append(QtCore.QString("<p>%1</p>").arg(par))


def main():
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

if __name__ == '__main__':
    main()
