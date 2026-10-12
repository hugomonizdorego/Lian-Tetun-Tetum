# SPDX-License-Identifier: GPL-3.0-or-later
# GNU-style entry points. debhelper (dh_auto_build/test/install/clean) calls
# these targets, so `make install` is the single installation path.
PREFIX ?= /usr/local
DESTDIR ?=
PYTHON ?= python3
INSTALL_FLAGS ?=

.PHONY: all build check test install deb source clean distclean
all: build

build:
	$(PYTHON) scripts/build.py

check test: build
	$(PYTHON) -B -m unittest discover -s tests -v

install:
	$(PYTHON) -B scripts/install_prefix.py --prefix "$(PREFIX)" --destdir "$(DESTDIR)" $(INSTALL_FLAGS)

# Unsigned local Debian build (binary + source); output goes to the parent directory.
deb:
	dpkg-buildpackage -us -uc -b

source:
	dpkg-source -b .

clean:
	rm -rf build dist data/resources.html
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

distclean: clean
