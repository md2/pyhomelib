# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

from exceptions import Exception
from PyQt4 import QtCore, QtSql

schema = """
        CREATE TABLE IF NOT EXISTS info (name varchar(32),
                                         value varchar(255),
                                         PRIMARY KEY (name));

        CREATE TABLE IF NOT EXISTS libbook (bookid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                            title varchar(255),
                                            lang char(2),
                                            year smallint,
                                            authorid integer,
                                            genreid integer,
                                            seqid integer,
                                            fileauthor varchar(64),
                                            filetype char(4) NOT NULL DEFAULT 'fb2',
                                            filesize int,
                                            md5 char(32) NOT NULL,
                                            UNIQUE (md5));

        CREATE TABLE IF NOT EXISTS libauthor (bookid integer,
                                              authorid integer,
                                              PRIMARY KEY (bookid, authorid));

        CREATE TABLE IF NOT EXISTS libauthorname (authorid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                  firstname varchar(99) NOT NULL DEFAULT '',
                                                  middlename varchar(99) NOT NULL DEFAULT '',
                                                  lastname varchar(99) NOT NULL DEFAULT '',
                                                  nickname varchar(33) NOT NULL DEFAULT '');

        CREATE TABLE IF NOT EXISTS libsequence (bookid integer,
                                                seqid integer,
                                                seqnum int,
                                                PRIMARY KEY (bookid, seqid));

        CREATE TABLE IF NOT EXISTS libseqname (seqid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                               seqname varchar(255),
                                               UNIQUE (seqname));

        CREATE TABLE IF NOT EXISTS libgenre (bookid integer,
                                             genreid integer,
                                             PRIMARY KEY (bookid, genreid));

        CREATE TABLE IF NOT EXISTS libgenrelist (genreid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                 genrecode varchar(45),
                                                 genredesc varchar(99),
                                                 UNIQUE(genrecode));

        CREATE TABLE IF NOT EXISTS libfilename (bookid integer,
                                                filename varchar(32767),
                                                PRIMARY KEY(bookid),
                                                UNIQUE(filename));

        CREATE TABLE IF NOT EXISTS libgrouplist (groupid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                 groupname varchar(32),
                                                 UNIQUE(groupname));

        CREATE TABLE IF NOT EXISTS libgroup (bookid integer,
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

def db():
    return QtSql.QSqlDatabase.database("qt_sql_default_connection", False)

def dbName():
    return db().databaseName()

def execUpdate(db, sql, *values):
    query = QtSql.QSqlQuery(db)
    query.prepare(sql)
    for value in values:
        query.addBindValue(value)
    if not query.exec_():
        raise Exception, query.lastError().text()
    return query.lastInsertId().toInt()[0]

def execScalar(db, sql, *values):
    query = QtSql.QSqlQuery(db)
    query.prepare(sql)
    for value in values:
        query.addBindValue(value)
    if not query.exec_():
        raise Exception, query.lastError().text()
    if query.next():
        return query.value(0)
    return None

def createDb(dbname, name, description, genrelist, grouplist):
    db().close()
    db().setDatabaseName(dbname)
    if not db().open():
        raise Exception, db().lastError().text()
    db().transaction()
    try:
        for statement in schema.split(';'):
            execUpdate(db(), statement)

        for pair in [('version', 1),
                     ('name', name),
                     ('description', description)]:
            execUpdate(db(), "INSERT INTO info(name, value) VALUES(?,?)",
                       pair[0], pair[1])

        for genre in genrelist:
            execUpdate(db(), "INSERT INTO libgenrelist(genreid, genrecode, genredesc) VALUES(?,?,?)",
                       genre[0], genre[1], genre[2])

        for groupname in grouplist:
            execUpdate(db(), "INSERT INTO libgrouplist(groupname) VALUES(?)",
                       groupname)

    except Exception, msg:
        db().rollback()
        raise
    else:
        if not db().commit():
            raise Exception, db().lastError().text()

def openDb(dbname):
    db().close()
    db().setDatabaseName(dbname)
    if not db().open():
        raise Exception, db().lastError().text()

def getDbProperty(name):
    return execScalar(db(), "SELECT value FROM info WHERE name = ?",
                     name)

def setDbProperty(name, value):
    execUpdate(db(),
               "INSERT OR REPLACE INTO info(name, value) VALUES(?,?)",
               name, value)

def bookCount():
    return execScalar(db(), "SELECT COUNT(*) FROM libbook").toLongLong()[0]

def filenameByBookId(bookid):
    return execScalar(db(),
                      "SELECT filename FROM libfilename WHERE bookid = ?",
                      bookid).toString()

def getGroupsBookIn(bookid):
    query = QtSql.QSqlQuery()
    query.prepare("SELECT groupid, groupname FROM libgroup JOIN libgrouplist USING(groupid) WHERE bookid = ?")
    query.addBindValue(bookid)
    if not query.exec_():
        raise Exception, query.lastError().text()
    groups = []
    while query.next():
        groups.append((query.value(0).toInt()[0],
                       query.value(1).toString()))
    return groups

def getGroupsBookNotIn(bookid):
    query = QtSql.QSqlQuery()
    query.prepare("SELECT groupid, groupname FROM libgrouplist WHERE groupid NOT IN (SELECT groupid FROM libgroup WHERE bookid = ?)")
    query.addBindValue(bookid)
    if not query.exec_():
        raise Exception, query.lastError().text()
    groups = []
    while query.next():
        groups.append((query.value(0).toInt()[0],
                       query.value(1).toString()))
    return groups

def addBookToGroup(bookid, groupid):
    execUpdate(db(), "INSERT INTO libgroup(bookid, groupid) VALUES(?,?)",
               bookid, groupid)

def removeBookFromGroup(bookid, groupid):
    execUpdate(db(), "DELETE FROM libgroup WHERE bookid = ? AND groupid = ?",
               bookid, groupid)

def addGroup(groupname):
    execUpdate(db(), "INSERT OR IGNORE INTO libgrouplist(groupname) VALUES(?)",
               groupname)

def removeGroup(groupid):
    db().transaction()
    try:
        execUpdate(db(), "DELETE FROM libgroup WHERE groupid = ?",
                   groupid)
        execUpdate(db(), "DELETE FROM libgrouplist WHERE groupid = ?",
                   groupid)
    except Exception, msg:
        db().rollback()
        raise
    else:
        if not db().commit():
            raise Exception, db().lastError().text()

def removeAuthor(authorid):
    db().transaction()
    try:
        execUpdate(db(), "DELETE FROM libauthor WHERE authorid = ?",
                   authorid)
        execUpdate(db(), "DELETE FROM libauthorname WHERE authorid = ?",
                   authorid)
        execUpdate(db(), "UPDATE libbook SET authorid=NULL WHERE authorid = ?",
                   authorid)
    except Exception, msg:
        db().rollback()
        raise
    else:
        if not db().commit():
            raise Exception, db().lastError().text()

def removeSequence(seqid):
    db().transaction()
    try:
        execUpdate(db(), "DELETE FROM libsequence WHERE seqid = ?",
                   seqid)
        execUpdate(db(), "DELETE FROM libseqname WHERE seqid = ?",
                   seqid)
        execUpdate(db(), "UPDATE libbook SET seqid=NULL WHERE seqid = ?",
                   seqid)
    except Exception, msg:
        db().rollback()
        raise
    else:
        if not db().commit():
            raise Exception, db().lastError().text()

