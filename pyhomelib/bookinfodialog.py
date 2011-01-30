# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import sys
from PyQt4 import QtCore, QtSql, QtGui
from ui.bookinfodialog import Ui_BookInfoDialog
from fb2streamreader import FB2StreamReader
from genretreemodelreader import GenreTreeModelReader


class BookInfoDialog(QtGui.QDialog, Ui_BookInfoDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.Window)

        self.setupUi(self)

        model = GenreTreeModelReader('genres.xml')

        reader = FB2StreamReader()
        filename = QtCore.QString.fromUtf8(sys.argv[1])
        reader.read(filename)
        info = reader.info
        self.setWindowTitle(info.bookTitle + " - " + self.windowTitle())
        for i in range(min(3, len(info.Authors))):
            self.authorsLayout.addWidget(self.makeLabel(info.Authors[i].makeName()))
        if len(info.Authors) > 3:
            self.authorsLayout.addWidget(self.makeLabel(self.tr("etc.")))
        self.titleLabel.setText(info.bookTitle)
        genres = QtCore.QStringList()
        for genre in info.Genres:
            genres.append(model.genreDescByCode(genre))
        self.genresLabel.setText(genres.join(", "))
        if info.Coverpage.isEmpty() or info.Coverpage.size() <= 120:
            self.coverpageLabel.setText(self.tr("No coverpage"))
        else:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(info.Coverpage)
            if pixmap.width() > 200:
                pixmap = pixmap.scaledToWidth(200, QtCore.Qt.SmoothTransformation)
            self.coverpageLabel.setPixmap(pixmap)
            self.annotationEdit.setMaximumHeight(max(pixmap.height(), 200))
        self.annotationEdit.setText(info.Annotation)

        self.filenameLabel.setText(filename)
        self.sizeLabel.setText(QtCore.QString.number(QtCore.QFileInfo(filename).size()))
        self.md5Label.setText(QtCore.QString(self.MD5(filename)))

        layout = self.layout1
        row = 0
        layout.addWidget(self.makeTitleLabel("title-info"), row, 1, 1, 2)
        row += 1
        for genre in info.Genres:
            layout.addWidget(self.makeLabel("genre:"), row, 1)
            layout.addWidget(self.makeEdit(genre), row, 2)
            row += 1
        if info.Keywords:
            layout.addWidget(self.makeLabel("keywords:"), row, 1)
            layout.addWidget(self.makeEdit(info.Keywords), row, 2)
            row += 1
        if info.Date:
            layout.addWidget(self.makeLabel("date:"), row, 1)
            layout.addWidget(self.makeEdit(info.Date), row, 2)
            row += 1
        if info.Lang:
            layout.addWidget(self.makeLabel("lang:"), row, 1)
            layout.addWidget(self.makeEdit(info.Lang, 30), row, 2)
            row += 1
        if info.srcLang:
            layout.addWidget(self.makeLabel("src-lang:"), row, 1)
            layout.addWidget(self.makeEdit(info.srcLang, 30), row, 2)
            row += 1
        for tr in info.Translators:
            layout.addWidget(self.makeLabel("translator:"), row, 1)
            layout.addWidget(self.makeEdit(tr.makeName()), row, 2)
            row +=1
        for seq in info.Sequences:
            layout.addWidget(self.makeLabel("sequence:"), row, 1)
            layout.addWidget(self.makeEdit(seq.sequenceName + " #" +
                                           QtCore.QString.number(seq.sequenceNumber)), row, 2)

        row += 1

        layout.addWidget(self.makeTitleLabel("document-info"), row, 1, 1, 2)
        row += 1
        for author in info.documentAuthors:
            layout.addWidget(self.makeLabel("author:"), row, 1)
            layout.addWidget(self.makeEdit(author.makeName()), row, 2)
            row += 1
        if info.programUsed:
            layout.addWidget(self.makeLabel("program-used:"), row, 1)
            layout.addWidget(self.makeEdit(info.programUsed), row, 2)
            row += 1
        if info.documentDate:
            layout.addWidget(self.makeLabel("date:"), row, 1)
            layout.addWidget(self.makeEdit(info.documentDate), row, 2)
            row += 1
        if info.srcUrl:
            layout.addWidget(self.makeLabel("src-url:"), row, 1)
            layout.addWidget(self.makeEdit(info.srcUrl), row, 2)
            row += 1
        if info.srcOcr:
            layout.addWidget(self.makeLabel("src-ocr:"), row, 1)
            layout.addWidget(self.makeEdit(info.srcOcr), row, 2)
            row += 1
        if info.Id:
            layout.addWidget(self.makeLabel("id:"), row, 1)
            layout.addWidget(self.makeEdit(info.Id), row, 2)
            row += 1
        if info.Version:
            layout.addWidget(self.makeLabel("version:"), row, 1)
            layout.addWidget(self.makeEdit(info.Version, 40), row, 2)
            row += 1
        if info.History:
            layout.addWidget(self.makeLabel("history:"), row, 1)
            edit = QtGui.QTextEdit(info.History, self)
            edit.setReadOnly(True)
            edit.setFrameStyle(QtGui.QFrame.NoFrame)
            layout.addWidget(edit, row, 2)
            row += 1

        layout.addWidget(self.makeTitleLabel("publish-info"), row, 1, 1, 2)
        row += 1
        if info.bookName:
            layout.addWidget(self.makeLabel("book-name:"), row, 1)
            layout.addWidget(self.makeEdit(info.bookName), row, 2)
            row += 1
        if info.Publisher:
            layout.addWidget(self.makeLabel("publisher:"), row, 1)
            layout.addWidget(self.makeEdit(info.Publisher), row, 2)
            row += 1
        if info.City:
            layout.addWidget(self.makeLabel("city:"), row, 1)
            layout.addWidget(self.makeEdit(info.City), row, 2)
            row += 1
        if info.Year:
            layout.addWidget(self.makeLabel("year:"), row, 1)
            layout.addWidget(self.makeEdit(QtCore.QString.number(info.Year), 50), row, 2)
            row += 1
        if info.ISBN:
            layout.addWidget(self.makeLabel("isbn:"), row, 1)
            layout.addWidget(self.makeEdit(info.ISBN), row, 2)
            row += 1
        for seq in info.publisherSequences:
            layout.addWidget(self.makeLabel("sequence:"), row, 1)
            layout.addWidget(self.makeEdit(seq.sequenceName + " #" +
                                           QtCore.QString.number(seq.sequenceNumber)), row, 2)
            row += 1

        spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Expanding)
        layout.addItem(spacer, row, 0)

        self.centered = False

    def makeLabel(self, text):
        label = QtGui.QLabel(text, self)
        label.setSizePolicy(QtGui.QSizePolicy.Fixed,
                            QtGui.QSizePolicy.Fixed)
        return label

    def makeEdit(self, text, maxw=None):
        edit = QtGui.QLineEdit(text, self)
        edit.setReadOnly(True)
        edit.setFrame(False)
        edit.home(False)
        if maxw:
            edit.setMaximumWidth(maxw)
        return edit

    def makeTitleLabel(self, text):
        label = QtGui.QLabel(text, self)
        label.setSizePolicy(QtGui.QSizePolicy.Preferred,
                            QtGui.QSizePolicy.Fixed)
        label.setAlignment(QtCore.Qt.AlignHCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        label.setFont(font)
        label.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(183, 181, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(183, 181, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 145, 144))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(183, 181, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(183, 181, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        label.setPalette(palette)
        return label

    def MD5(self, filename):
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.ReadOnly):
            return "<error>"
        return QtCore.QCryptographicHash.hash(file.readAll(),
                                        QtCore.QCryptographicHash.Md5).toHex()

    def showEvent(self, event):
        if not self.centered:
            desktopGeometry = QtGui.qApp.desktop().screenGeometry()
            self.move((desktopGeometry.width() - self.width()) / 2,
                      (desktopGeometry.height() - self.height()) / 2)
            self.centered = True

def main():
    try:
        from pyhomelib.pyhomelib import init
        init()
    except ImportError:
        pass

    app = QtGui.QApplication(sys.argv)
    if len(sys.argv) < 2:
        sys.exit(-1)
    qttranslator = QtCore.QTranslator()
    if qttranslator.load("qt_" + QtCore.QLocale.system().name(),
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
        app.installTranslator(qttranslator)
    translator = QtCore.QTranslator()
    if translator.load("pyhomelib_" + QtCore.QLocale.system().name()):
        app.installTranslator(translator)

    dlg = BookInfoDialog()
    dlg.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
