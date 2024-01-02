# Define targets
.PHONY: install test build clean

# Define variables
PYTHON := python3
PI := pip
PYINSTALLER := pyinstaller

# Default target
default: install test build

# Target to install dependencies
install:
	$(PI) install -r requirements.txt

# Target to run tests
test:
	$(PYTEST) tests/

# Target to create an executable using PyInstaller
build:
	$(PYINSTALLER) your_script.py --onefile

# Target to clean up build artifacts
clean:
	rm -rf build/ dist/ your_script.spec
