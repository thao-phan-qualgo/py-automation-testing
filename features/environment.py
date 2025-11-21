"""
Behave environment configuration and hooks.

This file contains all environment setup, teardown, and hook functions
for Behave test execution. Behave requires this file in the features/ directory.

Hooks execution order:
1. before_all - Run once before all tests
2. before_scenario - Run before each scenario
3. [test execution]
4. after_scenario - Run after each scenario (including cleanup)
5. after_all - Run once after all tests

Documentation: https://behave.readthedocs.io/en/stable/api.html#environment-file-functions
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

# Import Allure for enhanced reporting
try:
	import allure
	from allure_commons.types import AttachmentType

	ALLURE_AVAILABLE = True
except ImportError:
	ALLURE_AVAILABLE = False

# Ensure project root is in Python path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
	sys.path.insert(0, str(project_root))

# Import settings after adding project root to path
from config.settings import (
	BROWSER,
	HEADLESS,
	PORTAL_BASE_URL,
	DEBUG,
	SLOW_MO,
	TRACE,
	DEFAULT_TIMEOUT,
	SCREENSHOT_ON_FAILURE,
	SCREENSHOT_DIR,
	VIDEO_ON_FAILURE,
	VIDEO_DIR,
)

# Import step modules to register them with Behave
# Behave will automatically discover step definitions in features/steps/
# from features.steps.common import login_steps, overview_steps  # noqa: F401

# Setup logging
logger = logging.getLogger(__name__)


# ============================================================================
# BEFORE HOOKS
# ============================================================================


def before_all(context):
	"""
	Hook that runs once before all tests.

	Initializes:
	- Playwright instance
	- Browser instance (chromium/firefox/webkit)
	- Global test configuration

	Args:
		context: Behave context object (shared across all scenarios)
	"""
	logger.info("Initializing test environment...")

	# Start Playwright
	context.playwright = sync_playwright().start()

	# Configure browser launch options
	launch_options = {
		"headless": HEADLESS,
		"slow_mo": SLOW_MO if DEBUG else 0,
	}

	# Add debug-specific options
	if DEBUG:
		launch_options["args"] = [
			"--disable-blink-features=AutomationControlled",
			"--disable-dev-shm-usage",
		]

	# Launch browser based on configuration
	if BROWSER == "chromium":
		context.browser = context.playwright.chromium.launch(**launch_options)
	elif BROWSER == "firefox":
		context.browser = context.playwright.firefox.launch(**launch_options)
	elif BROWSER == "webkit":
		context.browser = context.playwright.webkit.launch(**launch_options)
	else:
		raise ValueError(
			f"Unsupported browser: {BROWSER}. "
			f"Supported browsers: chromium, firefox, webkit"
		)

	# Store base URL for easy access in tests
	context.portal_base_url = PORTAL_BASE_URL

	# Display debug information if enabled
	if DEBUG:
		print("\n" + "=" * 60)
		print("🐛 DEBUG MODE ENABLED")
		print("=" * 60)
		print(f"   Browser: {BROWSER}")
		print(f"   Headless: {HEADLESS}")
		print(f"   Slow Motion: {SLOW_MO}ms")
		print(f"   Trace: {TRACE}")
		print(f"   Base URL: {PORTAL_BASE_URL}")
		print("=" * 60 + "\n")

	logger.info(f"Browser {BROWSER} launched successfully")


def before_scenario(context, scenario):
	"""
	Hook that runs before each scenario.

	Creates a fresh browser context and page for each test scenario
	to ensure test isolation.

	Args:
		context: Behave context object
		scenario: Current scenario being executed
	"""
	logger.info(f"Starting scenario: {scenario.name}")

	# Configure browser context options
	context_options = {
		"viewport": {"width": 1280, "height": 920},
		"user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
		              "AppleWebKit/537.36 (KHTML, like Gecko) "
		              "Chrome/120.0.0.0 Safari/537.36",
	}

	# Enable video recording if configured
	if VIDEO_ON_FAILURE:
		os.makedirs(VIDEO_DIR, exist_ok=True)
		context_options["record_video_dir"] = VIDEO_DIR
		context_options["record_video_size"] = {"width": 1280, "height": 920}

	# Create new browser context for this scenario
	context.browser_context = context.browser.new_context(**context_options)

	# Start tracing if enabled (for debugging)
	if TRACE:
		context.browser_context.tracing.start(
			screenshots=True, snapshots=True, sources=True
		)

	# Create new page
	context.page = context.browser_context.new_page()
	context.page.set_default_timeout(DEFAULT_TIMEOUT)

	# Enable console and error logging in debug mode
	if DEBUG:
		context.page.on(
			"console", lambda msg: print(f"🖥️  Console [{msg.type}]: {msg.text}")
		)
		context.page.on("pageerror", lambda err: print(f"❌ Page Error: {err}"))

	logger.debug(f"Browser context created for scenario: {scenario.name}")


# ============================================================================
# AFTER HOOKS
# ============================================================================


def after_scenario(context, scenario):
	"""
	Hook that runs after each scenario.

	Handles cleanup and captures debugging artifacts on failure:
	- Saves trace files
	- Takes screenshots
	- Attaches artifacts to Allure report
	- Closes browser context and page

	Args:
		context: Behave context object
		scenario: Completed scenario
	"""
	logger.info(f"Scenario '{scenario.name}' completed with status: {scenario.status}")

	# Save trace on failure
	if TRACE and scenario.status == "failed":
		trace_dir = "reports/traces"
		os.makedirs(trace_dir, exist_ok=True)
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		scenario_name = _sanitize_filename(scenario.name)
		trace_path = f"{trace_dir}/{scenario_name}_{timestamp}.zip"

		try:
			context.browser_context.tracing.stop(path=trace_path)
			print(f"\n📊 Trace saved: {trace_path}")
			print(f"   View with: playwright show-trace {trace_path}\n")
			logger.info(f"Trace saved: {trace_path}")

			# Attach trace to Allure report
			if ALLURE_AVAILABLE:
				try:
					allure.attach.file(
						trace_path,
						name="Playwright Trace",
						attachment_type=AttachmentType.ZIP,
					)
				except Exception as e:
					logger.debug(f"Could not attach trace to Allure: {e}")
		except Exception as e:
			logger.error(f"Failed to save trace: {e}")
	elif TRACE:
		try:
			context.browser_context.tracing.stop()
		except Exception as e:
			logger.error(f"Failed to stop tracing: {e}")

	# Take screenshot on failure
	if SCREENSHOT_ON_FAILURE and scenario.status == "failed":
		screenshot_dir = SCREENSHOT_DIR
		os.makedirs(screenshot_dir, exist_ok=True)
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		scenario_name = _sanitize_filename(scenario.name)
		filepath = os.path.join(screenshot_dir, f"{scenario_name}_{timestamp}.png")

		try:
			screenshot_bytes = context.page.screenshot(path=filepath, full_page=True)
			print(f"📸 Screenshot saved: {filepath}\n")
			logger.info(f"Screenshot saved: {filepath}")

			# Attach screenshot to Allure report
			if ALLURE_AVAILABLE:
				try:
					allure.attach(
						screenshot_bytes,
						name=f"Failure Screenshot - {scenario.name}",
						attachment_type=AttachmentType.PNG,
					)
				except Exception as e:
					logger.debug(f"Could not attach screenshot to Allure: {e}")
		except Exception as e:
			logger.error(f"Failed to save screenshot: {e}")

	# Attach browser console logs on failure (for debugging)
	if ALLURE_AVAILABLE and scenario.status == "failed":
		try:
			# Capture page URL and other debugging info
			page_info = f"URL: {context.page.url}\n"
			page_info += f"Title: {context.page.title()}\n"
			page_info += f"Status: {scenario.status}\n"

			allure.attach(
				page_info,
				name="Page Information",
				attachment_type=AttachmentType.TEXT,
			)
		except Exception as e:
			logger.debug(f"Could not attach page info to Allure: {e}")

	# Always cleanup: close page and context
	try:
		context.page.close()
		context.browser_context.close()
		logger.debug("Browser context closed successfully")
	except Exception as e:
		logger.error(f"Error during cleanup: {e}")


def after_all(context):
	"""
	Hook that runs once after all tests.

	Performs final cleanup:
	- Closes browser instance
	- Stops Playwright

	Args:
		context: Behave context object
	"""
	logger.info("Cleaning up test environment...")

	try:
		context.browser.close()
		context.playwright.stop()
		logger.info("Browser and Playwright stopped successfully")
	except Exception as e:
		logger.error(f"Error during final cleanup: {e}")

	if DEBUG:
		print("\n" + "=" * 60)
		print("✅ Test execution completed")
		print("=" * 60 + "\n")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _sanitize_filename(filename: str) -> str:
	"""
	Sanitize a string to be used as a filename.

	Args:
		filename: Original filename string

	Returns:
		Sanitized filename safe for use in file systems
	"""
	# Replace spaces and slashes with underscores
	sanitized = filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
	# Remove other problematic characters
	sanitized = "".join(c for c in sanitized if c.isalnum() or c in "._-")
	return sanitized


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
	"before_all",
	"after_all",
	"before_scenario",
	"after_scenario",
]
