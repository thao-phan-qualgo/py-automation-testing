.PHONY: help install install-dev setup test test-api test-web test-all lint format clean report venv

# Default target
help:
	@echo "=================================================="
	@echo "  Python Automation Testing - Makefile"
	@echo "=================================================="
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  Setup & Installation:"
	@echo "    make venv          - Create virtual environment"
	@echo "    make install       - Install dependencies"
	@echo "    make install-dev   - Install dev dependencies"
	@echo "    make setup         - Full setup (venv + install)"
	@echo ""
	@echo "  Testing:"
	@echo "    make test          - Run all tests"
	@echo "    make test-api      - Run API tests only"
	@echo "    make test-web      - Run web tests only"
	@echo "    make test-positive - Run positive API tests"
	@echo "    make test-negative - Run negative API tests"
	@echo "    make test-smoke    - Run smoke tests"
	@echo ""
	@echo "  Code Quality:"
	@echo "    make lint          - Run linters (check code)"
	@echo "    make format        - Format code with black"
	@echo ""
	@echo "  Reports:"
	@echo "    make report        - Open HTML test report"
	@echo "    make allure        - Generate Allure report"
	@echo "    make allure-serve  - Serve Allure report"
	@echo ""
	@echo "  Cleanup:"
	@echo "    make clean         - Remove cache and temp files"
	@echo "    make clean-all     - Remove venv and all generated files"
	@echo ""
	@echo "=================================================="

# Virtual Environment
venv:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "✅ Virtual environment created!"
	@echo "Activate with: source .venv/bin/activate"

# Installation
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install black flake8 pylint mypy
	@echo "✅ Dev dependencies installed!"

# Full setup
setup: venv
	@echo "Setting up project..."
	@bash -c "source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
	@echo "✅ Setup complete!"
	@echo ""
	@echo "To activate virtual environment, run:"
	@echo "  source .venv/bin/activate"

# Testing - All
test:
	@echo "Running all tests..."
	pytest -v --html=reports/report.html --self-contained-html

test-all:
	@echo "Running all tests with verbose output..."
	pytest -vv --html=reports/report.html --self-contained-html

# Testing - API
test-api:
	@echo "Running API tests..."
	pytest features/api/ steps/api/ -v --html=reports/api_report.html --self-contained-html

test-api-positive:
	@echo "Running positive API tests..."
	pytest features/api/ steps/api/ -m positive -v

test-api-negative:
	@echo "Running negative API tests..."
	pytest features/api/ steps/api/ -m negative -v

test-api-validation:
	@echo "Running validation API tests..."
	pytest features/api/ steps/api/ -m validation -v

# Testing - Web
test-web:
	@echo "Running web tests..."
	pytest features/web/ steps/web/ -v --html=reports/web_report.html --self-contained-html

test-web-smoke:
	@echo "Running web smoke tests..."
	pytest features/web/ steps/web/ -m smoke -v

# Testing - By marker
test-smoke:
	@echo "Running smoke tests..."
	pytest -m smoke -v

test-regression:
	@echo "Running regression tests..."
	pytest -m regression -v

test-positive:
	@echo "Running positive tests..."
	pytest -m positive -v

test-negative:
	@echo "Running negative tests..."
	pytest -m negative -v

# Code Quality
lint:
	@echo "Running linters..."
	@echo "Checking with flake8..."
	-flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "Checking with pylint..."
	-pylint steps/ pages/ utils/ config/ || true
	@echo "✅ Linting complete!"

format:
	@echo "Formatting code with black..."
	black steps/ pages/ utils/ config/ --line-length 88
	@echo "✅ Code formatted!"

format-check:
	@echo "Checking code format..."
	black steps/ pages/ utils/ config/ --check --line-length 88

# Reports
report:
	@echo "Opening HTML report..."
	@if [ -f reports/report.html ]; then \
		open reports/report.html 2>/dev/null || xdg-open reports/report.html 2>/dev/null || start reports/report.html 2>/dev/null || echo "Please open reports/report.html manually"; \
	else \
		echo "❌ No report found. Run 'make test' first."; \
	fi

report-api:
	@echo "Opening API test report..."
	@if [ -f reports/api_report.html ]; then \
		open reports/api_report.html 2>/dev/null || xdg-open reports/api_report.html 2>/dev/null || start reports/api_report.html 2>/dev/null || echo "Please open reports/api_report.html manually"; \
	else \
		echo "❌ No API report found. Run 'make test-api' first."; \
	fi

report-web:
	@echo "Opening web test report..."
	@if [ -f reports/web_report.html ]; then \
		open reports/web_report.html 2>/dev/null || xdg-open reports/web_report.html 2>/dev/null || start reports/web_report.html 2>/dev/null || echo "Please open reports/web_report.html manually"; \
	else \
		echo "❌ No web report found. Run 'make test-web' first."; \
	fi

# Allure Reports
allure:
	@echo "Generating Allure report..."
	pytest -v --alluredir=reports/allure_results
	allure generate reports/allure_results -o reports/allure_report --clean
	@echo "✅ Allure report generated!"
	@echo "View at: reports/allure_report/index.html"

allure-serve:
	@echo "Serving Allure report..."
	allure serve reports/allure_results

# Cleanup
clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache 2>/dev/null || true
	@echo "✅ Cleanup complete!"

clean-reports:
	@echo "Cleaning up reports..."
	rm -rf reports/*.html reports/screenshots/* reports/traces/* 2>/dev/null || true
	@echo "✅ Reports cleaned!"

clean-all: clean clean-reports
	@echo "Removing virtual environment..."
	rm -rf .venv 2>/dev/null || true
	rm -rf reports/allure_results reports/allure_report 2>/dev/null || true
	@echo "✅ Full cleanup complete!"

# Utility commands
check:
	@echo "Checking environment..."
	@echo "Python version:"
	@python3 --version
	@echo ""
	@echo "Virtual environment:"
	@if [ -d ".venv" ]; then \
		echo "  ✅ Virtual environment exists"; \
	else \
		echo "  ❌ Virtual environment not found. Run 'make venv'"; \
	fi
	@echo ""
	@echo "Dependencies:"
	@if command -v pytest >/dev/null 2>&1; then \
		echo "  ✅ pytest installed"; \
	else \
		echo "  ❌ pytest not found. Run 'make install'"; \
	fi

info:
	@echo "Project Information:"
	@echo "  Name: Python Automation Testing Framework"
	@echo "  Type: Web & API Testing"
	@echo "  Framework: pytest + pytest-bdd + Playwright"
	@echo ""
	@echo "Test Coverage:"
	@echo "  - Web UI tests (Playwright)"
	@echo "  - API tests (Keycloak Authentication)"
	@echo "  - BDD-style tests (Gherkin)"
	@echo ""
	@echo "Run 'make help' for available commands"

# Quick start
quick-start:
	@echo "=================================================="
	@echo "  Quick Start Guide"
	@echo "=================================================="
	@echo ""
	@echo "1. Setup environment:"
	@echo "   make setup"
	@echo ""
	@echo "2. Activate virtual environment:"
	@echo "   source .venv/bin/activate"
	@echo ""
	@echo "3. Run tests:"
	@echo "   make test-api      # Run API tests"
	@echo "   make test-web      # Run web tests"
	@echo "   make test          # Run all tests"
	@echo ""
	@echo "4. View reports:"
	@echo "   make report        # Open HTML report"
	@echo ""
	@echo "=================================================="

