import pytest
import os
from pathlib import Path
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page, portal_base_url):
    return LoginPage(page, portal_base_url)


@pytest.fixture
def test_credentials():
    email = os.getenv("TEST_EMAIL")
    password = os.getenv("TEST_PASSWORD")

    if not email or not password:
        raise ValueError(
            "TEST_EMAIL and TEST_PASSWORD must be set in .env file. "
            "Never hardcode credentials in source code!"
        )

    return {"email": email, "password": password}


# ============================================================================
# GIVEN STEPS - Setup/Preconditions
# ============================================================================


@given("I am logged in as an admin user")
def logged_in_as_admin(login_page, test_credentials):
    """Step: User is logged in as admin"""
    login_page.goto_sign_in()
    login_page.complete_full_login(
        email=test_credentials["email"],
        password=test_credentials["password"],
    )
