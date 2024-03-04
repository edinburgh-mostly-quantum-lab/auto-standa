INSTALL_DIR := $(HOME)/.local/auto-standa
BIN_DIR := $(HOME)/.local/bin

install:
	install -D src/* -t $(INSTALL_DIR)
	python3 -m venv $(INSTALL_DIR)/.venv
	$(INSTALL_DIR)/.venv/bin/python -m pip install libximc

	install -D bin/* -t $(BIN_DIR)

uninstall:
	rm -rfv $(INSTALL_DIR)
	rm -rfv $(BIN_DIR)/auto-standa

.PHONY: install uninstall