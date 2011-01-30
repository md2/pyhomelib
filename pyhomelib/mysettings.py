# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt4 import QtCore


KEY_PROGRAMS = 'programs'
KEY_SAVE_UI_ON_EXIT = 'other/save_ui_on_exit'
KEY_ROW_HEIGHT = 'other/row_height'


class MySettings(QtCore.QSettings):

    def __init__(self, filename, parent=None):
        exists = QtCore.QFileInfo(filename).exists()
        super(MySettings, self).__init__(filename, QtCore.QSettings.IniFormat,
                                         parent)

        self.defaults_programs = [
            ('FBReader', 'FBReader %p'),
            ('Okular', 'okular %p'),
            (self.tr('Book info'), 'bookinfodialog %p'),
            (self.tr('Validation'), 'validator --nonet --noout %p')]

        if not exists:
            self.writeDefaultSettings()

    def writeDefaultSettings(self):
        self.writePrograms(self.defaults_programs)
        self.writeSaveUiOnExitOption(True)
        self.sync()

    def getBool(self, key, default=None):
        if self.contains(key):
            value = self.value(key).toString()
            if value == '1':
                return True
            elif value == '0':
                return False
        return default

    def writeBool(self, key, value):
        if value:
            self.setValue(key, 1)
        else:
            self.setValue(key, 0)

    def getPrograms(self):
        programs = []
        size = self.beginReadArray(KEY_PROGRAMS)
        for i in range(min(size, 9)):
            self.setArrayIndex(i)
            programs.append((self.value('title').toString(),
                             self.value('cmd').toString()))
        self.endArray()
        return programs

    def writePrograms(self, programs):
        self.beginWriteArray(KEY_PROGRAMS)
        for index, program in enumerate(programs):
            self.setArrayIndex(index)
            self.setValue('title', program[0])
            self.setValue('cmd', program[1])
        self.endArray()

    def getSaveUiOnExitOption(self):
        return self.getBool(KEY_SAVE_UI_ON_EXIT)

    def writeSaveUiOnExitOption(self, value):
        self.writeBool(KEY_SAVE_UI_ON_EXIT, value)

    def getRowHeight(self):
        return self.value(KEY_ROW_HEIGHT).toInt()[0]

    def writeRowHeight(self, value):
        self.setValue(KEY_ROW_HEIGHT, QtCore.QString.number(value))

