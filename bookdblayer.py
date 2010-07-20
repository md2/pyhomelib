# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore, QtSql
from db import Db, DatabaseError


schema = """
        CREATE TABLE IF NOT EXISTS info
                                        (name varchar(32),
                                         value varchar(255),
                                         PRIMARY KEY (name));

        CREATE TABLE IF NOT EXISTS libbook
                                        (bookid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                         title varchar(255),
                                         lang char(2),
                                         year smallint,
                                         authorid integer,
                                         genreid integer,
                                         seqid integer,
                                         fileauthor varchar(64),
                                         filetype char(4) NOT NULL DEFAULT '',
                                         filesize int,
                                         md5 char(32) NOT NULL,
                                         UNIQUE (md5));

        CREATE TABLE IF NOT EXISTS libauthor
                                        (bookid integer,
                                         authorid integer,
                                         PRIMARY KEY (bookid, authorid));

        CREATE TABLE IF NOT EXISTS libauthorname
                                        (authorid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                         firstname varchar(99) NOT NULL DEFAULT '',
                                         middlename varchar(99) NOT NULL DEFAULT '',
                                         lastname varchar(99) NOT NULL DEFAULT '',
                                         nickname varchar(33) NOT NULL DEFAULT '');

        CREATE TABLE IF NOT EXISTS libsequence
                                        (bookid integer,
                                         seqid integer,
                                         seqnum int,
                                         PRIMARY KEY (bookid, seqid));

        CREATE TABLE IF NOT EXISTS libseqname
                                        (seqid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                         seqname varchar(255),
                                         UNIQUE (seqname));

        CREATE TABLE IF NOT EXISTS libgenre
                                        (bookid integer,
                                         genreid integer,
                                         PRIMARY KEY (bookid, genreid));

        CREATE TABLE IF NOT EXISTS libgenrelist
                                        (genreid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                         genrecode varchar(45),
                                         genredesc varchar(99),
                                         UNIQUE(genrecode));

        CREATE TABLE IF NOT EXISTS libfilename
                                        (bookid integer,
                                         filename varchar(32767),
                                         PRIMARY KEY(bookid),
                                         UNIQUE(filename));

        CREATE TABLE IF NOT EXISTS libgrouplist
                                        (groupid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                         groupname varchar(32),
                                         UNIQUE(groupname));

        CREATE TABLE IF NOT EXISTS libgroup
                                        (bookid integer,
                                         groupid integer,
                                         PRIMARY KEY (bookid, groupid));

        CREATE INDEX IF NOT EXISTS idx_libbook_title ON libbook(title);
        CREATE INDEX IF NOT EXISTS idx_libbook_lang ON libbook(lang);
        CREATE INDEX IF NOT EXISTS idx_libbook_authorid ON libbook(authorid);
        CREATE INDEX IF NOT EXISTS idx_libbook_genreid ON libbook(genreid);
        CREATE INDEX IF NOT EXISTS idx_libbook_seqid ON libbook(seqid);
        CREATE INDEX IF NOT EXISTS idx_libbook_fileauthor ON libbook(fileauthor);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_libbook_md5 ON libbook(md5);

        CREATE INDEX IF NOT EXISTS idx_libauthor_bookid ON libauthor(bookid);
        CREATE INDEX IF NOT EXISTS idx_libauthor_authorid ON libauthor(authorid);

        CREATE INDEX IF NOT EXISTS idx_libauthorname_firstname ON libauthorname(firstname);
        CREATE INDEX IF NOT EXISTS idx_libauthorname_middlename ON libauthorname(middlename);
        CREATE INDEX IF NOT EXISTS idx_libauthorname_lastname ON libauthorname(lastname);
        CREATE INDEX IF NOT EXISTS idx_libauthorname_nickname ON libauthorname(nickname);

        CREATE INDEX IF NOT EXISTS idx_libsequence_bookid ON libsequence(bookid);
        CREATE INDEX IF NOT EXISTS idx_libsequence_seqid ON libsequence(seqid);

        CREATE UNIQUE INDEX IF NOT EXISTS idx_libseqname_seqname ON libseqname(seqname);

        CREATE INDEX IF NOT EXISTS idx_libgenre_bookid ON libgenre(bookid);
        CREATE INDEX IF NOT EXISTS idx_libgenre_genreid ON libgenre(genreid);

        CREATE UNIQUE INDEX IF NOT EXISTS idx_libfilename_filename ON libfilename(filename);

        CREATE INDEX IF NOT EXISTS idx_libgroup_bookid ON libgroup(bookid);
        CREATE INDEX IF NOT EXISTS idx_libgroup_groupid ON libgroup(groupid)
        """


class BookDbLayer(object):
    def __init__(self, connectionName=None, db_to_clone=None):
        super(BookDbLayer, self).__init__()
        self._db = Db(connectionName, db_to_clone)

    def __getattr__(self, name):
        return getattr(self._db, name)

    def create(self, databaseName, name, description, genrelist, grouplist):
        db = self._db
        db.open(databaseName)
        db.transaction()
        try:
            for statement in schema.split(';'):
                db.execUpdate(statement)

            for pair in [('version', 1),
                         ('name', name),
                         ('description', description)]:
                db.execUpdate("INSERT INTO info(name, value) VALUES(?,?)",
                              pair[0], pair[1])

            for genre in genrelist:
                db.execUpdate("INSERT INTO libgenrelist(genreid, genrecode, genredesc) VALUES(?,?,?)",
                              genre[0], genre[1], genre[2])

            for groupname in grouplist:
                db.execUpdate("INSERT INTO libgrouplist(groupname) VALUES(?)",
                              groupname)

        except DatabaseError:
            db.rollback()
            raise
        else:
            if not db.commit():
                raise DatabaseError, db.lastError().text()

    def getDbProperty(self, name):
        return self._db.execScalar("SELECT value FROM info WHERE name = ?",
                                   name)

    def setDbProperty(self, name, value):
        self._db.execUpdate("INSERT OR REPLACE INTO info(name, value) VALUES(?,?)",
                            name, value)

    def getBookCount(self):
        return self._db.execScalar("SELECT COUNT(*) FROM libbook").toLongLong()[0]

    def getFilenameByBookId(self, bookid):
        return self._db.execScalar("SELECT filename FROM libfilename WHERE bookid = ?",
                                   bookid).toString()

    def getGroupsBookIn(self, bookid):
        query = self._db.newQuery()
        query.prepare("SELECT groupid, groupname FROM libgroup JOIN libgrouplist USING(groupid) WHERE bookid = ?")
        query.addBindValue(bookid)
        if not query.exec_():
            raise DatabaseError, query.lastError().text()
        groups = []
        while query.next():
            groups.append((query.value(0).toInt()[0],
                           query.value(1).toString()))
        return groups

    def getGroupsBookNotIn(self, bookid):
        query = self._db.newQuery()
        query.prepare("SELECT groupid, groupname FROM libgrouplist WHERE groupid NOT IN (SELECT groupid FROM libgroup WHERE bookid = ?)")
        query.addBindValue(bookid)
        if not query.exec_():
            raise DatabaseError, query.lastError().text()
        groups = []
        while query.next():
            groups.append((query.value(0).toInt()[0],
                           query.value(1).toString()))
        return groups

    def addBookToGroup(self, bookid, groupid):
        self._db.execUpdate("INSERT INTO libgroup(bookid, groupid) VALUES(?,?)",
                            bookid, groupid)

    def removeBookFromGroup(self, bookid, groupid):
        self._db.execUpdate("DELETE FROM libgroup WHERE bookid = ? AND groupid = ?",
                            bookid, groupid)

    def addGroup(self, groupname):
        self._db.execUpdate("INSERT OR IGNORE INTO libgrouplist(groupname) VALUES(?)",
                            groupname)

    def removeGroup(self, groupid):
        db = self._db
        db.transaction()
        try:
            db.execUpdate("DELETE FROM libgroup WHERE groupid = ?",
                          groupid)
            db.execUpdate("DELETE FROM libgrouplist WHERE groupid = ?",
                          groupid)
        except DatabaseError:
            db.rollback()
            raise
        else:
            if not db.commit():
                raise DatabaseError, db.lastError().text()

    def removeAuthor(self, authorid):
        db = self._db
        db.transaction()
        try:
            db.execUpdate("DELETE FROM libauthor WHERE authorid = ?",
                          authorid)
            db.execUpdate("DELETE FROM libauthorname WHERE authorid = ?",
                          authorid)
            db.execUpdate("UPDATE libbook SET authorid = NULL WHERE authorid = ?",
                          authorid)
        except DatabaseError:
            db.rollback()
            raise
        else:
            if not db.commit():
                raise DatabaseError, db.lastError().text()

    def removeSequence(self, seqid):
        db = self._db
        db.transaction()
        try:
            db.execUpdate("DELETE FROM libsequence WHERE seqid = ?",
                          seqid)
            db.execUpdate("DELETE FROM libseqname WHERE seqid = ?",
                          seqid)
            db.execUpdate("UPDATE libbook SET seqid = NULL WHERE seqid = ?",
                          seqid)
        except DatabaseError:
            db.rollback()
            raise
        else:
            if not db.commit():
                raise DatabaseError, db.lastError().text()


