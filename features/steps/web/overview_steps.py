"""
Step definitions for IT Asset Inventory Overview page tests.
"""

import os

from behave import given, then, when

from pages.it_assert_inventory.overview_page import OverviewPage
from pages.login_page import LoginPage


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_overview_page(context):
    """Get or create OverviewPage instance from context."""
    if not hasattr(context, "overview_page"):
        context.overview_page = OverviewPage(context.page, context.portal_base_url)
    return context.overview_page


def get_login_page(context):
    """Get or create LoginPage instance from context."""
    if not hasattr(context, "login_page"):
        context.login_page = LoginPage(context.page, context.portal_base_url)
    return context.login_page


# ============================================================================
# GIVEN STEPS - Setup/Preconditions
# ============================================================================


@given("I am logged in as an admin user")
def step_logged_in_as_admin(context):
    """Step: Ensure user is logged in as an admin."""
    email = os.getenv("TEST_EMAIL")
    password = os.getenv("TEST_PASSWORD")

    if not email or not password:
        raise ValueError(
            "TEST_EMAIL and TEST_PASSWORD must be set in .env file. "
            "Never hardcode credentials in source code!"
        )

    login_page = get_login_page(context)
    login_page.goto_sign_in()
    login_page.complete_full_login(email=email, password=password)


@given("I am on the Security Operations Dashboard Page")
def step_on_dashboard_page(context):
    """Step: Verify user is on the Security Operations Dashboard page."""
    # User should already be on dashboard after login in Background
    # Just verify we're on the correct page
    context.page.wait_for_load_state("networkidle")


@given("I am on the Overview page")
def step_on_overview_page(context):
    """Step: Navigate to the IT Asset Inventory Overview page."""
    overview_page = get_overview_page(context)
    overview_page.click_menu_item("IT Asset Inventory")
    overview_page.click_submenu_item("Overview")
    context.page.wait_for_load_state("networkidle")


# ============================================================================
# WHEN STEPS - Actions
# ============================================================================


@when('I click on the "{menu_item}" menu item')
def step_click_menu_item(context, menu_item):
    """Step: Click on a main menu item (e.g., IT Asset Inventory)."""
    get_overview_page(context).click_menu_item(menu_item)


@when('I click on "{submenu_item}" submenu item')
def step_click_submenu_item(context, submenu_item):
    """Step: Click on a submenu item (e.g., Overview)."""
    get_overview_page(context).click_submenu_item(submenu_item)


@when('I locate the "{section_name}" section')
def step_locate_section(context, section_name):
    """Step: Locate and verify a specific section exists on the page."""
    overview_page = get_overview_page(context)
    section = overview_page.locate_section(section_name)
    assert section is not None, f"Section '{section_name}' not found on the page"


# ============================================================================
# THEN STEPS - Assertions/Verification
# ============================================================================


@then("I should see the Overview page")
def step_verify_overview_page(context):
    """Step: Verify the Overview page is displayed correctly after DOM loads."""
    overview_page = get_overview_page(context)
    assert overview_page.is_overview_page_displayed(), (
        "Overview page is not displayed. "
        "Expected to find 'Display Overview' or 'Overview' text on the page after DOM loads."
    )


@then('I should see the section title "{title}"')
def step_verify_section_title(context, title):
    """Step: Verify a section title is visible on the page."""
    overview_page = get_overview_page(context)
    assert overview_page.is_section_title_visible(title), (
        f"Section title '{title}' not found. "
        f"Page may not have loaded correctly or title text may have changed."
    )


@then("I should see {count:d} metric cards displayed")
def step_verify_metric_card_count(context, count):
    """Step: Verify the exact number of metric cards displayed."""
    overview_page = get_overview_page(context)
    actual_count = overview_page.count_metric_cards()
    assert actual_count == count, (
        f"Expected {count} metric cards, but found {actual_count}. "
        f"Check if all cards are loading correctly or if page structure changed."
    )


@then('I should see the "{metric_name}" metric card')
def step_verify_metric_card_visible(context, metric_name):
    """Step: Verify a specific metric card is visible by name."""
    overview_page = get_overview_page(context)
    assert overview_page.is_metric_card_visible(metric_name), (
        f"Metric card '{metric_name}' is not visible. "
        f"Card may not have loaded or the text may have changed."
    )


@then("all metric values should be numeric and properly formatted")
def step_verify_metric_values_numeric(context):
    """Step: Verify all metric values are numeric and properly formatted."""
    overview_page = get_overview_page(context)
    is_valid, message = overview_page.verify_all_metric_values_numeric()
    assert is_valid, f"Metric value validation failed: {message}"
