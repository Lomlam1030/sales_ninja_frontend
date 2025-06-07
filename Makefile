.PHONY: run setup clean install

# Default target
all: setup run

# Run the Streamlit application
run:
	streamlit run app.py

# Setup virtual environment and install dependencies
setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Install dependencies only (if venv already exists)
install:
	pip install -r requirements.txt

# Clean up generated files and virtual environment
clean:
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Help target
help:
	@echo "Available targets:"
	@echo "  make run      - Run the Streamlit application"
	@echo "  make setup    - Create virtual environment and install dependencies"
	@echo "  make install  - Install dependencies (if venv exists)"
	@echo "  make clean    - Remove virtual environment and cache files"
	@echo "  make all      - Setup environment and run application (default)"
	@echo "  make help     - Show this help message" 