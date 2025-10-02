# Makefile for Al-Kafeel Book Extractor
# Created by Eylias Sharar

.PHONY: help install install-dev test test-verbose clean lint format setup run-test run-example build upload

# Default target
help:
	@echo "🚀 Al-Kafeel Book Extractor - Make Commands"
	@echo "Created by Eylias Sharar"
	@echo ""
	@echo "Available commands:"
	@echo "  install        Install the package and dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo "  test          Run tests"
	@echo "  test-verbose  Run tests with verbose output"
	@echo "  lint          Run code linting"
	@echo "  format        Format code with black"
	@echo "  setup         Setup environment and browsers"
	@echo "  run-test      Run built-in test extraction"
	@echo "  run-example   Run example extraction"
	@echo "  clean         Clean up temporary files"
	@echo "  build         Build distribution packages"
	@echo "  upload        Upload to PyPI (requires credentials)"
	@echo ""

install:
	@echo "📦 Installing Al-Kafeel Book Extractor..."
	pip install -r requirements.txt
	playwright install chromium
	@echo "✅ Installation complete!"

install-dev:
	@echo "🛠️ Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest pytest-asyncio black flake8 mypy
	playwright install chromium
	@echo "✅ Development setup complete!"

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

test-verbose:
	@echo "🧪 Running tests with verbose output..."
	pytest tests/ -v -s --tb=long

lint:
	@echo "🔍 Running code linting..."
	flake8 src/ main.py --max-line-length=100
	mypy src/ main.py --ignore-missing-imports

format:
	@echo "🎨 Formatting code..."
	black src/ main.py tests/ --line-length=100
	@echo "✅ Code formatted!"

setup:
	@echo "🔧 Setting up environment..."
	python main.py setup
	@echo "✅ Environment setup complete!"

run-test:
	@echo "🧪 Running built-in test..."
	python main.py test

run-example:
	@echo "📚 Running example extraction..."
	python main.py extract "https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b" --verbose

clean:
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	@echo "✅ Cleanup complete!"

build: clean
	@echo "📦 Building distribution packages..."
	python setup.py sdist bdist_wheel
	@echo "✅ Build complete!"

upload: build
	@echo "🚀 Uploading to PyPI..."
	twine upload dist/*
	@echo "✅ Upload complete!"

# Development helpers
dev-install: install-dev
	@echo "🔧 Installing package in development mode..."
	pip install -e .

check: lint test
	@echo "✅ All checks passed!"

all: clean install test lint
	@echo "🎉 Complete setup and verification finished!"
