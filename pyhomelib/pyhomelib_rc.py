# -*- coding: utf-8 -*-

# Resource object code
#
# Created: ?? ???. 30 20:18:13 2011
#      by: The Resource Compiler for PyQt (Qt v4.7.1)
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore

qt_resource_data = "\
\x00\x00\x00\xb0\
\x51\
\x4c\x61\x62\x65\x6c\x23\x61\x75\x74\x68\x6f\x72\x54\x69\x74\x6c\
\x65\x4c\x61\x62\x65\x6c\x2c\x0a\x51\x4c\x61\x62\x65\x6c\x23\x73\
\x65\x71\x54\x69\x74\x6c\x65\x4c\x61\x62\x65\x6c\x2c\x0a\x51\x4c\
\x61\x62\x65\x6c\x23\x67\x65\x6e\x72\x65\x54\x69\x74\x6c\x65\x4c\
\x61\x62\x65\x6c\x2c\x0a\x51\x4c\x61\x62\x65\x6c\x23\x72\x65\x73\
\x75\x6c\x74\x73\x54\x69\x74\x6c\x65\x4c\x61\x62\x65\x6c\x2c\x0a\
\x51\x4c\x61\x62\x65\x6c\x23\x67\x72\x6f\x75\x70\x54\x69\x74\x6c\
\x65\x4c\x61\x62\x65\x6c\x20\x7b\x0a\x09\x66\x6f\x6e\x74\x2d\x73\
\x69\x7a\x65\x3a\x20\x31\x34\x70\x74\x3b\x0a\x09\x66\x6f\x6e\x74\
\x2d\x77\x65\x69\x67\x68\x74\x3a\x20\x62\x6f\x6c\x64\x3b\x0a\x09\
\x63\x6f\x6c\x6f\x72\x3a\x20\x6e\x61\x76\x79\x3b\x0a\x7d\x0a\
"

qt_resource_name = "\
\x00\x0d\
\x0d\x0b\x8c\x63\
\x00\x70\
\x00\x79\x00\x68\x00\x6f\x00\x6d\x00\x65\x00\x6c\x00\x69\x00\x62\x00\x2e\x00\x63\x00\x73\x00\x73\
"

qt_resource_struct = "\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()