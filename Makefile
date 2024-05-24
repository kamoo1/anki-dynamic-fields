SHELL := /bin/bash
PATH_SRC := anki_dynamic_fields
PATH_VENDORS := $(PATH_SRC)/vendors
ANKI_ADDON_PATH := $(HOME)/.local/share/Anki2/addons21/$(PATH_SRC)
TOP_DEPS := jinja2
PLATFORMS := win_amd64 manylinux2014_x86_64 macosx_10_9_x86_64
CALL_GFD := "scripts/get_full_deps.sh"
CALL_MV := "scripts/make_vendor.sh"


all:
	mkdir -p dist && \
	$(MAKE) vendors && \
	FILE=$$(poetry version | tr ' ' '_').ankiaddon && \
	cd $(PATH_SRC) && zip -r ../dist/$$FILE *


.PHONY: vendors
vendors:
	rm -rf $(PATH_VENDORS) && mkdir -p $(PATH_VENDORS) && \
	DEPS=$$($(CALL_GFD) $(TOP_DEPS)) && \
	for dep in $$DEPS; do \
		$(CALL_MV) $(PATH_VENDORS) "$$dep" $(PLATFORMS); \
	done



.PHONY: link
link:
	rm -rf $(ANKI_ADDON_PATH)
	ln -s -f $(PWD)/$(PATH_SRC) $(ANKI_ADDON_PATH)


.PHONY: test
test:
	python -m unittest discover -vfs tests/unit