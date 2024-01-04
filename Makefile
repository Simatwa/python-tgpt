# Define targets
.PHONY: install test build clean

# Define variables
PYTHON := python3
PI := pip
PYINSTALLER := $(PYTHON) -m PyInstaller

# Default target
default: install test build

# Target to install dependencies
install:
	$(PI) install -r requirements.txt 
	$(PI) install .

# Target to run tests
test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -f -v

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
	--exclude PIL \
	--exclude matplotlib \
	--exclude PyQt5 \
	--exclude share \
	--icon assets/py-tgpt.png

# Target to clean up build artifacts
clean:
	rm -rf build/ dist/ main.spec
