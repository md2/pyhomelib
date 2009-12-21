include pyhomelib.pro

all: forms translations
	chmod 755 pyhomelib.py

forms: $(foreach f,$(FORMS),ui_$(subst .ui,.py,$(f)))

translations: $(foreach t,$(TRANSLATIONS),$(subst .ts,.qm,$(t)))

%.qm: %.ts
	lrelease-qt4 $<

ui_%.py: %.ui
	pyuic4 $< > $@

ext: sqlite3ext.so libSqliteIcu.so

libSqliteIcu.so: icu.c
	gcc -fPIC -shared icu.c `icu-config --ldflags` -o libSqliteIcu.so

sqlite3ext.so: sqlite3ext.c sqlite3extsetup.py
	python sqlite3extsetup.py build_ext -i

clean:
	rm -f *.pyc *.qm ui_*.py

.PHONY: clean

