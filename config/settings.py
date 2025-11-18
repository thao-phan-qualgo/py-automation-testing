"""
Unified Configuration Settings.

This module loads all configuration from environment variables (.env file).
All sensitive data (credentials, secrets) must be stored in .env file.

Environment variables are loaded from:
- .env file in project root (recommended for local development)
- System environment variables (for CI/CD and production)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

# ============================================================================
# PROJECT PATHS
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

# Load environment variables from .env file
load_dotenv(dotenv_path=ENV_PATH)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_bool_env(key: str, default: str = "false") -> bool:
	"""Convert environment variable to boolean."""
	return os.getenv(key, default).lower() == "true"


def get_int_env(key: str, default: str) -> int:
	"""Convert environment variable to integer."""
	return int(os.getenv(key, default))


# ============================================================================
# ENVIRONMENT & APPLICATION
# ============================================================================

ENV = os.getenv("ENV", "dev")
PORTAL_BASE_URL = os.getenv(
	"PORTAL_BASE_URL", os.getenv("BASE_URL", "https://dev-aisoc-fe.qualgo.dev")
)

# ============================================================================
# BROWSER CONFIGURATION
# ============================================================================

BROWSER = os.getenv("BROWSER", "chromium")  # chromium | firefox | webkit
HEADLESS = get_bool_env("HEADLESS", "true")
SLOW_MO = get_int_env("SLOW_MO", "0")  # Slow down execution (milliseconds)

# ============================================================================
# DEBUG & TRACING
# ============================================================================

DEBUG = get_bool_env("DEBUG", "false")
TRACE = get_bool_env("TRACE", "false")  # Enable Playwright trace recording

# ============================================================================
# TIMEOUTS (in milliseconds)
# ============================================================================

DEFAULT_TIMEOUT = get_int_env("DEFAULT_TIMEOUT", "10000")
NAVIGATION_TIMEOUT = get_int_env("NAVIGATION_TIMEOUT", "30000")

# ============================================================================
# SCREENSHOTS & VIDEOS
# ============================================================================

SCREENSHOT_ON_FAILURE = get_bool_env("SCREENSHOT_ON_FAILURE", "true")
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "reports/screenshots")

VIDEO_ON_FAILURE = get_bool_env("VIDEO_ON_FAILURE", "false")
VIDEO_DIR = os.getenv("VIDEO_DIR", "reports/videos")

# ============================================================================
# WEB TEST CREDENTIALS (from .env - no defaults for security)
# ============================================================================

TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
TEST_MFA_CODE = os.getenv("TEST_MFA_CODE")

# ============================================================================
# API / KEYCLOAK CONFIGURATION
# ============================================================================

# Keycloak endpoints and realm
KEYCLOAK_BASE_URL = os.getenv(
	"KEYCLOAK_BASE_URL", "https://nonprod-common-keycloak.qualgo.dev"
)
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "dev-ai-soc")
KEYCLOAK_TOKEN_ENDPOINT = (
	f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}" "/protocol/openid-connect/token"
)

# API Credentials (from .env - no defaults for security)
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_USERNAME = os.getenv("KEYCLOAK_USERNAME")
KEYCLOAK_PASSWORD = os.getenv("KEYCLOAK_PASSWORD")
KEYCLOAK_GRANT_TYPE = os.getenv("KEYCLOAK_GRANT_TYPE", "password")

# Invalid credentials for negative testing (from .env)
KEYCLOAK_INVALID_USERNAME = os.getenv("KEYCLOAK_INVALID_USERNAME", "invalid@qualgo.net")
KEYCLOAK_INVALID_PASSWORD = os.getenv("KEYCLOAK_INVALID_PASSWORD", "WrongPassword123@")

# ============================================================================
# API PERFORMANCE THRESHOLDS
# ============================================================================

MAX_RESPONSE_TIME_MS = get_int_env("MAX_RESPONSE_TIME_MS", "3000")
TOKEN_EXPIRES_IN = get_int_env("TOKEN_EXPIRES_IN", "300")  # 5 minutes
REFRESH_TOKEN_EXPIRES_IN = get_int_env("REFRESH_TOKEN_EXPIRES_IN", "1800")  # 30 minutes

# ============================================================================
# EXPECTED JWT CLAIMS (for validation)
# ============================================================================

EXPECTED_JWT_CLAIMS = [
	"exp",  # Expiration time
	"iat",  # Issued at
	"jti",  # JWT ID
	"iss",  # Issuer
	"aud",  # Audience
	"sub",  # Subject
	"typ",  # Type
	"azp",  # Authorized party
	"sid",  # Session ID
	"acr",  # Authentication Context Class Reference
	"scope",  # Scope
	"email_verified",  # Email verified
	"preferred_username",  # Preferred username
	"email",  # Email
]


# ============================================================================
# CONFIGURATION HELPERS
# ============================================================================


def get_keycloak_config() -> Dict[str, str]:
	"""
	Get Keycloak configuration as a dictionary.

	Returns:
		Dictionary with Keycloak configuration
	"""
	return {
		"endpoint": KEYCLOAK_TOKEN_ENDPOINT,
		"realm": KEYCLOAK_REALM,
		"base_url": KEYCLOAK_BASE_URL,
	}


def get_valid_credentials() -> Dict[str, str]:
	"""
	Get valid test credentials for API authentication.

	Returns:
		Dictionary with valid credentials

	Raises:
		ValueError: If required credentials are not set
	"""
	if not all(
			[
				KEYCLOAK_CLIENT_ID,
				KEYCLOAK_CLIENT_SECRET,
				KEYCLOAK_USERNAME,
				KEYCLOAK_PASSWORD,
			]
	):
		raise ValueError(
			"API credentials not configured. Please set the following in .env:\n"
			"  - KEYCLOAK_CLIENT_ID\n"
			"  - KEYCLOAK_CLIENT_SECRET\n"
			"  - KEYCLOAK_USERNAME\n"
			"  - KEYCLOAK_PASSWORD"
		)

	return {
		"client_id": KEYCLOAK_CLIENT_ID,
		"client_secret": KEYCLOAK_CLIENT_SECRET,
		"username": KEYCLOAK_USERNAME,
		"password": KEYCLOAK_PASSWORD,
		"grant_type": KEYCLOAK_GRANT_TYPE,
	}


def get_invalid_username_credentials() -> Dict[str, str]:
	"""Get credentials with invalid username for negative testing."""
	base = get_valid_credentials()
	base["username"] = KEYCLOAK_INVALID_USERNAME
	return base


def get_invalid_password_credentials() -> Dict[str, str]:
	"""Get credentials with invalid password for negative testing."""
	base = get_valid_credentials()
	base["password"] = KEYCLOAK_INVALID_PASSWORD
	return base


def validate_web_credentials() -> None:
	"""
	Validate that common test credentials are configured.

	Raises:
		ValueError: If credentials are not set
	"""
	if not all([TEST_EMAIL, TEST_PASSWORD]):
		raise ValueError(
			"Web test credentials not configured. Please set in .env:\n"
			"  - TEST_EMAIL\n"
			"  - TEST_PASSWORD"
		)


def get_performance_thresholds() -> Dict[str, int]:
	"""Get API performance thresholds."""
	return {
		"max_response_time_ms": MAX_RESPONSE_TIME_MS,
		"token_expires_in": TOKEN_EXPIRES_IN,
		"refresh_token_expires_in": REFRESH_TOKEN_EXPIRES_IN,
	}


# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================


def validate_config() -> Dict[str, Any]:
	"""
	Validate configuration and return status.

	Returns:
		Dictionary with validation results
	"""
	results = {
		"valid": True,
		"errors": [],
		"warnings": [],
	}

	# Check common credentials
	if not TEST_EMAIL or not TEST_PASSWORD:
		results["warnings"].append("Web test credentials not configured")

	# Check API credentials
	if not all([KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET]):
		results["warnings"].append("API test credentials not configured")

	# Check browser configuration
	if BROWSER not in ["chromium", "firefox", "webkit"]:
		results["errors"].append(f"Invalid browser: {BROWSER}")
		results["valid"] = False

	return results


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
	# Paths
	"BASE_DIR",
	"ENV_PATH",
	# Environment
	"ENV",
	"PORTAL_BASE_URL",
	# Browser
	"BROWSER",
	"HEADLESS",
	"SLOW_MO",
	# Debug
	"DEBUG",
	"TRACE",
	# Timeouts
	"DEFAULT_TIMEOUT",
	"NAVIGATION_TIMEOUT",
	# Screenshots/Videos
	"SCREENSHOT_ON_FAILURE",
	"SCREENSHOT_DIR",
	"VIDEO_ON_FAILURE",
	"VIDEO_DIR",
	# Web Credentials
	"TEST_EMAIL",
	"TEST_PASSWORD",
	"TEST_MFA_CODE",
	# Keycloak
	"KEYCLOAK_BASE_URL",
	"KEYCLOAK_REALM",
	"KEYCLOAK_TOKEN_ENDPOINT",
	"KEYCLOAK_CLIENT_ID",
	"KEYCLOAK_CLIENT_SECRET",
	"KEYCLOAK_USERNAME",
	"KEYCLOAK_PASSWORD",
	"KEYCLOAK_GRANT_TYPE",
	# Performance
	"MAX_RESPONSE_TIME_MS",
	"TOKEN_EXPIRES_IN",
	"REFRESH_TOKEN_EXPIRES_IN",
	# JWT
	"EXPECTED_JWT_CLAIMS",
	# Helper functions
	"get_keycloak_config",
	"get_valid_credentials",
	"get_invalid_username_credentials",
	"get_invalid_password_credentials",
	"validate_web_credentials",
	"get_performance_thresholds",
	"validate_config",
]
