"""
Step definitions for Login/Authentication tests.
"""

import os

from behave import given, then, when

from pages.login_page import LoginPage


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_login_page(context):
	"""Get or create LoginPage instance from context."""
	if not hasattr(context, "login_page"):
		context.login_page = LoginPage(context.page, context.portal_base_url)
	return context.login_page


# ============================================================================
# GIVEN STEPS - Setup/Preconditions
# ============================================================================


@given("I am on the sign-in page")
def step_on_sign_in_page(context):
	"""Navigate to sign-in page with automatic wait"""
	login_page = LoginPage(context.page, context.portal_base_url)
	login_page.goto_sign_in()
	context.login_page = login_page


# ============================================================================
# WHEN STEPS - Actions
# ============================================================================


@when('I click the "Sign in with Microsoft" button')
def step_click_sign_in_with_microsoft(context):
	"""Click Sign in with Microsoft button and wait for navigation"""
	get_login_page(context).click_sign_in_with_microsoft()


@when('I enter my email "{email}"')
def step_enter_email(context, email):
	"""Enter email address from step or use credentials"""
	# Use environment variable or the email from step
	actual_email = os.getenv("TEST_EMAIL", email)
	get_login_page(context).enter_email(actual_email)


@when('I click the "Next" button')
def step_click_next_button(context):
	"""Click Next button and wait"""
	get_login_page(context).click_next()


@when("I enter my password")
def step_enter_password(context):
	"""Enter password from test credentials"""
	password = os.getenv("TEST_PASSWORD")
	if not password:
		raise ValueError("TEST_PASSWORD must be set in .env file")
	get_login_page(context).enter_password(password)


@when('I enter incorrect password "{password}"')
def step_enter_incorrect_password(context, password):
	"""Enter incorrect password"""
	get_login_page(context).enter_password(password)


@when('I click the "Sign in" button')
def step_click_sign_in_button(context):
	"""Click Sign in button and wait"""
	get_login_page(context).click_sign_in()


@when("I wait 10 seconds for manual MFA code entry")
def step_wait_for_manual_mfa_code_entry(context):
	"""Wait 10 seconds for user to manually enter MFA code"""
	get_login_page(context).manual_enter_mfa_code()


@when('I click the "Verify" button')
def step_click_verify_button(context):
	"""Click Verify button for MFA"""
	get_login_page(context).click_verify()


@when("I choose to stay signed in")
def step_choose_stay_signed_in(context):
	"""Choose to stay signed in by clicking Yes"""
	get_login_page(context).click_stay_signed_in_yes()


@when("I choose not to stay signed in")
def step_choose_not_stay_signed_in(context):
	"""Choose not to stay signed in by clicking No"""
	get_login_page(context).click_stay_signed_in_no()


@when('I click the "{team_name}" team button')
def step_click_team_button(context, team_name):
	"""Click the team selection button after successful login."""
	get_login_page(context).click_team_button(team_name)


@when('I select the "{team_name}" team from the dropdown')
def step_select_team_from_dropdown(context, team_name):
	"""Select a team from the team dropdown menu."""
	get_login_page(context).select_team_from_dropdown(team_name)


# ============================================================================
# THEN STEPS - Assertions/Verification
# ============================================================================


@then("I should see the Security Operations Dashboard")
def step_verify_dashboard_heading(context):
	"""Verify the Security Operations Dashboard heading is visible"""
	login_page = get_login_page(context)
	login_page.wait_for_page_load("networkidle")
	heading_text = "Security Operations Dashboard"
	assert login_page.verify_dashboard_heading(heading_text), (
		f"Expected heading '{heading_text}' not found. "
		f"Actual: {login_page.get_dashboard_heading_text()}"
	)


@then("I should see an error message")
def step_verify_error_message_visible(context):
	"""Verify error message is displayed"""
	login_page = get_login_page(context)
	login_page.wait_for_page_load("domcontentloaded")
	assert login_page.is_error_visible(), "Expected error message not found"


@then("I should see password error message")
def step_verify_password_error(context):
	"""Verify password-specific error message"""
	login_page = get_login_page(context)
	login_page.wait_for_page_load("domcontentloaded")
	error = login_page.get_error_message()
	assert error is not None, "Expected password error message not found"
	assert (
			"password" in error.lower() or "incorrect" in error.lower()
	), f"Expected password error but got: {error}"


@then("I should be signed in successfully")
def step_verify_signed_in(context):
	"""Verify user is signed in by checking URL or dashboard presence"""
	context.page.wait_for_load_state("networkidle")
	assert "sign-in" not in context.page.url.lower(), "Still on sign-in page"


@then('I should see text "{text}"')
def step_verify_text_visible(context, text):
	"""Verify specific text is visible on page"""
	context.page.wait_for_load_state("networkidle")
	assert context.page.get_by_text(
		text
	).is_visible(), f"Text '{text}' not found on page"
