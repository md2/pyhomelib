# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import sys
from PyQt4 import QtCore, QtSql, QtGui
from ui_bookinfodialog import Ui_BookInfoDialog
from fb2streamreader import FB2StreamReader
from genretreemodelreader import GenreTreeModelReader


class BookInfoDialog(QtGui.QDialog, Ui_BookInfoDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        model = GenreTreeModelReader('genres.xml')

        reader = FB2StreamReader()
        filename = QtCore.QString.fromUtf8(sys.argv[1])
        reader.read(filename)
        info = reader.info
        self.setWindowTitle(info.bookTitle + " - " + self.windowTitle())
        for i in xrange(min(3, len(info.Authors))):
            self.authorsLayout.addWidget(self.makeLabel(info.Authors[i].makeName()))
        if len(info.Authors) > 3:
            self.authorsLayout.addWidget(self.makeLabel(self.tr("etc.")))
        self.titleLabel.setText(info.bookTitle)
        genres = QtCore.QStringList()
        for genre in info.Genres:
            genres.append(model.genreDescByCode(genre))
        self.genresLabel.setText(genres.join(", "))
        if info.Coverpage.isEmpty():
            self.coverpageLabel.setText(self.tr("No coverpage"))
        else:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(info.Coverpage)
            if pixmap.width() > 200:
                pixmap = pixmap.scaledToWidth(200)
            self.coverpageLabel.setPixmap(pixmap)
            self.annotationEdit.setMaximumHeight(max(pixmap.height(), 200))
        self.annotationEdit.setText(info.Annotation)

        self.fileinfoLayout.addWidget(self.makeLabel(self.tr("<b>Filename:</b>") +
            " " + filename))
        self.fileinfoLayout.addWidget(self.makeLabel(self.tr("<b>Size:</b>") +
            " " + QtCore.QString.number(QtCore.QFileInfo(filename).size())))
        self.fileinfoLayout.addWidget(self.makeLabel(self.tr("<b>MD5:</b>") +
            " " + QtCore.QString(self.MD5(filename))))

        row = 0
        self.layout1.addWidget(self.makeLabel("<b style='color:red'>&lt;title-info&gt;</b>"), row, 0)
        row += 1
        for genre in info.Genres:
            self.layout1.addWidget(self.makeLabel("<b>genre:</b>"), row, 0)
            self.layout1.addWidget(self.makeLabel(genre), row, 1)
            row += 1
        self.layout1.addWidget(self.makeLabel("<b>keywords:</b>"), row, 0)
        self.layout1.addWidget(self.makeLabel(info.Keywords), row, 1)
        row += 1
        self.layout1.addWidget(self.makeLabel("<b>date:</b>"), row, 0)
        self.layout1.addWidget(self.makeLabel(info.Date), row, 1)
        row += 1
        self.layout1.addWidget(self.makeLabel("<b>lang:</b>"), row, 0)
        self.layout1.addWidget(self.makeLabel(info.Lang), row, 1)
        row += 1
        self.layout1.addWidget(self.makeLabel("<b>src-lang:</b>"), row, 0)
        self.layout1.addWidget(self.makeLabel(info.srcLang), row, 1)
        row += 1
        for tr in info.Translators:
            self.layout1.addWidget(self.makeLabel("<b>translator:</b>"), row, 0)
            self.layout1.addWidget(self.makeLabel(tr.makeName()), row, 1)
            row +=1
        for seq in info.Sequences:
            self.layout1.addWidget(self.makeLabel("<b>sequence:</b>"), row, 0)
            self.layout1.addWidget(self.makeLabel(seq.sequenceName + ", <b>number:</b> " +
                                           QtCore.QString.number(seq.sequenceNumber)), row, 1)
            row += 1
        spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Expanding)
        self.layout1.addItem(spacer, row, 0)


        row = 0
        self.layout2.addWidget(self.makeLabel("<b style='color:red'>&lt;document-info&gt;</b>"), row, 0)
        row += 1
        for author in info.documentAuthors:
            self.layout2.addWidget(self.makeLabel("<b>author:</b>"), row, 0)
            self.layout2.addWidget(self.makeLabel(author.makeName()), row, 1)
            row += 1
        self.layout2.addWidget(self.makeLabel("<b>program-used:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.programUsed), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>date:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.documentDate), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>src-url:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.srcUrl), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>src-ocr:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.srcOcr), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>id:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.Id), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>version:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.Version), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b style='color:red'>&lt;publish-info&gt;</b>"), row, 0)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>book-name:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.bookName), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>publisher:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.Publisher), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>city:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.City), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>year:</b>"), row, 0)
        if info.Year:
            self.layout2.addWidget(self.makeLabel(QtCore.QString.number(info.Year)), row, 1)
        row += 1
        self.layout2.addWidget(self.makeLabel("<b>isbn:</b>"), row, 0)
        self.layout2.addWidget(self.makeLabel(info.ISBN), row, 1)
        row += 1
        for seq in info.publisherSequences:
            self.layout2.addWidget(self.makeLabel("<b>sequence:</b>"), row, 0)
            self.layout2.addWidget(self.makeLabel(seq.sequenceName + ", <b>number:</b> " +
                                           QtCore.QString.number(seq.sequenceNumber)), row, 1)
            row += 1
        spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Expanding)
        self.layout2.addItem(spacer, row, 0)

        self.centered = False

    def makeLabel(self, text):
        label = QtGui.QLabel(text, self)
        label.setSizePolicy(QtGui.QSizePolicy.Fixed,
                            QtGui.QSizePolicy.Fixed)
        label.setTextInteractionFlags(label.textInteractionFlags() |
                                      QtCore.Qt.TextSelectableByMouse)
        return label

    def MD5(self, filename):
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.ReadOnly):
            return ""
        return QtCore.QCryptographicHash.hash(file.readAll(),
                                        QtCore.QCryptographicHash.Md5).toHex()

    def showEvent(self, event):
        if not self.centered:
            desktopGeometry = QtGui.qApp.desktop().screenGeometry()
            self.move((desktopGeometry.width() - self.width()) / 2,
                      (desktopGeometry.height() - self.height()) / 2)
            self.centered = True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(-1)
    app = QtGui.QApplication(sys.argv)
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

