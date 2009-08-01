
prefix=/usr/local
PREFIX=$(prefix)
SRCDIR=src
SRCS=$(SRCDIR)/minetconf.py $(SRCDIR)/minet.py $(SRCDIR)/minet-gui.py

all:

install: $(SRCS)
	# Installing MINET+GUI
	# Creating directories
	@install -v -d $(PREFIX)/share/minet/pics/
	@install -v -d $(PREFIX)/share/applications/
	@install -v -d $(PREFIX)/share/icons/hicolor/32x32/apps/
	@install -v -d $(PREFIX)/bin
	# Copying files to dest dir
	@install -v src/*.py $(PREFIX)/share/minet/
	@install -v -m 644 src/pics/* $(PREFIX)/share/minet/pics/
	@install -v -m 644 src/pics/minet.png $(PREFIX)/share/icons/hicolor/32x32/apps/
	@install -v -m 644 misc/minet.desktop $(PREFIX)/share/applications/
	# Creating links to *.py
	cd $(PREFIX)/bin; \
	pwd; \
	ln -svf ../share/minet/minetconf.py minetconf;\
	ln -svf ../share/minet/minet.py minet;\
	ln -svf ../share/minet/minet-gui.py minet-gui;

uninstall:
	# Uninstalling MINET+GUI
	@rm -vf $(PREFIX)/bin/minet*
	@rm -rvf $(PREFIX)/share/minet
	@rm -vf $(PREFIX)/share/applications/minet.desktop
	@rm -vf $(PREFIX)/share/icons/hicolor/32x32/apps/minet.png

clean:
	@rm -f *.pyc *.log
