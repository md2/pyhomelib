# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore


class FinderThread(QtCore.QThread):

    found = QtCore.pyqtSignal(QtCore.QString)

    def __init__(self, directory, parent=None):
        super(FinderThread, self).__init__(parent)
        self.directory = directory
        self.abort = False

    def quit(self):
        self.abort = True

    def run(self):
        it = QtCore.QDirIterator(self.directory,
                                 QtCore.QDirIterator.Subdirectories)
        while it.hasNext() and not self.abort:
            if it.next().endsWith('.fb2') and it.fileInfo().isFile():
                self.found.emit(it.filePath())

