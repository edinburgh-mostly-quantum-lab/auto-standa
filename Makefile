INSTALL_DIR := $(HOME)/.local/Faris\ Motor
BIN_DIR := $(HOME)/.local/bin
APP_DIR := $(HOME)/.local/share/applications

install:
	install -D src/* -t $(INSTALL_DIR)
	python3 -m venv $(INSTALL_DIR)/.venv
	$(INSTALL_DIR)/.venv/bin/python -m pip install ThorlabsPM100 libximc

	install -D bin/* -t $(BIN_DIR)
	install -D res/* -t $(APP_DIR)

uninstall:
	rm -rfv $(INSTALL_DIR)
	rm -rfv $(BIN_DIR)/faris-motor
	rm -rfv $(APP_DIR)/faris-motor.desktop

.PHONY: install uninstall