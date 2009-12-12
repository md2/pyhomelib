# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79

from PyQt4 import QtCore, QtSql
from fb2streamreader import FB2StreamReader
from bookdblayer import *


class ImportThread(QtCore.QThread):

    error = QtCore.pyqtSignal(QtCore.QString)
    processed = QtCore.pyqtSignal(QtCore.QString)

    def __init__(self, dbname, directory, parent=None):
        super(ImportThread, self).__init__(parent)
        self.dbname = dbname
        self.directory = directory
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.filenames = QtCore.QStringList()
        self.abort = False

    def quit(self):
        locker = QtCore.QMutexLocker(self.mutex)
        self.abort = True
        self.condition.wakeOne()

    def addFilename(self, filename):
        locker = QtCore.QMutexLocker(self.mutex)
        self.filenames.append(filename)
        self.condition.wakeOne()

    def takeFilename(self):
        locker = QtCore.QMutexLocker(self.mutex)
        if self.filenames.isEmpty():
            self.condition.wait(self.mutex)
        if not self.filenames.isEmpty():
            return self.filenames.takeFirst()
        else:
            return None

    def MD5(self, filename):
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.ReadOnly):
            return None
        return QtCore.QCryptographicHash.hash(file.readAll(),
                                        QtCore.QCryptographicHash.Md5).toHex()

    def selectBookByFilename(self, db, filename):
        bookid = execScalar(db, "SELECT bookid FROM libfilename WHERE filename = ? LIMIT 1",
                            filename)
        if bookid:
            return bookid.toInt()[0]
        return None

    def selectBookByMd5(self, db, md5):
        bookid = execScalar(db, "SELECT bookid FROM libbook WHERE md5 = ? LIMIT 1",
                            md5)
        if bookid:
            return bookid.toInt()[0]
        return None

    def insertBook(self, db, title, lang, year, fileauthor, size, md5):
        return execUpdate(db, "INSERT INTO libbook(title, lang, year, fileauthor, filesize, md5) VALUES(?,?,?,?,?,?)",
                          title, lang, year, fileauthor, size, md5)

    def selectAuthorByName(self, db, firstname, middlename, lastname, nickname):
        query = QtSql.QSqlQuery(db)
        query.prepare("SELECT authorid FROM libauthorname WHERE lastname=? AND firstname=? AND middlename=? AND nickname=?")
        for s in (lastname, firstname, middlename, nickname):
            if s.isNull():
                query.addBindValue("")
            else:
                query.addBindValue(s)
        if not query.exec_():
            raise Exception, query.lastError().text()
        if query.next():
            return query.value(0).toInt()[0]
        return None

    def insertAuthor(self, db, firstname, middlename, lastname, nickname):
        query = QtSql.QSqlQuery(db)
        query.prepare("INSERT INTO libauthorname (firstname, middlename, lastname, nickname) VALUES(?,?,?,?)")
        for s in (firstname, middlename, lastname, nickname):
            if s.isNull():
                query.addBindValue("")
            else:
                query.addBindValue(s)
        if not query.exec_():
            raise Exception, query.lastError().text()
        return query.lastInsertId().toInt()[0]

    def insertBookAuthorRelation(self, db, bookid, authorid):
        execUpdate(db, "INSERT OR IGNORE INTO libauthor(bookid, authorid) VALUES(?,?)",
                   bookid, authorid)

    def selectGenreByCode(self, db, genrecode):
        genreid = execScalar(db, "SELECT genreid FROM libgenrelist WHERE genrecode = ?",
                             genrecode)
        if genreid:
            return genreid.toInt()[0]
        return None

    def insertBookGenreRelation(self, db, bookid, genreid):
        execUpdate(db, "INSERT OR IGNORE INTO libgenre(bookid, genreid) VALUES(?,?)",
                   bookid, genreid)

    def selectSequenceByName(self, db, seqname):
        seqid = execScalar(db, "SELECT seqid FROM libseqname WHERE seqname = ?",
                           seqname)
        if seqid:
            return seqid.toInt()[0]
        return None

    def insertBookSeqRelation(self, db, bookid, seqid, seqnum):
        execUpdate(db, "INSERT OR IGNORE INTO libsequence(bookid, seqid, seqnum) VALUES(?,?,?)",
                   bookid, seqid, seqnum)

    def insertSequence(self, db, seqname):
        return execUpdate(db, "INSERT INTO libseqname (seqname) VALUES(?)",
                          seqname)

    def updateBookInfo(self, db, bookid, authorid, genreid, seqid):
        execUpdate(db, "UPDATE libbook SET authorid = ?, genreid = ?, seqid = ? WHERE bookid = ?",
                   authorid, genreid, seqid, bookid)

    def insertFilename(self, db, bookid, filename):
        execUpdate(db, "INSERT INTO libfilename(bookid, filename) VALUES(?,?)",
                   bookid, filename)

    def run(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.dbname)
        if not db.open():
            raise Exception, db.lastError().text()

        while not self.abort:
            filename = self.takeFilename()
            if filename:
                bookid = self.selectBookByFilename(db, filename)
                if not bookid:
                    md5 = self.MD5(filename)
                    bookid = self.selectBookByMd5(db, md5)
                    if bookid:
                        self.error.emit("<span style='color:red'>" +
                                        self.tr("Non-unique md5") + "</span>: " +
                                        QtCore.QDir(self.directory).relativeFilePath(filename))
                if not bookid:
                    parser = FB2StreamReader()
                    if not parser.read(filename):
                        self.error.emit("<span style='color:red'>" +
                                        self.tr("Parser error") + "</span>: " +
                                        QtCore.QDir(self.directory).relativeFilePath(filename))
                    else:
                        info = parser.info
                        size = QtCore.QFileInfo(filename).size()

                        try:
                            db.transaction()
                            if info.documentAuthors:
                                fileauthor = info.documentAuthors[0].makeName()
                            else:
                                fileauthor = None
                            bookid = self.insertBook(db, info.bookTitle,
                                                     info.Lang, info.Year,
                                                     fileauthor, size, md5)

                            _authorid, _genreid, _seqid = None, None, None

                            for author in info.Authors:
                                authorid = self.selectAuthorByName(db,
                                                                   author.firstName,
                                                                   author.middleName,
                                                                   author.lastName,
                                                                   author.nickName)
                                if not authorid:
                                    authorid = self.insertAuthor(db,
                                                                 author.firstName,
                                                                 author.middleName,
                                                                 author.lastName,
                                                                 author.nickName)
                                self.insertBookAuthorRelation(db, bookid, authorid)
                                if not _authorid:
                                    _authorid = authorid

                            for genrecode in info.Genres:
                                genreid = self.selectGenreByCode(db, genrecode)
                                if genreid:
                                    self.insertBookGenreRelation(db, bookid, genreid)
                                    if not _genreid:
                                        _genreid = genreid

                            for seq in info.Sequences + info.publisherSequences:
                                seqid = self.selectSequenceByName(db, seq.sequenceName)
                                if not seqid:
                                    seqid = self.insertSequence(db, seq.sequenceName)
                                self.insertBookSeqRelation(db, bookid, seqid, seq.sequenceNumber)
                                if not _seqid:
                                    _seqid = seqid

                            if _authorid or _genreid or _seqid:
                                self.updateBookInfo(db, bookid, _authorid, _genreid, _seqid)

                            self.insertFilename(db, bookid, filename)

                        except Exception, msg:
                            self.error.emit("<span style='color:red'>" +
                                            self.tr("Database error") + "</span>: " +
                                            QtCore.QString.fromUtf8(str(msg)))
                            db.rollback()

                        else:
                            if not db.commit():
                                self.error.emit("<span style='color:red'>" +
                                                self.tr("Database error") + "</span>: " +
                                                db.lastError().text())
                self.processed.emit(filename)

