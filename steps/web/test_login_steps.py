import pytest
import os
from pathlib import Path
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage

# Link the feature file using absolute path
CURRENT_DIR = Path(__file__).parent
FEATURE_FILE = CURRENT_DIR / "../../features/web/login.feature"
scenarios(str(FEATURE_FILE.resolve()))


@pytest.fixture
def login_page(page, portal_base_url):
    """Fixture to provide LoginPage instance"""
    return LoginPage(page, portal_base_url)


@pytest.fixture
def test_credentials():
    """Fixture to provide test credentials from environment (must be set in .env)"""
    email = os.getenv("TEST_EMAIL")
    password = os.getenv("TEST_PASSWORD")
    mfa_code = os.getenv("TEST_MFA_CODE")
    
    if not email or not password:
        raise ValueError(
            "TEST_EMAIL and TEST_PASSWORD must be set in .env file. "
            "Never hardcode credentials in source code!"
        )
    
    return {
        "email": email,
        "password": password,
        "mfa_code": mfa_code
    }


# ============================================================================
# GIVEN STEPS - Setup/Preconditions
# ============================================================================

@given("I am on the sign-in page")
def navigate_to_sign_in_page(login_page):
    """Navigate to sign-in page with automatic wait"""
    login_page.goto_sign_in()


# ============================================================================
# WHEN STEPS - Actions
# ============================================================================

@when('I click the "Sign in with Microsoft" button')
def click_sign_in_with_microsoft(login_page):
    """Click Sign in with Microsoft button and wait for navigation"""
    login_page.click_sign_in_with_microsoft()


@when('I enter my email "thao.pt@qualgo.net"')
def enter_email(login_page, test_credentials):
    """Enter email address from credentials"""
    login_page.enter_email(test_credentials["email"])


@when('I click the "Next" button')
def click_next_button(login_page):
    """Click Next button and wait"""
    login_page.click_next()


@when("I enter my password")
def enter_password(login_page, test_credentials):
    """Enter password from test credentials"""
    login_page.enter_password(test_credentials["password"])


@when(parsers.parse('I enter incorrect password "{password}"'))
def enter_incorrect_password(login_page, password):
    """Enter incorrect password"""
    login_page.enter_password(password)


@when('I click the "Sign in" button')
def click_sign_in_button(login_page):
    """Click Sign in button and wait"""
    login_page.click_sign_in()


@when("I wait 20 seconds for manual MFA code entry")
def wait_for_manual_mfa_code_entry(login_page):
    login_page.manual_enter_mfa_code()


@when('I click the "Verify" button')
def click_verify_button(login_page):
    """Click Verify button for MFA"""
    login_page.click_verify()


@when("I choose to stay signed in")
def choose_stay_signed_in(login_page):
    """Choose to stay signed in by clicking Yes"""
    login_page.click_stay_signed_in_yes()


@when("I choose not to stay signed in")
def choose_not_stay_signed_in(login_page):
    """Choose not to stay signed in by clicking No"""
    login_page.click_stay_signed_in_no()


# ============================================================================
# THEN STEPS - Assertions/Verification
# ============================================================================

@then("I should see the Security Operations Dashboard")
def verify_dashboard_heading(login_page):
    """Verify the Security Operations Dashboard heading is visible"""
    login_page.wait_for_page_load("networkidle")
    heading_text = "Security Operations Dashboard"
    assert login_page.verify_dashboard_heading(heading_text), \
        f"Expected heading '{heading_text}' not found. Actual: {login_page.get_dashboard_heading_text()}"


@then("I should see an error message")
def verify_error_message_visible(login_page):
    """Verify error message is displayed"""
    login_page.wait_for_page_load("domcontentloaded")
    assert login_page.is_error_visible(), "Expected error message not found"


@then("I should see password error message")
def verify_password_error(login_page):
    """Verify password-specific error message"""
    login_page.wait_for_page_load("domcontentloaded")
    error = login_page.get_error_message()
    assert error is not None, "Expected password error message not found"
    assert "password" in error.lower() or "incorrect" in error.lower(), \
        f"Expected password error but got: {error}"


@then("I should be signed in successfully")
def verify_signed_in(page):
    """Verify user is signed in by checking URL or dashboard presence"""
    page.wait_for_load_state("networkidle")
    assert "sign-in" not in page.url.lower(), "Still on sign-in page"


@then(parsers.parse('I should see text "{text}"'))
def verify_text_visible(page, text):
    """Verify specific text is visible on page"""
    page.wait_for_load_state("networkidle")
    assert page.get_by_text(text).is_visible(), f"Text '{text}' not found on page"

