# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# Environment
ENV = os.getenv("ENV", "dev")

# Application URL
PORTAL_BASE_URL = os.getenv("PORTAL_BASE_URL", os.getenv("BASE_URL", "https://dev-aisoc-fe.qualgo.dev"))

# Browser Configuration
BROWSER = os.getenv("BROWSER", "chromium")  # chromium | firefox | webkit
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Debug Configuration
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Slow down execution (milliseconds)
TRACE = os.getenv("TRACE", "false").lower() == "true"  # Enable trace recording

# Test Credentials (MUST be set in .env - no defaults for security)
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
TEST_MFA_CODE = os.getenv("TEST_MFA_CODE")

# Timeouts (in milliseconds)
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))

# Screenshot Configuration
SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "reports/screenshots")

# Video Recording
VIDEO_ON_FAILURE = os.getenv("VIDEO_ON_FAILURE", "false").lower() == "true"
VIDEO_DIR = os.getenv("VIDEO_DIR", "reports/videos")

