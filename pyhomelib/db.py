# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import weakref
from PyQt4 import QtSql


class DatabaseError(Exception):
    pass


class Db(object):
    def __init__(self, connectionName=None, db_to_clone=None, type='QSQLITE'):
        super(Db, self).__init__()
        if connectionName is None:
            assert not (QtSql.QSqlDatabase.contains())
        else:
            assert not (QtSql.QSqlDatabase.contains(connectionName))
        assert (db_to_clone is None) or (connectionName is not None)

        if connectionName is None:
            db = QtSql.QSqlDatabase.addDatabase(type)
        else:
            if db_to_clone is None:
                db = QtSql.QSqlDatabase.addDatabase(type, connectionName)
            else:
                db = QtSql.QSqlDatabase.cloneDatabase(db_to_clone, connectionName)
        self._db = db
        self._weak_dict = weakref.WeakValueDictionary()

    def __del__(self):
        self._db.close()
        connectionName = self._db.connectionName()
        del self._db
        QtSql.QSqlDatabase.removeDatabase(connectionName)

    def __getattr__(self, name):
        return getattr(self._db, name)

    @property
    def name(self):
        return self._db.databaseName()

    def open(self, databaseName=None):
        db = self._db
        db.close()
        if databaseName is not None:
            db.setDatabaseName(databaseName)
        if not db.open():
            raise DatabaseError, db.lastError().text()

    def execScalar(self, sql, *values):
        query = QtSql.QSqlQuery(self._db)
        query.prepare(sql)
        for value in values:
            query.addBindValue(value)
        if not query.exec_():
            raise DatabaseError, query.lastError().text()
        if query.next():
            return query.value(0)
        return None

    def execUpdate(self, sql, *values):
        query = QtSql.QSqlQuery(self._db)
        query.prepare(sql)
        for value in values:
            query.addBindValue(value)
        if not query.exec_():
            raise DatabaseError, query.lastError().text()
        return query.lastInsertId().toInt()[0]

    def newQuery(self):
        query = QtSql.QSqlQuery(self._db)
        self._weak_dict[id(query)] = query
        return query

    def finishActiveQueries(self):
        for ref in self._weak_dict.valuerefs():
            query = ref()
            if query is not None and query.isActive():
                query.finish()

