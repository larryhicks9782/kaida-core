.PHONY: install clean run help

all: install

install:
	@echo "Installing Titan System..."
	pip install -e .

clean:
	@echo "Cleaning Python cache..."
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf *.egg-info

run:
	@echo "Initializing Titan Brain..."
	python3 titan_brain.py

help:
	@echo "Titan System Control:"
	@echo "  make install  - Install project"
	@echo "  make run      - Launch core"
	@echo "  make clean    - Wipe cache"
