# Python Automation Testing Framework

## Overview

A comprehensive test automation framework using **Playwright** with **Behave** for BDD-style testing with rich HTML and Allure reporting capabilities.

## Features

✅ **Page Object Model (POM)** - Clean, maintainable test architecture  
✅ **Automatic Wait Handling** - Built-in waits for reliable tests  
✅ **BDD Support** - Write tests in Gherkin (Given/When/Then)  
✅ **Traditional pytest** - Also supports standard pytest tests  
✅ **API Testing** - Comprehensive REST API testing with JWT validation  
✅ **Multi-Browser** - Chromium, Firefox, WebKit  
✅ **Multi-Platform** - Windows, macOS, Linux  
✅ **Parallel Execution** - Run tests concurrently  
✅ **Rich Reporting** - HTML, Allure reports with screenshots  
✅ **Microsoft SSO Support** - Automated login with MFA handling

## Project Structure

```
py-automation-testing/
├── features/               # BDD feature files (Gherkin)
│   ├── api/               # API test scenarios
│   │   └── test.feature
│   └── web/               # Web UI test scenarios
│       ├── home_page.feature
│       └── login.feature
├── steps/                 # BDD step definitions
│   ├── api/               # API step definitions
│   │   └── test_keycloak_steps.py
│   └── web/               # Web step definitions
│       ├── test_home_page_steps.py
│       └── test_login_steps.py
├── pages/                 # Page Object Model
│   ├── base_page.py      # Base class with automatic waits
│   ├── home_page.py      # Home page object
│   └── login_page.py     # Login page object
├── tests/                 # Traditional pytest tests
│   └── web/
│       ├── test_sample_homepage.py
│       └── test_login.py
├── config/                # Configuration
│   └── settings.py       # Unified configuration (web + API)
├── utils/                 # Utility functions
│   └── api_helper.py     # API testing utilities
├── examples/              # Example scripts
│   └── api_usage_example.py
├── reports/              # Test reports and screenshots
│   ├── allure_results/
│   └── screenshots/
├── conftest.py           # Pytest fixtures and hooks
├── pytest.ini            # Pytest configuration
├── requirements.txt      # Python dependencies
├── run_api_tests.sh      # API test runner script
├── .env                  # Environment variables (not in git)
└── *.md                  # Documentation files
```

## Quick Start

### 1. Installation

```bash
# Clone the repository
cd py-automation-testing

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configuration

Create `.env` file in project root:

```bash
# Browser settings
BROWSER=chromium
HEADLESS=true
PORTAL_BASE_URL=https://dev-aisoc-fe.qualgo.dev

# Test credentials (optional)
TEST_EMAIL=your.email@domain.com
TEST_PASSWORD=YourPassword123
TEST_MFA_CODE=123456
```

### 3. Run Tests

```bash
# Run all tests with Behave
behave

# Run tests with HTML report
behave --format html --outfile reports/behave_report.html --format pretty

# Run tests with Allure report
behave --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# Run with specific tags
behave --tags=@smoke
behave --tags=@OV_03

# Run specific tags with Allure report
behave --tags=@smoke --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# Using Make commands (recommended)
make test           # Run all tests
make test-html      # Run with HTML report
make test-allure    # Run with Allure report
make test-report    # Run with both reports

# View generated reports
make report         # Open HTML report
make allure-serve   # Serve Allure report
```

## Testing Styles

### API Testing

**Feature File** (`features/api/test.feature`):

```gherkin
Feature: Keycloak Authentication API

  @api @authentication @positive
  Scenario: Successful authentication with valid credentials
    Given the Keycloak token endpoint is "https://nonprod-common-keycloak.qualgo.dev/..."
    And I have the following authentication credentials:
      | field         | value                  |
      | client_id     | be-admin               |
      | client_secret | your-secret            |
      | username      | user@example.com       |
      | password      | Password123@           |
      | grant_type    | password               |
    When I send a POST request to the token endpoint
    Then the response status code should be 200
    And the response should contain "access_token"
    And the access token should be a valid JWT token
```

**Run API Tests**:

```bash
# Or using pytest directly
pytest features/web/test.feature -v
```

### BDD Style (Behavior Driven Development)

**Feature File** (`features/web/login.feature`):

```gherkin
Feature: User Login

  @web @smoke
  Scenario: Successful login
    Given I am on the sign-in page
    When I click the "Sign in with Microsoft" button
    And I enter my email "user@example.com"
    And I click the "Next" button
    Then I should see the dashboard
```

**Step Definition** (`steps/web/test_login_steps.py`):

```python
@given("I am on the sign-in page")
def navigate_to_sign_in(login_page):
    login_page.goto_sign_in()

@when('I click the "Sign in with Microsoft" button')
def click_sso(login_page):
    login_page.click_sign_in_with_microsoft()
```

**Run BDD Tests**:

```bash
pytest steps/common/test_login_steps.py -v
```

### Traditional pytest Style

**Test File** (`tests/web/test_login.py`):

```python
def test_successful_login(login_page, test_credentials):
    login_page.goto_sign_in()
    login_page.complete_full_login(
        email=test_credentials["email"],
        password=test_credentials["password"],
        mfa_code=test_credentials["mfa_code"]
    )
    assert login_page.verify_dashboard_heading("Dashboard")
```

**Run pytest Tests**:

```bash
pytest tests/common/test_login.py -v
```

## Page Object Model

### BasePage - Automatic Wait Handling

All page objects inherit from `BasePage` which provides automatic wait management:

```python
from pages.base_page import BasePage

class MyPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
    
    def click_button(self):
        # Automatically waits for navigation/load
        self.click_and_wait("button#submit")
    
    def navigate_to_page(self):
        # Automatically waits for page load
        self.navigate(f"{self.base_url}/page")
```

### Available Page Objects

#### HomePage

```python
home = HomePage(page, base_url)
home.goto()              # Navigate with auto-wait
home.click_sign_in()     # Click and wait
title = home.get_title() # Get page title
```

#### LoginPage

```python
login = LoginPage(page, base_url)
login.goto_sign_in()
login.complete_full_login(email, password, mfa_code)
assert login.verify_dashboard_heading("Dashboard")
```

## Running Tests

### By Test Type

```bash
# BDD tests
pytest steps/ -v

# Traditional tests
pytest tests/ -v

# All tests
pytest -v
```

### By Marker

```bash
# Smoke tests (quick validation)
pytest -m smoke -v

# Regression tests (comprehensive)
pytest -m regression -v

# Web tests
pytest -m common -v

# Login tests
pytest -m login -v

# Combination
pytest -m "web and smoke" -v
```

### By Feature/Scenario

```bash
# Specific BDD test
pytest steps/common/test_login_steps.py -v -k "Successful login"

# Specific pytest test
pytest tests/common/test_login.py::TestLogin::test_successful_login_with_mfa -v
```

### Multi-Browser Execution

```bash
# Firefox
BROWSER=firefox pytest -m common -v

# WebKit (Safari)
BROWSER=webkit pytest -m common -v

# Chromium (default)
BROWSER=chromium pytest -m common -v
```

### Parallel Execution

Run tests in parallel using pytest-xdist:

```bash
# Run with 4 workers
pytest -m common -n 4 -v

# Run with auto-detection
pytest -m common -n auto -v
```

### Headed Mode (See Browser)

```bash
# Set in .env
HEADLESS=false

# Or via environment variable
HEADLESS=false pytest -m smoke -v
```

## Reporting

This framework supports two powerful reporting formats:

### Quick Start - Generate Reports

```bash
# Using Make commands (Recommended)
make test-html      # HTML report
make test-allure    # Allure report
make test-report    # Both reports

# Using Behave directly
behave --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty
behave --tags=@OV_03 --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# View reports
make report         # Open HTML report
make allure-serve   # Serve Allure interactively
allure serve reports/allure_results  # Serve Allure directly
```

### Using Python Test Runner

```bash
# Run with HTML report
python run_tests.py --html

# Run with Allure report
python run_tests.py --allure

# Run with both reports
python run_tests.py --both

# Run specific tags with reports
python run_tests.py --tags @smoke --html
python run_tests.py --tags @OV_03 --allure
```

### Using Behave Directly with Reports

```bash
# HTML report only
behave --format html --outfile reports/behave_report.html --format pretty

# Allure report only
behave --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# Both reports
behave --format html --outfile reports/behave_report.html \
       --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results \
       --format pretty

# With specific tags
behave --tags=@smoke --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty
behave --tags=@High --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# Exclude tags
behave --tags=~@skip --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# Multiple tags (AND)
behave --tags=@SecurityPosture --tags=@High --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty
```

### HTML Report Features

- ✅ Single, self-contained HTML file
- ✅ Easy to share via email
- ✅ No additional tools needed
- ✅ Shows pass/fail status
- ✅ Step details and timing
- ✅ Error messages and tracebacks

```bash
# Generate and open HTML report
make test-html
make report
```

### Allure Report Features

- ✅ Rich, interactive web interface
- ✅ Test history and trends
- ✅ Categories and severity
- ✅ Screenshots attached on failure
- ✅ Playwright traces attached
- ✅ Timeline visualization
- ✅ Detailed test analytics

```bash
# Generate Allure results (Make)
make test-allure

# Generate Allure results (Behave)
behave --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# Serve interactively (recommended)
make allure-serve
# or
allure serve reports/allure_results

# Or generate static report
make allure-report
make allure-open
```

### Common Test Execution Examples

```bash
# Example 1: Run specific test scenario with Allure report
behave --tags=@OV_03 --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty
allure serve reports/allure_results

# Example 2: Run smoke tests with HTML report
behave --tags=@smoke --format html --outfile reports/behave_report.html --format pretty
open reports/behave_report.html  # macOS

# Example 3: Run high priority tests with both reports
behave --tags=@High --format html --outfile reports/behave_report.html \
       --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results \
       --format pretty

# Example 4: Run Security Posture tests with Allure
behave --tags=@SecurityPosture --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# Example 5: Run all tests except skipped ones
behave --tags=~@skip --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty

# Example 6: Run specific feature file with Allure
behave features/web/overview.feature --format allure_behave.formatter:AllureFormatter --outfile reports/allure_results --format pretty
```

### Automatic Attachments on Failure

The framework automatically captures and attaches:

- 📸 **Full page screenshots** (PNG)
- 📊 **Playwright traces** (ZIP) - viewable with `playwright show-trace`
- 📝 **Page information** (URL, title, status)
- 🖥️ **Console logs** (in debug mode)

All artifacts are:

- Saved to `reports/` directory
- Attached to Allure reports automatically
- Timestamped for easy identification

### Report Locations

```
reports/
├── behave_report.html        # HTML report
├── allure_results/            # Allure raw results
├── allure_report/             # Generated Allure report
├── screenshots/               # Failure screenshots
└── traces/                    # Playwright traces
```

### View Reports

```bash
# HTML Report
make report                    # Opens HTML report in browser

# Allure Report
make allure-serve             # Serve interactively
make allure-report            # Generate static report
make allure-open              # Open generated report
```

### Clean Reports

```bash
make clean-reports            # Remove all reports
make allure-clean             # Remove Allure artifacts only
```

📚 **For detailed reporting documentation, see:** [`docs/REPORTING_GUIDE.md`](docs/REPORTING_GUIDE.md)

This includes:

- Complete usage guide
- CI/CD integration examples
- Troubleshooting tips
- Best practices

## Test Markers

Configure in `pytest.ini`:

- `@smoke` - Quick sanity tests (~5-10 min)
- `@regression` - Full test suite
- `@web` - Web UI tests
- `@api` - API tests
- `@login` - Login-specific tests
- `@authentication` - Authentication tests
- `@positive` - Positive test cases
- `@negative` - Negative test cases
- `@validation` - Validation tests

### Usage

```python
@pytest.mark.web
@pytest.mark.smoke
def test_quick_check():
    pass

@pytest.mark.web
@pytest.mark.regression
def test_detailed_check():
    pass
```

Run specific markers:

```bash
pytest -m smoke -v
```

## Environment Variables

### Required

```bash
PORTAL_BASE_URL=https://your-app-url.com
```

### Optional

```bash
BROWSER=chromium          # chromium, firefox, webkit
HEADLESS=true            # true, false
TEST_EMAIL=user@test.com
TEST_PASSWORD=password123
TEST_MFA_CODE=123456
```

## Automatic Wait Handling

### No Manual Waits Needed!

❌ **Old Way** (manual waits):

```python
page.click("button")
page.wait_for_load_state("networkidle")
page.wait_for_selector("#element")
```

✅ **New Way** (automatic):

```python
page_object.click_and_wait("button")  # Waits automatically!
```

### How It Works

1. **BasePage handles all waits**
2. **Every navigation waits for networkidle**
3. **Every click waits for load completion**
4. **Consistent across all page objects**

### Benefits

✅ Less flaky tests  
✅ Cleaner code  
✅ Consistent behavior  
✅ No forgotten waits

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Automated Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Run smoke tests
        env:
          PORTAL_BASE_URL: ${{ secrets.PORTAL_BASE_URL }}
          TEST_EMAIL: ${{ secrets.TEST_EMAIL }}
          TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
        run: pytest -m smoke -v --html=reports/report.html
      
      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: reports/
```

## Troubleshooting

### Tests Failing with "Element not found"

- Check if page loaded completely
- Verify locator is correct
- Increase timeout if needed
- Run in headed mode to debug: `HEADLESS=false`

### MFA Code Issues

- MFA codes expire quickly (30-60 seconds)
- Use test account without MFA
- Or integrate with authenticator API (pyotp)
- See `LOGIN_TEST_GUIDE.md` for details

### Permission Errors with .env

- Ensure `.env` file has read permissions
- Check file is in project root
- Verify not ignored by .gitignore

### Browser Not Found

```bash
# Reinstall browsers
playwright install chromium
```

## Documentation

### General

- **README.md** (this file) - Project overview and quick start
- **BEHAVE_COMMANDS.md** - Behave commands quick reference
- **docs/REPORTING_GUIDE.md** - Complete reporting documentation
- **docs/REPORTING_WORKFLOW.md** - Reporting workflow diagrams

### Test Execution

- **run_tests.py** - Python test runner with reporting options
- **Makefile** - Make commands for test execution and reports

### Configuration

- **behave.ini** - Behave test runner configuration
- **config/settings.py** - Environment and browser settings
- **features/environment.py** - Test hooks and setup

### Quick References

- **BEHAVE_COMMANDS.md** - All Behave commands with examples
- Common patterns and use cases
- Tag-based execution examples
- Report generation commands

## Best Practices

### 1. Use Page Objects

✅ Encapsulate page logic in page objects  
✅ Keep tests clean and readable

### 2. Use Automatic Waits

✅ Leverage BasePage methods  
✅ No manual waits in tests

### 3. Use Descriptive Names

✅ Clear test names  
✅ Meaningful assertions

### 4. Separate Concerns

✅ BDD for business-readable tests  
✅ pytest for technical tests

### 5. Use Fixtures

✅ Reusable setup/teardown  
✅ Centralized test data

## Contributing

1. Create feature branch
2. Write tests (BDD or pytest style)
3. Ensure all tests pass
4. Create pull request

## Support

For questions or issues:

1. Check documentation files
2. Review example tests
3. Check conftest.py for fixtures
4. Review page objects for available methods

## License

[Your License Here]

## Version History

- **v1.0** - Initial framework with POM and automatic waits
- **v1.1** - Added BDD support with pytest-bdd
- **v1.2** - Added login feature with Microsoft SSO
- **v1.3** - Enhanced reporting and CI/CD support
- **v1.4** - Added comprehensive API testing for Keycloak authentication
