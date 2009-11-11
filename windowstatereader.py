# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

import os
from PyQt4 import QtCore, QtGui

class WindowStateReader(object):

    def __init__(self):
        super(WindowStateReader, self).__init__()
        self.reader = QtCore.QXmlStreamReader()

    def readStateFrom(self, filename):
        file = QtCore.QFile(filename)
        if file.open(QtCore.QFile.ReadOnly):
            self.reader.setDevice(file)
            while not self.reader.isStartElement() and \
                  not self.reader.hasError():
                self.reader.readNext()
            if self.reader.isStartElement():
                self.readElement(True)

    def readElement(self, root=False):
        name = self.reader.name().toString()

        if root:
            widget = self
        else:
            objname = self.reader.attributes().value('name').toString()
            widget = self.findChild(QtGui.QWidget, objname)

        if widget and widget.metaObject().className() == name:
            if widget.property('currentIndex').isValid():
                if self.reader.attributes().hasAttribute('currentIndex'):
                    currentIndex = self.reader.attributes().value('currentIndex').toString().toInt()[0]
                    widget.setCurrentIndex(currentIndex)

            if widget.inherits('QMainWindow'):
                if self.reader.attributes().hasAttribute('maximized') and \
                   self.reader.attributes().value('maximized') == '1':
                    widget.setWindowState(widget.windowState and QtCore.Qt.WindowMaximized)
                elif self.reader.attributes().hasAttribute('geometry'):
                    l = self.reader.attributes().value('geometry').toString().split(",")
                    if len(l) == 4:
                        widget.setGeometry(l[0].toInt()[0], l[1].toInt()[0],
                                           l[2].toInt()[0], l[3].toInt()[0])

            if widget.inherits('QDockWidget'):
                if self.reader.attributes().hasAttribute('visible'):
                    visible = self.reader.attributes().value('visible').toString().toInt()[0]
                    widget.setVisible(visible)
                if self.reader.attributes().hasAttribute('area'):
                    area = self.reader.attributes().value('area').toString().toInt()[0]
                    widget.parent().addDockWidget(area, widget)

            if widget.inherits('QSplitter'):
                if self.reader.attributes().hasAttribute('sizes'):
                    sizes = []
                    for size in self.reader.attributes().value('sizes').toString().split(","):
                        sizes.append(size.toInt()[0])
                    widget.setSizes(sizes)

            if widget.inherits('QTableView'):
                l = self.reader.attributes().value('headerSections').toString().split(",")
                for index in xrange(l.count()):
                    widget.horizontalHeader().resizeSection(index, l[index].toInt()[0])

            if widget.inherits('QToolBar'):
                if self.reader.attributes().hasAttribute('visible'):
                    visible = self.reader.attributes().value('visible').toString().toInt()[0]
                    widget.setVisible(visible)

        while not self.reader.atEnd():
            self.reader.readNext()
            if self.reader.isEndElement():
                break
            if self.reader.isStartElement():
                self.readElement()

