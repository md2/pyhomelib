# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

from PyQt4 import QtCore

class TreeItem(object):

    def __init__(self, description=None):
        super(TreeItem, self).__init__()
        self.description = description
        self.parentItem = None
        self.childItems = []

    def columnCount(self):
        return 1

    def data(self, column):
        if column == 0:
            return self.description
        else:
            return None

    def appendChild(self, item):
        self.childItems.append(item)
        item.parentItem = self

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class GenreTreeItem(TreeItem):

    def __init__(self, id, code, description):
        super(GenreTreeItem, self).__init__(description)
        self.id = id
        self.code = code

    def columnCount(self):
        return 0

    def data(self, column):
        if column == 0:
            return self.description
        elif column == 1:
            return self.id
        else:
            return None


class GroupTreeItem(TreeItem):

    def __init__(self, description):
        super(GroupTreeItem, self).__init__(description)

    def columnCount(self):
        return 2


class GenreTreeModelReader(QtCore.QAbstractItemModel):

    def __init__(self, filename, parent=None):
        super(GenreTreeModelReader, self).__init__(parent)
        self.xml = QtCore.QXmlStreamReader()
        self.groups = []
        self.rootItem = TreeItem()

        self.setupModelData(filename)

    def list(self):
        result = []
        for group in self.groups:
            for genre in group.childItems:
                result.append((genre.id,
                               genre.code,
                               genre.description))
        return result

    def genreDescByCode(self, code):
        for group in self.groups:
            for genre in group.childItems:
                if genre.code == code:
                    return genre.description
        return code

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        if not self.parent(index).isValid():
            return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, filename):
        file = QtCore.QFile(filename)
        file.open(QtCore.QFile.ReadOnly)
        self.xml.setDevice(file)
        self.read()

    def read(self):
        while not self.xml.atEnd():
            self.xml.readNext()
            if self.xml.isStartElement():
                if self.xml.name() == 'genres':
                    self.readGenres()
                else:
                    self.xml.raiseError("Parser error")
        return not self.xml.hasError()

    def readUnknownElement(self):
        while not self.xml.atEnd():
            self.xml.readNext()
            if self.xml.isEndElement():
                break
            if self.xml.isStartElement():
                self.readUnknownElement()

    def readGenres(self):
        while not self.xml.atEnd():
            self.xml.readNext()
            if self.xml.isEndElement():
                break
            if self.xml.isStartElement():
                if self.xml.name() == 'group':
                    self.readGroup()
                else:
                    self.readUnknownElement()

    def readGroup(self):
        desc = self.xml.attributes().value('description').toString()
        group = GroupTreeItem(desc)
        self.groups.append(group)
        self.rootItem.appendChild(group)
        while not self.xml.atEnd():
            self.xml.readNext()
            if self.xml.isEndElement():
                break
            if self.xml.isStartElement():
                if self.xml.name() == 'genre':
                    self.readGenre()
                else:
                    self.readUnknownElement()

    def readGenre(self):
        id = self.xml.attributes().value('id').toString().toInt()[0]
        code = self.xml.attributes().value('code').toString()
        desc = self.xml.attributes().value('description').toString()
        self.xml.readNext()
        genre = GenreTreeItem(id, code, desc)
        self.groups[-1].appendChild(genre)

