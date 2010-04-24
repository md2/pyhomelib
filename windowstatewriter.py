# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore

class WindowStateWriter(object):

    def __init__(self):
        super(WindowStateWriter, self).__init__()
        self.writer = QtCore.QXmlStreamWriter()

    def writeStateTo(self, filename):
        file = QtCore.QFile(filename)
        if file.open(QtCore.QFile.WriteOnly):
            self.writer.setDevice(file)
            self.writer.setAutoFormatting(True)
            self.writer.writeStartDocument()
            self.saveWidgetState(self)
            self.writer.writeEndDocument()

    def saveWidgetState(self, widget):
        classname = widget.metaObject().className()
        self.writer.writeStartElement(classname)
        self.writer.writeAttribute('name', widget.objectName())

        currentIndex = widget.property('currentIndex')
        if currentIndex.isValid():
            self.writer.writeAttribute('currentIndex', currentIndex.toString())

        if widget.inherits('QMainWindow'):
            if widget.windowState() and QtCore.Qt.WindowMaximized:
                self.writer.writeAttribute('maximized', '1')
            else:
                l = QtCore.QStringList()
                for num in (widget.geometry().left(), widget.geometry().top(),
                            widget.geometry().width(), widget.geometry().height()):
                    l.append(QtCore.QString.number(num))
                self.writer.writeAttribute('geometry', l.join(","))

        if widget.inherits('QDockWidget'):
            if not widget.isVisible():
                self.writer.writeAttribute('visible', '0')
            area = widget.parent().dockWidgetArea(widget)
            self.writer.writeAttribute('area', QtCore.QString.number(area))

        if widget.inherits('QSplitter'):
            l = QtCore.QStringList()
            for size in widget.sizes():
                l.append(QtCore.QString.number(size))
            self.writer.writeAttribute('sizes', l.join(","))

        if widget.inherits('QTableView'):
            l = QtCore.QStringList()
            header = widget.horizontalHeader()
            for index in range(header.count()):
                l.append(QtCore.QString.number(header.sectionSize(index)))
            self.writer.writeAttribute('headerSections', l.join(","))
            l.clear()
            for index in range(header.count()):
                l.append(QtCore.QString.number(header.visualIndex(index)))
            self.writer.writeAttribute('visualOrder', l.join(","))

        if widget.inherits('QToolBar'):
            if not widget.isVisible():
                self.writer.writeAttribute('visible', '0')

        for child in widget.children():
            if child.isWidgetType() and not child.objectName().isEmpty() \
                                    and not child.objectName().startsWith("qt_"):
                self.saveWidgetState(child)

        self.writer.writeEndElement()

