# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

from exceptions import Exception
from PyQt4 import QtCore, QtSql

class SqlQueryModelEx(QtSql.QSqlQueryModel):

    def __init__(self, parent, columns, from_, where=None, order=None, group=None, limit=None):
        super(SqlQueryModelEx, self).__init__(parent)
        self.columns = columns
        self.from_ = from_
        self.where = where
        self.order = order
        self.group = group
        self.limit = limit
        self.values = []
        self.oldsql = None
        self.oldvalues = []
        self.query = QtSql.QSqlQuery()

    def setColumns(self, columns):
        self.columns = columns

    def setFromClause(self, from_):
        self.from_ = from_

    def setWhereClause(self, where):
        self.where = where

    def setOrderByClause(self, order):
        self.order = order

    def setGroupByClause(self, group):
        self.group = group

    def setLimit(self, limit):
        self.limit = limit

    def addBindValue(self, value):
        self.values.append(value)

    def select(self, force=False):
        l = QtCore.QStringList("SELECT")
        l.append(self.columns)
        l.append("FROM")
        l.append(self.from_)
        if self.where:
            l.append("WHERE")
            l.append(self.where)
        if self.group:
            l.append("GROUP BY")
            l.append(self.group)
        if self.order:
            l.append("ORDER BY")
            l.append(self.order)
        if self.limit:
            l.append("LIMIT")
            l.append(self.limit)
        sql = l.join(" ")
        if force or sql != self.oldsql or self.values != self.oldvalues:
            self.query.prepare(sql)
            for value in self.values:
                self.query.addBindValue(value)
            if not self.query.exec_():
                raise Exception, self.query.lastError().text()
            self.setQuery(self.query)
        self.oldsql = sql
        self.oldvalues = self.values
        self.values = []

    def refresh(self):
        self.values = self.oldvalues
        self.select(True)

    def sort(self, column, order):
        if order == QtCore.Qt.AscendingOrder:
            self.setOrderByClause(QtCore.QString("%1").arg(column + 1))
        else:
            self.setOrderByClause(QtCore.QString("%1 DESC").arg(column + 1))
        self.refresh()

