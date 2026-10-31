# Minimal packaging Makefile for openttd-national-anthem
# Reference layout follows OpenTTD base-music conventions.

PKG     = openttd-national-anthem
VERSION = 1.0
DIR     = $(PKG)-$(VERSION)
TAR     = $(DIR).tar
TGZ     = $(DIR).tar.gz

all: $(TGZ)

$(TGZ): $(DIR)
	tar -czf $(TGZ) -C $(DIR) .

$(TAR): $(DIR)
	tar -cf $(TAR) -C $(DIR) .

$(DIR): $(wildcard *.mid) national_anthems.obm README.md LICENSE changelog.txt
	mkdir -p $(DIR)
	cp $^ $(DIR)/

clean:
	rm -rf $(DIR) $(TAR) $(TGZ)

.PHONY: all clean
