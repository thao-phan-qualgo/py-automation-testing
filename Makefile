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
	@echo "    make test                  - Run all tests with Behave"
	@echo "    make test-api              - Run API tests only"
	@echo "    make test-web              - Run web tests only"
	@echo "    make test-smoke            - Run smoke tests"
	@echo "    make test-regression       - Run regression tests"
	@echo "    make test-high-priority    - Run high priority tests"
	@echo "    make test-security-posture - Run security posture tests"
	@echo ""
	@echo "  Code Quality:"
	@echo "    make lint          - Run linters (check code)"
	@echo "    make format        - Format code with black"
	@echo ""
	@echo "  Reports:"
	@echo "    make test-html             - Run tests with HTML report"
	@echo "    make test-allure           - Run tests with Allure report"
	@echo "    make test-report           - Run tests with both HTML and Allure"
	@echo "    make report                - Open HTML test report"
	@echo "    make allure-report         - Generate Allure report from results"
	@echo "    make allure-serve          - Serve Allure report in browser"
	@echo "    make allure-clean          - Clean Allure results"
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
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python -m pip install -r requirements.txt; \
	else \
		echo "⚠️  No virtual environment detected."; \
		echo "Activate with: source .venv/bin/activate"; \
		echo "Or create with: make venv"; \
		exit 1; \
	fi
	@echo "✅ Dependencies installed!"

install-dev:
	@echo "Installing development dependencies..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python -m pip install -r requirements.txt; \
		python -m pip install black flake8 pylint mypy; \
	else \
		echo "⚠️  No virtual environment detected."; \
		echo "Activate with: source .venv/bin/activate"; \
		echo "Or create with: make venv"; \
		exit 1; \
	fi
	@echo "✅ Dev dependencies installed!"

# Full setup
setup:
	@echo "Setting up project..."
	@bash -c "source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
	@echo "✅ Setup complete!"
	@echo ""
	@echo "To activate virtual environment, run:"
	@echo "  source .venv/bin/activate"

# Testing - All
test:
	@echo "Running all tests with Behave..."
	behave

test-all:
	@echo "Running all tests with verbose output..."
	behave --no-capture

# Testing - With HTML Report
test-html:
	@echo "Running tests with HTML report..."
	@mkdir -p reports
	behave --format html --outfile reports/behave_report.html --format pretty
	@echo "✅ HTML report generated: reports/behave_report.html"

# Testing - With Allure Report
test-allure:
	@echo "Running tests with Allure report..."
	@mkdir -p reports/allure_results
	behave --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty
	@echo "✅ Allure results generated: reports/allure_results"
	@echo "Generate report with: make allure-report"
	@echo "Or serve directly with: make allure-serve"

# Testing - With Both Reports
test-report:
	@echo "Running tests with HTML and Allure reports..."
	@mkdir -p reports reports/allure_results
	behave --format html --outfile reports/behave_report.html \
	       --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results \
	       --format pretty
	@echo "✅ HTML report: reports/behave_report.html"
	@echo "✅ Allure results: reports/allure_results"
	@echo "Generate Allure report with: make allure-report"

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
	behave features/web/

test-web-smoke:
	@echo "Running web smoke tests..."
	behave --tags=@smoke features/web/

# Testing - By tags
test-smoke:
	@echo "Running smoke tests..."
	behave --tags=@smoke

test-regression:
	@echo "Running regression tests..."
	behave --tags=@regression

test-high-priority:
	@echo "Running high priority tests..."
	behave --tags=@High

test-security-posture:
	@echo "Running security posture tests..."
	behave --tags=@SecurityPosture

# Code Quality
lint:
	@echo "Running linters..."
	@if command -v flake8 >/dev/null 2>&1; then \
		echo "Checking with flake8..."; \
		flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true; \
	else \
		echo "⚠️  flake8 not installed. Install with: pip install flake8"; \
	fi
	@if command -v pylint >/dev/null 2>&1; then \
		echo "Checking with pylint..."; \
		pylint steps/ pages/ utils/ config/ --exit-zero 2>/dev/null || true; \
	else \
		echo "⚠️  pylint not installed. Install with: pip install pylint"; \
	fi
	@echo "✅ Linting complete!"

format:
	@echo "Formatting code with black..."
	@if command -v black >/dev/null 2>&1; then \
		black steps/ pages/ utils/ config/ --line-length 88; \
		echo "✅ Code formatted!"; \
	else \
		echo "❌ black not installed."; \
		echo "Install with: pip install black"; \
		echo "Or run: make install-dev"; \
		exit 1; \
	fi

format-check:
	@echo "Checking code format..."
	@if command -v black >/dev/null 2>&1; then \
		black steps/ pages/ utils/ config/ --check --line-length 88; \
	else \
		echo "❌ black not installed."; \
		echo "Install with: pip install black"; \
		exit 1; \
	fi

# Reports
report:
	@echo "Opening HTML report..."
	@if [ -f reports/behave_report.html ]; then \
		open reports/behave_report.html 2>/dev/null || xdg-open reports/behave_report.html 2>/dev/null || start reports/behave_report.html 2>/dev/null || echo "Please open reports/behave_report.html manually"; \
	elif [ -f reports/report.html ]; then \
		open reports/report.html 2>/dev/null || xdg-open reports/report.html 2>/dev/null || start reports/report.html 2>/dev/null || echo "Please open reports/report.html manually"; \
	else \
		echo "❌ No HTML report found. Run 'make test-html' or 'make test-report' first."; \
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
allure-report:
	@echo "Generating Allure report..."
	@if [ ! -d "reports/allure_results" ] || [ -z "$$(ls -A reports/allure_results 2>/dev/null)" ]; then \
		echo "❌ No Allure results found. Run 'make test-allure' or 'make test-report' first."; \
		exit 1; \
	fi
	@if command -v allure >/dev/null 2>&1; then \
		allure generate reports/allure_results -o reports/allure_report --clean; \
		echo "✅ Allure report generated!"; \
		echo "📊 View at: reports/allure_report/index.html"; \
		echo "Or open with: open reports/allure_report/index.html"; \
	else \
		echo "❌ Allure CLI not installed."; \
		echo "Install with: brew install allure (macOS)"; \
		echo "Or download from: https://docs.qameta.io/allure/#_installing_a_commandline"; \
		exit 1; \
	fi

allure-serve:
	@echo "Serving Allure report..."
	@if [ ! -d "reports/allure_results" ] || [ -z "$$(ls -A reports/allure_results 2>/dev/null)" ]; then \
		echo "❌ No Allure results found. Run 'make test-allure' or 'make test-report' first."; \
		exit 1; \
	fi
	@if command -v allure >/dev/null 2>&1; then \
		allure serve reports/allure_results; \
	else \
		echo "❌ Allure CLI not installed."; \
		echo "Install with: brew install allure (macOS)"; \
		echo "Or download from: https://docs.qameta.io/allure/#_installing_a_commandline"; \
		exit 1; \
	fi

allure-open:
	@echo "Opening Allure report..."
	@if [ -f "reports/allure_report/index.html" ]; then \
		open reports/allure_report/index.html 2>/dev/null || xdg-open reports/allure_report/index.html 2>/dev/null || start reports/allure_report/index.html 2>/dev/null || echo "Please open reports/allure_report/index.html manually"; \
	else \
		echo "❌ Allure report not generated. Run 'make allure-report' first."; \
	fi

allure-clean:
	@echo "Cleaning Allure results and reports..."
	rm -rf reports/allure_results reports/allure_report 2>/dev/null || true
	@echo "✅ Allure artifacts cleaned!"

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
	rm -rf reports/allure_results reports/allure_report 2>/dev/null || true
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
	@echo "  Framework: Behave + Playwright"
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
	@echo "   make test          # Run all tests with Behave"
	@echo "   make test-web      # Run web tests"
	@echo "   make test-smoke    # Run smoke tests"
	@echo ""
	@echo "4. View reports:"
	@echo "   make report        # Open HTML report"
	@echo ""
	@echo "=================================================="

