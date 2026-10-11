.PHONY: build test clean source
build:
	python3 scripts/build.py
test:
	python3 scripts/build.py --catalogs-only
	python3 -m unittest discover -s tests -v
clean:
	$(MAKE) -f debian/rules clean
source:
	dpkg-source -b .

PREFIX ?= /usr/local
DESTDIR ?=
.PHONY: install
install:
	python3 scripts/install_prefix.py --prefix "$(PREFIX)" --destdir "$(DESTDIR)"
