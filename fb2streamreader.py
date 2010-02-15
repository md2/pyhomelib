# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore

class FB2AuthorInfo(object):

    def __init__(self):
        super(FB2AuthorInfo, self).__init__()
        self.firstName = QtCore.QString()
        self.middleName = QtCore.QString()
        self.lastName = QtCore.QString()
        self.nickName = QtCore.QString()

    def empty(self):
        return self.firstName.isEmpty() and self.middleName.isEmpty() and \
               self.lastName.isEmpty() and self.nickName.isEmpty()

    def makeName(self):
        if not self.nickName.isEmpty() and self.firstName.isEmpty() and \
                                           self.lastName.isEmpty():
            return self.nickName
        l = QtCore.QStringList()
        for s in (self.firstName, self.middleName, self.lastName):
            if not s.isEmpty():
                l.append(s)
        if not self.nickName.isEmpty():
            l.append(QtCore.QString("(%1)").arg(self.nickName))
        return l.join(" ")


class FB2SequenceInfo(object):

    def __init__(self):
        super(FB2SequenceInfo, self).__init__()
        self.sequenceName = QtCore.QString()
        self.sequenceNumber = 0

    def empty(self):
        return self.sequenceName.isEmpty()


class FB2Info(object):

    def __init__(self):
        super(FB2Info, self).__init__()
        self.Year = None
        self.Genres = QtCore.QStringList()
        self.Authors = []
        self.Translators = []
        self.documentAuthors = []
        self.Sequences = []
        self.publisherSequences = []
        self.Coverpage = QtCore.QByteArray()

    def __getattr__(self, attr):
        return ""

    def addGenre(self, genre):
        self.Genres.append(genre)

    def addAuthor(self, author):
        self.Authors.append(author)

    def addTranslator(self, translator):
        self.Translators.append(translator)

    def addDocumentAuthor(self, author):
        self.documentAuthors.append(author)

    def addSequence(self, sequence):
        self.Sequences.append(sequence)

    def addPublisherSequence(self, sequence):
        self.publisherSequences.append(sequence)


class FB2StreamReader(QtCore.QXmlStreamReader):

    def __init__(self):
        super(FB2StreamReader, self).__init__()
        self.info = FB2Info()
        self.binaryId = QtCore.QString()

    def read(self, filename):
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.ReadOnly):
            self.raiseError(QtCore.QString("Unable to open file '%1' for reading")
                            .arg(filename))
            return False

        self.setDevice(file)

        while not self.atEnd():
            self.readNext()
            if self.isStartElement():
                if self.name() == 'FictionBook':
                    self.readFictionBook()
                else:
                    self.raiseError("Parser error")
        return not self.hasError()

    def readUnknownElement(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                self.readUnknownElement()

    def readFictionBook(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'description':
                    self.readDescription()
                elif self.name() == 'binary':
                    self.readBinary()
                else:
                    self.readUnknownElement()

    def readDescription(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'title-info':
                    self.readTitleInfo()
                elif self.name() == 'document-info':
                    self.readDocumentInfo()
                elif self.name() == 'publish-info':
                    self.readPublishInfo()
                else:
                    self.readUnknownElement()

    def readBinary(self):
        id = self.attributes().value('id').toString()
        if not self.binaryId.isEmpty() and id == self.binaryId:
            self.info.Coverpage = QtCore.QByteArray.fromBase64(self.readElementText().toAscii())
        else:
            self.readElementText()

    def readTitleInfo(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'genre':
                    self.readGenre()
                elif self.name() == 'author':
                    self.readBookAuthor()
                elif self.name() == 'book-title':
                    self.readBookTitle()
                elif self.name() == 'annotation':
                    self.readAnnotation()
                elif self.name() == 'keywords':
                    self.readKeywords()
                elif self.name() == 'date':
                    self.readDate()
                elif self.name() == 'coverpage':
                    self.readCoverpage()
                elif self.name() == 'lang':
                    self.readLang()
                elif self.name() == 'src-lang':
                    self.readSrcLang()
                elif self.name() == 'translator':
                    self.readTranslator()
                elif self.name() == 'sequence':
                    self.readSequence()
                else:
                    self.readUnknownElement()

    def readDocumentInfo(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'author':
                    self.readDocumentAuthor()
                elif self.name() == 'program-used':
                    self.readProgramUsed()
                elif self.name() == 'date':
                    self.readDocumentDate()
                elif self.name() == 'src-url':
                    self.readSrcUrl()
                elif self.name() == 'src-ocr':
                    self.readSrcOcr()
                elif self.name() == 'id':
                    self.readBookId()
                elif self.name() == 'version':
                    self.readVersion()
                elif self.name() == 'history':
                    self.readHistory()
                else:
                    self.readUnknownElement()

    def readPublishInfo(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'book-name':
                    self.readBookName()
                elif self.name() == 'publisher':
                    self.readPublisher()
                elif self.name() == 'city':
                    self.readCity()
                elif self.name() == 'year':
                    self.readYear()
                elif self.name() == 'isbn':
                    self.readISBN()
                elif self.name() == 'sequence':
                    self.readPublisherSequence()
                else:
                    self.readUnknownElement()

    def readGenre(self):
        self.info.addGenre(self.readElementText())

    def readBookAuthor(self):
        author = FB2AuthorInfo()
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'first-name':
                    author.firstName = self.readFirstname()
                elif self.name() == 'middle-name':
                    author.middleName = self.readMiddlename()
                elif self.name() == 'last-name':
                    author.lastName = self.readLastname()
                elif self.name() == 'nickname':
                    author.nickName = self.readNickname()
                else:
                    self.readUnknownElement()
        if not author.empty():
            self.info.addAuthor(author)

    def readBookTitle(self):
        title = self.readElementText()
        if not title.isEmpty():
            self.info.bookTitle = title
        else:
            self.raiseError("Parser error")

    def readAnnotation(self):
        anno = QtCore.QString()
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'p':
                    anno.append(self.readParagraph())
                else:
                    self.readUnknownElement()
        self.info.Annotation = anno

    def readKeywords(self):
        self.info.Keywords = self.readElementText()

    def readDate(self):
        if self.attributes().hasAttribute('value'):
            date = self.attributes().value('value').toString()
            self.readElementText()
        else:
            date = self.readElementText()
        self.info.Date = date

    def readParagraph(self):
        result = QtCore.QString('<p>')
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'emphasis':
                    result.append(self.readEmphasis())
                elif self.name() == 'strong':
                    result.append(self.readStrong())
                else:
                    result.append(self.readPlainText())
            elif self.isCharacters():
                result.append(self.text().toString())
        result.append('</p>')
        return result

    def readEmphasis(self):
        result = QtCore.QString('<i>')
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'emphasis':
                    result.append(self.readEmphasis())
                elif self.name() == 'strong':
                    result.append(self.readStrong())
                else:
                    result.append(self.readPlainText())
            elif self.isCharacters():
                result.append(self.text().toString())
        result.append('</i>')
        return result

    def readStrong(self):
        result = QtCore.QString('<b>')
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'emphasis':
                    result.append(self.readEmphasis())
                elif self.name() == 'strong':
                    result.append(self.readStrong())
                else:
                    result.append(self.readPlainText())
            elif self.isCharacters():
                result.append(self.text().toString())
        result.append('</b>')
        return result

    def readPlainText(self):
        result = QtCore.QString()
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                result.append(self.readPlainText())
            elif self.isCharacters():
                result.append(self.text().toString())
        return result

    def readCoverpage(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'image':
                    self.readImage()
                else:
                    self.readUnknownElement()

    def readLang(self):
        self.info.Lang = self.readElementText()

    def readSrcLang(self):
        self.info.srcLang = self.readElementText()

    def readTranslator(self):
        translator = FB2AuthorInfo()
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'first-name':
                    translator.firstName = self.readFirstname()
                elif self.name() == 'middle-name':
                    translator.middleName = self.readMiddlename()
                elif self.name() == 'last-name':
                    translator.lastName = self.readLastname()
                elif self.name() == 'nickname':
                    translator.nickName = self.readNickname()
                else:
                    self.readUnknownElement()
        if not translator.empty():
            self.info.addTranslator(translator)

    def readSequence(self):
        seq = FB2SequenceInfo()
        if self.attributes().hasAttribute('name'):
            seq.sequenceName = self.attributes().value('name').toString()
        if self.attributes().hasAttribute('number'):
            seq.sequenceNumber = self.attributes().value('number').toString().toInt()[0]
        if not seq.empty():
            self.info.addSequence(seq)
        self.readElementText()

    def readPublisherSequence(self):
        seq = FB2SequenceInfo()
        if self.attributes().hasAttribute('name'):
            seq.sequenceName = self.attributes().value('name').toString()
        if self.attributes().hasAttribute('number'):
            seq.sequenceNumber = self.attributes().value('number').toString().toInt()[0]
        if not seq.empty():
            self.info.addPublisherSequence(seq)
        self.readElementText()

    def readDocumentAuthor(self):
        author = FB2AuthorInfo()
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'first-name':
                    author.firstName = self.readFirstname()
                elif self.name() == 'middle-name':
                    author.middleName = self.readMiddlename()
                elif self.name() == 'last-name':
                    author.lastName = self.readLastname()
                elif self.name() == 'nickname':
                    author.nickName = self.readNickname()
                else:
                    self.readUnknownElement()
        if not author.empty():
            self.info.addDocumentAuthor(author)

    def readProgramUsed(self):
        self.info.programUsed = self.readElementText()

    def readDocumentDate(self):
        if self.attributes().hasAttribute('value'):
            date = self.attributes().value('value').toString()
            self.readElementText()
        else:
            date = self.readElementText()
        self.info.documentDate = date

    def readSrcUrl(self):
        self.info.srcUrl = self.readElementText()

    def readSrcOcr(self):
        self.info.srcOcr = self.readElementText()

    def readBookId(self):
        self.info.Id = self.readElementText()

    def readVersion(self):
        self.info.Version = self.readElementText()

    def readHistory(self):
        history = QtCore.QString()
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'p':
                    history.append(self.readParagraph())
                else:
                    self.readUnknownElement()
        self.info.History = history

    def readBookName(self):
        self.info.bookName = self.readElementText()

    def readPublisher(self):
        self.info.Publisher = self.readElementText()

    def readCity(self):
        self.info.City = self.readElementText()

    def readYear(self):
        self.info.Year = self.readElementText().toInt()[0]

    def readISBN(self):
        self.info.ISBN = self.readElementText()

    def readImage(self):
        for i in xrange(self.attributes().size()):
            if self.attributes().at(i).qualifiedName().toString().endsWith(':href'):
                href = self.attributes().at(i).value().toString()
                if href.startsWith('#'):
                    self.binaryId = href.mid(1)
        self.readElementText()

    def readFirstname(self):
        return self.readElementText()

    def readMiddlename(self):
        return self.readElementText()

    def readLastname(self):
        return self.readElementText()

    def readNickname(self):
        return self.readElementText()

