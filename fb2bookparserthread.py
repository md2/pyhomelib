# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

from PyQt4 import QtCore, QtSql
from fb2streamreader import FB2StreamReader
from bookdblayer import *

class FB2BookParserThread(QtCore.QThread):

    bookParsed = QtCore.pyqtSignal(FB2StreamReader)

    def __init__(self, parent=None):
        super(FB2BookParserThread, self).__init__(parent)
        self.bookid = 0
        self.abort = False
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()

    def __del__(self):
        QtSql.QSqlDatabase.removeDatabase("parser_thread_connection")

    def quit(self):
        locker = QtCore.QMutexLocker(self.mutex)
        self.abort = True
        self.condition.wakeOne()

    def parse(self, bookid):
        locker = QtCore.QMutexLocker(self.mutex)
        if self.bookid != bookid:
            self.bookid = bookid
            self.condition.wakeOne()

    def run(self):
        self.mutex.lock()
        if QtSql.QSqlDatabase.contains("parser_thread_connection"):
            self.mutex.unlock()
            return
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE", "parser_thread_connection")
        self.mutex.unlock()
        db.setDatabaseName(dbName())
        if not db.open():
            return
        while not self.abort:
            bookid = self.bookid
            if bookid != 0:
                filename = execScalar(db, "SELECT filename FROM libfilename WHERE bookid = ? LIMIT 1",
                                      bookid)
                if filename:
                    reader = FB2StreamReader()
                    if reader.read(filename.toString()) and self.bookid == bookid:
                        self.bookParsed.emit(reader)
            self.mutex.lock()
            if self.bookid == bookid:
                self.bookid = 0
                self.condition.wait(self.mutex)
            self.mutex.unlock()

