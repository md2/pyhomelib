# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import os
import sys
from PyQt4 import QtCore, QtGui, QtSql
from ui_importdialog import Ui_ImportDialog
from fb2streamreader import FB2StreamReader
from importthread import ImportThread
from finderthread import FinderThread


class ImportDialog(QtGui.QDialog, Ui_ImportDialog):

    def __init__(self, directory, parent=None):
        super(ImportDialog, self).__init__(parent)
        self.found = 0
        self.processed = 0

        self.setupUi(self)

        self.importThread = ImportThread(directory)
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
            if self.closeAfterCompletingBox.isChecked():
                self.close()

