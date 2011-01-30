from distutils.core import setup, Extension

module = Extension('sqlite3ext',
                   sources = ['sqlite3ext.c'],
                   libraries = ['sqlite3'])

setup (name = 'sqlite3ext',
       version = '1.0',
       description = 'Python wrapper for ICU sqlite extension',
       ext_modules = [module])

