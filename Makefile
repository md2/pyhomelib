include pyhomelib.pro

yo = 0

all: forms translations resources
	chmod 755 pyhomelib.py

forms: $(foreach f,$(FORMS),ui_$(subst .ui,.py,$(f)))

translations: $(foreach t,$(TRANSLATIONS),$(subst .ts,.qm,$(t)))

resources: pyhomelib_rc.py
pyhomelib_rc.py: pyhomelib.qrc
	pyrcc4 $< > $@

%.qm: %.ts
	lrelease-qt4 $<

ui_%.py: %.ui
	pyuic4 $< > $@

ext: sqlite3ext.so libSqliteIcu.so

libSqliteIcu.so: icu.c
	gcc -fPIC -shared icu.c `icu-config --ldflags` -DASSUME_YO_EQ_E=$(yo) -o libSqliteIcu.so

sqlite3ext.so: sqlite3ext.c sqlite3extsetup.py
	python sqlite3extsetup.py build_ext -i

clean:
	rm -f *.pyc *.qm ui_*.py

.PHONY: clean

