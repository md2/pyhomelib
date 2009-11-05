#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from mainwindow import MainWindow

app = QtGui.QApplication(sys.argv)

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

