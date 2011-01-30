import subprocess

import os

from setuptools import setup, find_packages
from PyQt4.uic import compileUiDir

prefix = os.path.join( os.sys.prefix, "share" )
name= "pyhomelib"
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

def needsupdate(src, targ):
    return not os.path.exists(targ) or os.path.getmtime(src) > os.path.getmtime(targ)

def compile_qrc(qrc_file, py_file):
        if not needsupdate(qrc_file, py_file):
            return
        print("compiling %s -> %s" % (qrc_file, py_file))
        try:
            rccprocess = subprocess.Popen(['pyrcc4', qrc_file, '-o', py_file])
            rccprocess.wait()
        except Exception, e:
            raise distutils.errors.DistutilsExecError, 'Unable to compile resouce file %s' % str(e)
            return

data_files = []
for dp, dn, fs in os.walk( os.path.join( name, "icons")):
    temp=[]
    for f in fs:
        if f.endswith('.png'):
            temp.append( os.path.join( dp,f ) )
    data_files.append( ( os.path.join( prefix, dp), temp, ) )

'''
data_files.append(
        ( "/usr/share/applications/",
          [os.path.join( name, "pyhomelib.desktop") ] ) )
'''

compileUiDir(os.path.join(name,'ui'))
compile_qrc(os.path.join( name, 'resources','pyhomelib.qrc'), os.path.join(name, 'pyhomelib_rc.py'))

p = subprocess.Popen(['lrelease', os.path.join(name, 'locals', 'pyhomelib_ru.ts')])
p.wait()

setup(name='pyhomelib',
    #version = VERSION,
      description='fb2 collection manager',
      author='md2',
      author_email='md2@gmail.com',#TODO
      url='https://github.com/md2/pyhomelib',
      download_url = 'https://github.com/md2/pyhomelib',
      license='GPLv3',
      packages=find_packages(exclude=('pyhomelib')),
      data_files=data_files,
            entry_points = {
       'console_scripts':[
            'pyhomelib = pyhomelib.pyhomelib:main',
            'bookinfodialog = pyhomelib.bookinfodialog:main'
            'validator = pyhomelib.validator:main'
        ]
      }
     )
