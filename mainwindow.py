# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import os
import sys
from exceptions import Exception
from PyQt4 import QtCore, QtSql, QtGui
from ui_mainwindow import Ui_MainWindow
from dbpropertiesdialog import DbPropertiesDialog
from windowstatereader import WindowStateReader
from windowstatewriter import WindowStateWriter
from genretreemodelreader import GenreTreeModelReader
from bookdblayer import *
from fb2streamreader import FB2StreamReader
from fb2bookparserthread import FB2BookParserThread
from sqlquerymodelex import SqlQueryModelEx
from settingsdialog import SettingsDialog
from statisticsdialog import StatisticsDialog
from mysettings import MySettings

class MainWindow(QtGui.QMainWindow, Ui_MainWindow,
                 WindowStateReader, WindowStateWriter):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        WindowStateReader.__init__(self)
        WindowStateWriter.__init__(self)

        if not QtSql.QSqlDatabase.drivers().contains("QSQLITE"):
            raise Exception, "Fatal error: QSQLITE database driver is not found!"

        self.userConfigDir = QtCore.QDir.homePath() + QtCore.QDir.separator() + \
                             '.pyhomelib';
        if not QtCore.QFileInfo(self.userConfigDir).isDir():
            QtCore.QDir.home().mkdir('.pyhomelib')
        self.uiSettingsFile = self.userConfigDir + QtCore.QDir.separator() + \
                              'ui.xml'
        self.programSettings = MySettings(self.userConfigDir +
                                          QtCore.QDir.separator() +
                                          'pyhomelib.conf')

        if len(sys.argv) < 2:
            dbname = self.userConfigDir + QtCore.QDir.separator() + \
                     'default.sqlite'
        else:
            dbname = QtCore.QString.fromUtf8(sys.argv[1])

        QtSql.QSqlDatabase.addDatabase("QSQLITE")

        genreModel = GenreTreeModelReader('genres.xml')

        info = QtCore.QFileInfo(dbname)
        if info.exists() and info.size() > 0:
            openDb(dbname)
        else:
            QtGui.QMessageBox.information(self, self.tr("Information"),
                QtCore.QString(self.tr("Database doesn't exists, recreating: %1"))
                .arg(dbname))
            createDb(dbname, 'Default', '', genreModel.list(),
                     [self.tr('Favorites')])

        self.setupUi(self)
        self.appTitle = self.windowTitle()
        self.appendToTitle(getDbProperty('name').toString())
        self.actionRuLetterA.setText(u"А")
        self.actionRuLetterB.setText(u"Б")
        self.actionRuLetterV.setText(u"В")
        self.actionRuLetterG.setText(u"Г")
        self.actionRuLetterD.setText(u"Д")
        self.actionRuLetterE.setText(u"Е")
        self.actionRuLetterYo.setText(u"Ё")
        self.actionRuLetterZh.setText(u"Ж")
        self.actionRuLetterZ.setText(u"З")
        self.actionRuLetterI.setText(u"И")
        self.actionRuLetterY.setText(u"Й")
        self.actionRuLetterK.setText(u"К")
        self.actionRuLetterL.setText(u"Л")
        self.actionRuLetterM.setText(u"М")
        self.actionRuLetterN.setText(u"Н")
        self.actionRuLetterO.setText(u"О")
        self.actionRuLetterP.setText(u"П")
        self.actionRuLetterR.setText(u"Р")
        self.actionRuLetterS.setText(u"С")
        self.actionRuLetterT.setText(u"Т")
        self.actionRuLetterU.setText(u"У")
        self.actionRuLetterF.setText(u"Ф")
        self.actionRuLetterH.setText(u"Х")
        self.actionRuLetterTs.setText(u"Ц")
        self.actionRuLetterCh.setText(u"Ч")
        self.actionRuLetterSh.setText(u"Ш")
        self.actionRuLetterSch.setText(u"Щ")
        self.actionRuLetterYy.setText(u"Ы")
        self.actionRuLetterEe.setText(u"Э")
        self.actionRuLetterYu.setText(u"Ю")
        self.actionRuLetterYa.setText(u"Я")

        self.lettersGroup = QtGui.QActionGroup(self)
        for a in self.findChildren(QtGui.QAction):
            if a.objectName().startsWith('actionRuLetter') or \
               a.objectName().startsWith('actionEnLetter'):
                self.lettersGroup.addAction(a)

        self.authorsModel = SqlQueryModelEx(self, "authorid, lastname, firstname",
                                                  "libauthorname",
                                                  None,
                                                  "lastname, firstname")
        self.authorsView.setModel(self.authorsModel)
        self.setTableAuthorsModelQuery()
        self.authorsView.hideColumn(0)
        self.authorsView.model().setHeaderData(1, QtCore.Qt.Horizontal, self.tr("Last name"))
        self.authorsView.model().setHeaderData(2, QtCore.Qt.Horizontal, self.tr("First name"))

        self.sequencesModel = SqlQueryModelEx(self, "seqid, seqname",
                                                    "libseqname",
                                                    None,
                                                    "seqname")
        self.sequencesView.setModel(self.sequencesModel)
        self.sequencesModel.select()
        self.sequencesView.hideColumn(0)
        self.sequencesView.model().setHeaderData(1, QtCore.Qt.Horizontal, self.tr("Sequence"))

        self.genresTree.setModel(genreModel)
        self.genresTree.hideColumn(1)


        self.bookSearchModel = SqlQueryModelEx(self, "b.bookid, firstname, lastname, title, seqname, genredesc, lang, year",
                                                     "libbook b LEFT JOIN libsequence s ON b.bookid = s.bookid LEFT JOIN libseqname sn ON s.seqid = sn.seqid LEFT JOIN libauthor a ON b.bookid = a.bookid LEFT JOIN libauthorname an ON a.authorid = an.authorid LEFT JOIN libgenre g ON b.bookid = g.bookid LEFT JOIN libgenrelist gl ON g.genreid = gl.genreid",
                                                     "b.bookid = 0",
                                                     None,
                                                     "1")
        self.bookSearchView.setModel(self.bookSearchModel)
        self.bookSearchModel.select()
        self.bookSearchView.hideColumn(0)
        self.bookSearchModel.setHeaderData(1, QtCore.Qt.Horizontal, self.tr("First name"))
        self.bookSearchModel.setHeaderData(2, QtCore.Qt.Horizontal, self.tr("Last name"))
        self.bookSearchModel.setHeaderData(3, QtCore.Qt.Horizontal, self.tr("Book Title"))
        self.bookSearchModel.setHeaderData(4, QtCore.Qt.Horizontal, self.tr("Sequence"))
        self.bookSearchModel.setHeaderData(5, QtCore.Qt.Horizontal, self.tr("Genre"))
        self.bookSearchModel.setHeaderData(6, QtCore.Qt.Horizontal, self.tr("Lang"))
        self.bookSearchModel.setHeaderData(7, QtCore.Qt.Horizontal, self.tr("Year"))

        self.groupsModel = SqlQueryModelEx(self, "groupid, groupname",
                                                 "libgrouplist",
                                                 None,
                                                 "groupname")
        self.groupsView.setModel(self.groupsModel)
        self.groupsModel.select()
        self.groupsView.hideColumn(0)
        self.groupsView.model().setHeaderData(1, QtCore.Qt.Horizontal, self.tr("Group"))

        self.booksByAuthorModel = SqlQueryModelEx(self, "bookid, title, seqname, genredesc, lang, year",
                                                        "libauthor a INNER JOIN libbook b USING(bookid) LEFT JOIN libseqname s ON b.seqid = s.seqid LEFT JOIN libgenrelist g ON b.genreid = g.genreid",
                                                        "a.authorid = ?")
        self.booksByAuthorView.setModel(self.booksByAuthorModel)
        self.booksByAuthorModel.addBindValue(0)
        self.booksByAuthorModel.select()
        self.booksByAuthorView.hideColumn(0)
        self.booksByAuthorModel.setHeaderData(1, QtCore.Qt.Horizontal, self.tr("Book Title"))
        self.booksByAuthorModel.setHeaderData(2, QtCore.Qt.Horizontal, self.tr("Sequence"))
        self.booksByAuthorModel.setHeaderData(3, QtCore.Qt.Horizontal, self.tr("Genre"))
        self.booksByAuthorModel.setHeaderData(4, QtCore.Qt.Horizontal, self.tr("Lang"))
        self.booksByAuthorModel.setHeaderData(5, QtCore.Qt.Horizontal, self.tr("Year"))

        self.booksBySeqModel = SqlQueryModelEx(self, "bookid, firstname, lastname, title, genredesc, lang, year",
                                                     "libsequence s INNER JOIN libbook b USING(bookid) LEFT JOIN libauthorname a ON b.authorid = a.authorid LEFT JOIN libgenrelist g ON b.genreid = g.genreid",
                                                     "s.seqid = ?")
        self.booksBySeqView.setModel(self.booksBySeqModel)
        self.booksBySeqModel.addBindValue(0)
        self.booksBySeqModel.select()
        self.booksBySeqView.hideColumn(0)
        self.booksBySeqModel.setHeaderData(1, QtCore.Qt.Horizontal, self.tr("First name"))
        self.booksBySeqModel.setHeaderData(2, QtCore.Qt.Horizontal, self.tr("Last name"))
        self.booksBySeqModel.setHeaderData(3, QtCore.Qt.Horizontal, self.tr("Book Title"))
        self.booksBySeqModel.setHeaderData(4, QtCore.Qt.Horizontal, self.tr("Genre"))
        self.booksBySeqModel.setHeaderData(5, QtCore.Qt.Horizontal, self.tr("Lang"))
        self.booksBySeqModel.setHeaderData(6, QtCore.Qt.Horizontal, self.tr("Year"))

        self.booksByGenreModel = SqlQueryModelEx(self, "bookid, firstname, lastname, title, seqname, lang, year",
                                                       "libgenre g INNER JOIN libbook b USING(bookid) LEFT JOIN libauthorname a ON b.authorid = a.authorid LEFT JOIN libseqname s ON b.seqid = s.seqid",
                                                       "g.genreid = ?")
        self.booksByGenreView.setModel(self.booksByGenreModel)
        self.booksByGenreModel.addBindValue(0)
        self.booksByGenreModel.select()
        self.booksByGenreView.hideColumn(0)
        self.booksByGenreModel.setHeaderData(1, QtCore.Qt.Horizontal, self.tr("First name"))
        self.booksByGenreModel.setHeaderData(2, QtCore.Qt.Horizontal, self.tr("Last name"))
        self.booksByGenreModel.setHeaderData(3, QtCore.Qt.Horizontal, self.tr("Book Title"))
        self.booksByGenreModel.setHeaderData(4, QtCore.Qt.Horizontal, self.tr("Sequence"))
        self.booksByGenreModel.setHeaderData(5, QtCore.Qt.Horizontal, self.tr("Lang"))
        self.booksByGenreModel.setHeaderData(6, QtCore.Qt.Horizontal, self.tr("Year"))

        self.booksByGroupModel = SqlQueryModelEx(self, "b.bookid, firstname, lastname, title, seqname, genredesc, lang, year",
                                                       "libgroup g INNER JOIN libbook b USING(bookid) LEFT JOIN libseqname s ON b.seqid = s.seqid LEFT JOIN libauthorname a ON b.authorid = a.authorid LEFT JOIN libgenrelist gl ON b.genreid = gl.genreid",
                                                       "g.groupid = ?")
        self.booksByGroupView.setModel(self.booksByGroupModel)
        self.booksByGroupModel.addBindValue(0)
        self.booksByGroupModel.select()
        self.booksByGroupView.hideColumn(0)
        self.booksByGroupModel.setHeaderData(1, QtCore.Qt.Horizontal, self.tr("First name"))
        self.booksByGroupModel.setHeaderData(2, QtCore.Qt.Horizontal, self.tr("Last name"))
        self.booksByGroupModel.setHeaderData(3, QtCore.Qt.Horizontal, self.tr("Book Title"))
        self.booksByGroupModel.setHeaderData(4, QtCore.Qt.Horizontal, self.tr("Sequence"))
        self.booksByGroupModel.setHeaderData(5, QtCore.Qt.Horizontal, self.tr("Genre"))
        self.booksByGroupModel.setHeaderData(6, QtCore.Qt.Horizontal, self.tr("Lang"))
        self.booksByGroupModel.setHeaderData(7, QtCore.Qt.Horizontal, self.tr("Year"))

        self.readStateFrom(self.uiSettingsFile)
        self.actionRussianAlphabet.setChecked(self.ruLettersToolbar.isVisibleTo(self))
        self.actionEnglishAlphabet.setChecked(self.enLettersToolbar.isVisibleTo(self))

        self.parserThread = FB2BookParserThread()
        self.parserThread.bookParsed.connect(self.bookParsed)
        self.parserThread.start()

    def __del__(self):
        self.parserThread.wait()

    def on_ruLettersToolbar_actionTriggered(self, action):
        self.setTableAuthorsModelQuery()

    def on_enLettersToolbar_actionTriggered(self, action):
        self.setTableAuthorsModelQuery()

    def on_authorEdit_textChanged(self, text):
        self.setTableAuthorsModelQuery()

    def on_sequenceEdit_textChanged(self, text):
        self.setTableSequencesModelQuery()

    def setTableAuthorsModelQuery(self):
        if not self.authorEdit.text().isEmpty():
            self.authorsModel.setWhereClause("lastname LIKE ?")
            self.authorsModel.addBindValue(self.authorEdit.text() + "%")
        else:
            checkedLetter = self.lettersGroup.checkedAction()
            if checkedLetter and checkedLetter.text() != '*':
                self.authorsModel.setWhereClause("lastname LIKE ?")
                self.authorsModel.addBindValue(checkedLetter.text() + "%")
            else:
                self.authorsModel.setWhereClause(None)
        self.authorsModel.select()

    def setTableSequencesModelQuery(self):
        if self.sequenceEdit.text().isEmpty():
            self.sequencesModel.setWhereClause(None)
        else:
            self.sequencesModel.setWhereClause("seqname LIKE ?")
            self.sequencesModel.addBindValue(self.sequenceEdit.text() + "%")
        self.sequencesModel.select()

    def on_authorsView_rowSelected(self, index):
        authorid = self.authorsModel.record(index.row()).value(0).toInt()[0]
        text = self.authorsModel.record(index.row()).value(2).toString().append(" ") + \
               self.authorsModel.record(index.row()).value(1).toString()
        self.authorTitleLabel.setText(text)
        self.booksByAuthorModel.addBindValue(authorid)
        self.booksByAuthorModel.select()

    def on_sequencesView_rowSelected(self, index):
        seqid = self.sequencesModel.record(index.row()).value(0).toInt()[0]
        text = self.sequencesModel.record(index.row()).value(1).toString()
        self.seqTitleLabel.setText(text)
        self.booksBySeqModel.addBindValue(seqid)
        self.booksBySeqModel.select()

    def on_genresTree_rowSelected(self, index):
        genredesc = self.genresTree.model().data(index)
        newidx = self.genresTree.model().index(index.row(), 1, index.parent())
        genreid = self.genresTree.model().data(newidx)
        self.genreTitleLabel.setText(genredesc)
        self.booksByGenreModel.addBindValue(genreid)
        self.booksByGenreModel.select()

    def on_groupsView_rowSelected(self, index):
        groupid = self.groupsModel.record(index.row()).value(0).toInt()[0]
        text = self.groupsModel.record(index.row()).value(1).toString()
        self.groupTitleLabel.setText(text)
        self.booksByGroupModel.addBindValue(groupid)
        self.booksByGroupModel.select()

    def appendToTitle(self, str):
        self.setWindowTitle(self.appTitle + " - " + str)

    def closeEvent(self, event):
        self.parserThread.quit()
        if self.programSettings.getSaveUiOnExitOption():
            self.writeStateTo(self.uiSettingsFile)
        event.accept()

    @QtCore.pyqtSlot()
    def on_actionDbProperties_triggered(self):
        dialog = DbPropertiesDialog(self)
        dialog.filenameEdit.setText(dbName())
        dialog.nameEdit.setFocus()
        if dialog.exec_():
            self.appendToTitle(getDbProperty('name').toString())

    @QtCore.pyqtSlot()
    def on_actionDbScanBookDir_triggered(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(self,
                                            self.tr("Select directory"),
                                            QtCore.QDir.homePath(),
                                            QtGui.QFileDialog.ShowDirsOnly)
        if not dirname.isEmpty():
            if self.programSettings.getSaveUiOnExitOption():
                self.writeStateTo(self.uiSettingsFile)
            os.execvp('python', ('python', 'importdialog.py',
                                 dbName(),
                                 QtCore.QDir(dirname).absolutePath(),
                                 '--execvp'))


    def bookParsed(self, reader):
        if reader.hasError():
            self.coverpageLabel.setText(self.tr("Parser error"))
            self.annotationEdit.setText("")
        else:
            self.annotationEdit.setText(reader.info.Annotation)
            if reader.info.Coverpage.isEmpty():
                self.coverpageLabel.setText(self.tr("No coverpage"))
            else:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(reader.info.Coverpage)
                if pixmap.width() <= 200:
                    self.coverpageLabel.setPixmap(pixmap)
                else:
                    self.coverpageLabel.setPixmap(pixmap.scaledToWidth(200))

    def on_booksByAuthorView_rowSelected(self, index):
        if self.dockWidget.isVisible():
            bookid = self.booksByAuthorModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksBySeqView_rowSelected(self, index):
        if self.dockWidget.isVisible():
            bookid = self.booksBySeqModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_bookSearchView_rowSelected(self, index):
        if self.dockWidget.isVisible():
            bookid = self.bookSearchModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByGenreView_rowSelected(self, index):
        if self.dockWidget.isVisible():
            bookid = self.booksByGenreModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByGroupView_rowSelected(self, index):
        if self.dockWidget.isVisible():
            bookid = self.booksByGroupModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByAuthorView_doubleClicked(self, index):
        bookid = self.booksByAuthorModel.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def on_booksBySeqView_doubleClicked(self, index):
        bookid = self.booksBySeqModel.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def on_booksByGenreView_doubleClicked(self, index):
        bookid = self.booksByGenreModel.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def on_bookSearchView_doubleClicked(self, index):
        bookid = self.bookSearchModel.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def on_booksByGroupView_doubleClicked(self, index):
        bookid = self.booksByGroupModel.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def startDefaultProgramUsingBookId(self, bookid):
        filename = filenameByBookId(bookid)
        if filename:
            programs = self.programSettings.getPrograms()
            if programs:
                args = programs[0][1].split(" ")
                if args.count():
                    program = args.takeFirst()
                    args.replaceInStrings('%p', filename)
                    self.startProgramDetached(program, args)

    def startProgramDetached(self, program, args):
        if not QtCore.QProcess.startDetached(program, args):
            QtGui.QMessageBox.critical(self, self.tr("Error"),
                    QtCore.QString(self.tr("Unable to start program: %1"))
                    .arg(program))

    @QtCore.pyqtSlot()
    def on_actionConfigure_triggered(self):
        dialog = SettingsDialog(self.programSettings, self)
        dialog.exec_()

    def makePopupMenu(self, bookid):
        menu = QtGui.QMenu()
        if bookid:
            filename = filenameByBookId(bookid)
            group = QtGui.QActionGroup(menu)
            group.triggered.connect(self.on_group1_triggered)
            for program in self.programSettings.getPrograms():
                if not program[1].isEmpty():
                    if program[0].isEmpty():
                        a = menu.addAction(program[1])
                    else:
                        a = menu.addAction(program[0])
                    args = program[1].split(" ")
                    program = args.takeFirst()
                    args.replaceInStrings('%p', filename)
                    a.program = program
                    a.args = args
                    group.addAction(a)
            groups = getGroupsBookNotIn(bookid)
            if groups:
                if not menu.isEmpty():
                    menu.addSeparator()
                menu2 = QtGui.QMenu(self.tr("Add to group"), menu)
                group2 = QtGui.QActionGroup(menu2)
                group2.triggered.connect(self.on_group2_triggered)
                for group in groups:
                    a = menu2.addAction(group[1])
                    a.bookid = bookid
                    a.groupid = group[0]
                    group2.addAction(a)
                menu.addMenu(menu2)
            groups = getGroupsBookIn(bookid)
            if groups:
                if not menu.isEmpty():
                    menu.addSeparator()
                menu3 = QtGui.QMenu(self.tr("Remove from group"), menu)
                group3 = QtGui.QActionGroup(menu3)
                group3.triggered.connect(self.on_group3_triggered)
                for group in groups:
                    a = menu3.addAction(group[1])
                    a.bookid = bookid
                    a.groupid = group[0]
                    group3.addAction(a)
                menu.addMenu(menu3)
        return menu

    def on_group1_triggered(self, action):
        self.startProgramDetached(action.program, action.args)

    def on_group2_triggered(self, action):
        self.fetchAll()
        addBookToGroup(action.bookid, action.groupid)
        self.booksByGroupModel.refresh()

    def on_group3_triggered(self, action):
        self.fetchAll()
        removeBookFromGroup(action.bookid, action.groupid)
        for index in self.booksByGroupView.selectionModel().selectedRows():
            self.booksByGroupView.setRowHidden(index.row(), True)

    def on_booksByAuthorView_rightButtonPressed(self, index):
        if index.isValid():
            bookid = self.booksByAuthorModel.record(index.row()).value(0).toInt()[0]
        else:
            bookid = None
        self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_booksBySeqView_rightButtonPressed(self, index):
        if index.isValid():
            bookid = self.booksBySeqModel.record(index.row()).value(0).toInt()[0]
        else:
            bookid = None
        self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_booksByGenreView_rightButtonPressed(self, index):
        if index.isValid():
            bookid = self.booksByGenreModel.record(index.row()).value(0).toInt()[0]
        else:
            bookid = None
        self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_bookSearchView_rightButtonPressed(self, index):
        if index.isValid():
            bookid = self.bookSearchModel.record(index.row()).value(0).toInt()[0]
        else:
            bookid = None
        self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_booksByGroupView_rightButtonPressed(self, index):
        if index.isValid():
            bookid = self.booksByGroupModel.record(index.row()).value(0).toInt()[0]
        else:
            bookid = None
        self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_authorsView_rightButtonPressed(self, index):
        if index.isValid():
            authorid = self.authorsModel.record(index.row()).value(0).toInt()[0]
            menu = QtGui.QMenu()
            g = QtGui.QActionGroup(menu)
            g.triggered.connect(self.on_remove_author_action_triggered)
            a = menu.addAction(self.tr("Remove author"))
            a.authorid = authorid
            g.addAction(a)
            menu.exec_(QtGui.QCursor.pos())

    def on_sequencesView_rightButtonPressed(self, index):
        if index.isValid():
            seqid = self.sequencesModel.record(index.row()).value(0).toInt()[0]
            menu = QtGui.QMenu()
            g = QtGui.QActionGroup(menu)
            g.triggered.connect(self.on_remove_sequence_action_triggered)
            a = menu.addAction(self.tr("Remove sequence"))
            a.seqid = seqid
            g.addAction(a)
            menu.exec_(QtGui.QCursor.pos())

    def on_groupsView_rightButtonPressed(self, index):
        if index.isValid():
            groupid = self.groupsModel.record(index.row()).value(0).toInt()[0]
            menu = QtGui.QMenu()
            g = QtGui.QActionGroup(menu)
            g.triggered.connect(self.on_remove_group_action_triggered)
            a = menu.addAction(self.tr("Remove group"))
            a.groupid = groupid
            g.addAction(a)
            menu.exec_(QtGui.QCursor.pos())

    def on_remove_author_action_triggered(self, action):
        self.fetchAll()
        removeAuthor(action.authorid)
        for index in self.authorsView.selectionModel().selectedRows():
            self.authorsView.setRowHidden(index.row(), True)

    def on_remove_sequence_action_triggered(self, action):
        self.fetchAll()
        removeSequence(action.seqid)
        for index in self.sequencesView.selectionModel().selectedRows():
            self.sequencesView.setRowHidden(index.row(), True)

    def on_remove_group_action_triggered(self, action):
        self.fetchAll()
        removeGroup(action.groupid)
        for index in self.groupsView.selectionModel().selectedRows():
            self.groupsView.setRowHidden(index.row(), True)

    @QtCore.pyqtSlot()
    def on_actionAboutQt_triggered(self):
        QtGui.QMessageBox.aboutQt(self, self.tr("About Qt"))

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        msgbox = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon,
                                   self.tr("About PyHomeLib"),
                                   QtCore.QString(self.tr("<b>Homepage</b>: %1"))
                                   .arg("<a href='http://github.com/md2/pyhomelib'>http://github.com/md2/pyhomelib</a>"),
                                   QtGui.QMessageBox.Ok,
                                   self)
        msgbox.exec_()

    def on_groupEdit_returnPressed(self):
        self.fetchAll()
        addGroup(self.groupEdit.text())
        self.groupsModel.refresh()
        self.groupEdit.clear()

    def on_searchByAuthorEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchByTitleEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchBySeqEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchByGenreEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchByFileAuthorEdit_returnPressed(self):
        self.setSearchModelQuery()

    def setSearchModelQuery(self):
        author = self.searchByAuthorEdit.text().trimmed()
        title = self.searchByTitleEdit.text().trimmed()
        seq = self.searchBySeqEdit.text().trimmed()
        genre = self.searchByGenreEdit.text().trimmed()
        fileauthor = self.searchByFileAuthorEdit.text().trimmed()
        l = QtCore.QStringList()
        if not author.isEmpty():
            l.append("lastname LIKE ?")
            self.bookSearchModel.addBindValue(author.append('%'))
        if not title.isEmpty():
            l.append("title LIKE ?")
            self.bookSearchModel.addBindValue(title.append('%'))
        if not seq.isEmpty():
            l.append("seqname LIKE ?")
            self.bookSearchModel.addBindValue(seq.append('%'))
        if not genre.isEmpty():
            char = genre[0].toAscii()
            if char >= 'a' and char <= 'z':
                l.append("genrecode LIKE ?")
            else:
                l.append("genredesc LIKE ?")
            self.bookSearchModel.addBindValue(genre.append('%'))
        if not fileauthor.isEmpty():
            l.append("fileauthor LIKE ?")
            self.bookSearchModel.addBindValue(fileauthor.append('%'))
        sql = l.join(" AND ")
        if not sql.isEmpty():
            self.bookSearchModel.setWhereClause(sql)
            self.bookSearchModel.select()

    def fetchAll(self):
        for widget in self.findChildren(QtGui.QTableView):
            while widget.model().canFetchMore():
                widget.model().fetchMore()
                QtGui.qApp.processEvents()

    def on_booksByAuthorView_clicked(self, index):
        if self.dockWidget.isVisible():
            bookid = self.booksByAuthorModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksBySeqView_clicked(self, index):
        if self.dockWidget.isVisible():
            bookid = self.booksBySeqModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_bookSearchView_clicked(self, index):
        if self.dockWidget.isVisible():
            bookid = self.bookSearchModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByGenreView_clicked(self, index):
        if self.dockWidget.isVisible():
            bookid = self.booksByGenreModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByGroupView_clicked(self, index):
        if self.dockWidget.isVisible():
            bookid = self.booksByGroupModel.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    @QtCore.pyqtSlot()
    def on_actionStatistics_triggered(self):
        dlg = StatisticsDialog(self)
        dlg.exec_()

    def on_dockWidget_visibilityChanged(self, visible):
        self.actionViewBookInfo.setChecked(self.dockWidget.isVisibleTo(self))

