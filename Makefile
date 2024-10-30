# Define targets
.PHONY: install install-minimal test test-tgpt test-api test-utils build build-deb build-minimal-deb clean

# Define variables
PYTHON := python3
PI := $(PYTHON) -m pip
PYINSTALLER := $(PYTHON) -m PyInstaller
DEB := $(shell pwd)/assets/deb
DEBLIB := $(DEB)/usr/lib


# Default target
default: install test build

# Target to install dependencies
install: clean
	$(PI) install -U pip
	$(PI) install -r requirements.txt 
	$(PI) install -e .
	$(PI) install --upgrade g4f[all]

# Target to install minimal dependencies
install-minimal: clean
	$(PI) install -U pip
	$(PI) install -r requirements.txt
	$(PI) install -e .

# Target to run tests
test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -f -v

# Target to run tgpt providers test
test-tgpt:
	$(PYTHON) -m unittest discover -s tests -p 'test_*_tgpt.py' -f -v

# Target to run REST-api test
test-api:
	$(PYTHON) -m unittest discover -s tests -p 'test_api.py' -f -v

# Target to run pytgpt utils test
test-utils:
	$(PYTHON) -m unittest discover -s tests -p 'test_utils.py' -f -v

# Target to create an executable using PyInstaller
build: install
	$(PI) install --upgrade pyinstaller
	$(PYINSTALLER) main.py \
	--onefile \
	--exclude pandas \
	--paths $(shell pwd) \
	--distpath dist/$(shell uname) \
	--workpath build/$(shell uname) \
	--log-level INFO \
	--exclude numpy \
	--exclude matplotlib \
	--exclude PyQt5 \
	--exclude PyQt6 \
	--exclude share \
	--icon assets/logo.png \
	--noconfirm

# Target to create .deb file
build-deb: install
	$(PI) install --upgrade pyinstaller
	$(PYINSTALLER) main.py \
	--onedir \
	--exclude pandas \
	--paths $(shell pwd) \
	--distpath $(DEBLIB) \
	--workpath build/$(shell uname) \
	--log-level INFO \
	--exclude numpy \
	--exclude matplotlib \
	--exclude PyQt5 \
	--exclude PyQt6 \
	--exclude share \
	--name pytgpt \
	--contents-directory . \
	--noconfirm

	echo "Version: $(shell pytgpt --version | grep -oP 'version \K[\d.]+')" >> $(DEB)/DEBIAN/control
	echo "Version=$(shell pytgpt --version | grep -oP 'version \K[\d.]+')" >> $(DEB)/usr/share/applications/pytgpt.desktop

	echo "/usr/lib/pytgpt\n"\
	"/usr/bin/pytgpt\n"\
	"/usr/share/applications/icons/pytgpt.png\n"\
	"/usr/share/applications/pytgpt.desktop" > $(DEBLIB)/pytgpt/entries.txt

	echo "Installed-Size: $(shell du -sh -B KB $(DEB) | awk '{print $$1}')" >> $(DEB)/DEBIAN/control

	dpkg-deb --build -Zxz $(DEB) pytgpt.deb

# Target to build minimal deb
build-minimal-deb: install-minimal
	$(PI) install --upgrade pyinstaller
	$(PYINSTALLER) main.py \
	--onedir \
	--exclude pandas \
	--paths $(shell pwd) \
	--distpath $(DEBLIB) \
	--workpath build/$(shell uname) \
	--log-level INFO \
	--exclude numpy \
	--exclude matplotlib \
	--exclude PyQt5 \
	--exclude PyQt6 \
	--exclude share \
	--name pytgpt \
	--contents-directory . \
	--noconfirm

	echo "Version: $(shell pytgpt --version | grep -oP 'version \K[\d.]+')" >> $(DEB)/DEBIAN/control
	echo "Version=$(shell pytgpt --version | grep -oP 'version \K[\d.]+')" >> $(DEB)/usr/share/applications/pytgpt.desktop

	echo "/usr/lib/pytgpt\n"\
	"/usr/bin/pytgpt\n"\
	"/usr/share/applications/icons/pytgpt.png\n"\
	"/usr/share/applications/pytgpt.desktop" > $(DEBLIB)/pytgpt/entries.txt

	echo "Installed-Size: $(shell du -sh -B KB $(DEB) | awk '{print $$1}')" >> $(DEB)/DEBIAN/control

	dpkg-deb --build -Zxz $(DEB) pytgpt.deb

# Target to clean up build artifacts
clean:
	rm -rf build/ dist/ *.spec *.deb
