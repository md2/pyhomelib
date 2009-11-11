# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

import os
import sys
from PyQt4 import QtCore, QtGui
from ui_importdialog import Ui_ImportDialog
from fb2streamreader import FB2StreamReader
from importthread import ImportThread
from finderthread import FinderThread


class ImportDialog(QtGui.QDialog, Ui_ImportDialog):

    def __init__(self, dbname, directory, parent=None):
        super(ImportDialog, self).__init__(parent)
        self.found = 0
        self.processed = 0

        self.setupUi(self)
        desktopGeometry = QtGui.qApp.desktop().screenGeometry()
        self.move((desktopGeometry.width() - self.width()) / 2,
                  (desktopGeometry.height() - self.height()) / 2)

        self.importThread = ImportThread(dbname, directory)
        self.importThread.error.connect(self.textEdit.append)
        self.importThread.processed.connect(self.on_processed)
        self.importThread.start()
        self.finderThread = FinderThread(directory)
        self.finderThread.found.connect(self.on_found)
        self.finderThread.found.connect(self.importThread.addFilename)
        self.finderThread.start()
        self.finished.connect(self.importThread.quit)
        self.finished.connect(self.finderThread.quit)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateCounters)
        timer.start(100)

    def __del__(self):
        self.importThread.wait()
        self.finderThread.wait()

    def on_found(self, filename):
        self.found += 1

    def on_processed(self, filename):
        self.processed += 1

    def updateCounters(self):
        self.filesFoundLabel.setNum(self.found)
        self.filesProcessedLabel.setNum(self.processed)
        if self.found != 0:
            self.progressBar.setValue(100 * self.processed / self.found)
        if self.found == self.processed and not self.finderThread.isRunning():
            self.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(-1)
    app = QtGui.QApplication(sys.argv)
    qttranslator = QtCore.QTranslator()
    if qttranslator.load("qt_" + QtCore.QLocale.system().name(),
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
        app.installTranslator(qttranslator)
    translator = QtCore.QTranslator()
    if translator.load("pyhomelib_" + QtCore.QLocale.system().name()):
        app.installTranslator(translator)
    dlg = ImportDialog(QtCore.QString.fromUtf8(sys.argv[1]),
                       QtCore.QString.fromUtf8(sys.argv[2]))
    dlg.show()
    ret = app.exec_()
    if len(sys.argv) >= 4 and sys.argv[3] == '--execvp':
        os.execvp('python', ('python', 'pyhomelib.py', sys.argv[1]))
    sys.exit(ret)

