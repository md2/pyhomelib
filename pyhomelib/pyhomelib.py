#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql
from mainwindow import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)

    if not QtSql.QSqlDatabase.drivers().contains("QSQLITE"):
        raise Exception, "Fatal error: QSQLITE database driver is not found!"

    qttranslator = QtCore.QTranslator()
    if qttranslator.load("qt_" + QtCore.QLocale.system().name(),
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
        app.installTranslator(qttranslator)

    translator = QtCore.QTranslator()
    if translator.load("pyhomelib_" + QtCore.QLocale.system().name()):
        app.installTranslator(translator)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
