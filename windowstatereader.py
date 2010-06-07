# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import os
from PyQt4 import QtCore, QtGui


class WindowStateReader(object):

    def __init__(self):
        super(WindowStateReader, self).__init__()
        self.reader = QtCore.QXmlStreamReader()

    def readStateFrom(self, filename):
        reader = self.reader
        file = QtCore.QFile(filename)
        if file.open(QtCore.QFile.ReadOnly):
            reader.setDevice(file)
            while not reader.isStartElement() and \
                  not reader.hasError():
                reader.readNext()
            if reader.isStartElement():
                self.readElement(True)

    def readElement(self, root=False):
        reader = self.reader
        name = reader.name().toString()

        if root:
            widget = self
        else:
            objname = reader.attributes().value('name').toString()
            widget = self.findChild(QtGui.QWidget, objname)

        if widget and widget.metaObject().className() == name:
            if widget.property('currentIndex').isValid():
                if reader.attributes().hasAttribute('currentIndex'):
                    currentIndex = reader.attributes().value('currentIndex').toString().toInt()[0]
                    widget.setCurrentIndex(currentIndex)

            if widget.inherits('QMainWindow'):
                if reader.attributes().hasAttribute('maximized') and \
                   reader.attributes().value('maximized') == '1':
                    widget.setWindowState(widget.windowState and QtCore.Qt.WindowMaximized)
                elif reader.attributes().hasAttribute('geometry'):
                    l = reader.attributes().value('geometry').toString().split(",")
                    if len(l) == 4:
                        widget.setGeometry(l[0].toInt()[0], l[1].toInt()[0],
                                           l[2].toInt()[0], l[3].toInt()[0])

            if widget.inherits('QDockWidget'):
                if reader.attributes().hasAttribute('visible'):
                    visible = reader.attributes().value('visible').toString().toInt()[0]
                    widget.setVisible(visible)
                if reader.attributes().hasAttribute('area'):
                    area = reader.attributes().value('area').toString().toInt()[0]
                    widget.parent().addDockWidget(area, widget)

            if widget.inherits('QSplitter'):
                if reader.attributes().hasAttribute('sizes'):
                    sizes = []
                    for size in reader.attributes().value('sizes').toString().split(","):
                        sizes.append(size.toInt()[0])
                    widget.setSizes(sizes)

            if widget.inherits('QTableView'):
                l = reader.attributes().value('headerSections').toString().split(",")
                for index in range(l.count()):
                    widget.horizontalHeader().resizeSection(index, l[index].toInt()[0])
                if reader.attributes().hasAttribute('visualOrder'):
                    l = reader.attributes().value('visualOrder').toString().split(",")
                    for index in range(l.count()):
                        widget.horizontalHeader().swapSections(widget.horizontalHeader().visualIndex(index),
                                                               l[index].toInt()[0])

            if widget.inherits('QToolBar'):
                if reader.attributes().hasAttribute('visible'):
                    visible = reader.attributes().value('visible').toString().toInt()[0]
                    widget.setVisible(visible)

        while not reader.atEnd():
            reader.readNext()
            if reader.isEndElement():
                break
            if reader.isStartElement():
                self.readElement()

