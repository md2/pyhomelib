include pyhomelib.pro

all: forms translations
	chmod 755 pyhomelib.py

forms: $(foreach f,$(FORMS),ui_$(subst .ui,.py,$(f)))

translations: $(foreach t,$(TRANSLATIONS),$(subst .ts,.qm,$(t)))

%.qm: %.ts
	lrelease-qt4 $<

ui_%.py: %.ui
	pyuic4 $< > $@

clean:
	rm -f *.pyc *.qm ui_*.py

.PHONY: clean

