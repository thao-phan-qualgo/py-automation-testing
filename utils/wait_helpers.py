"""
Wait and polling helpers for test automation.

This module provides utility functions for waiting and polling
operations that can be reused across different page objects.
"""

import time
import logging
from typing import Callable, Any, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


logger = logging.getLogger(__name__)


def wait_for_condition(
    condition: Callable[[], bool],
    timeout: int = 30,
    poll_interval: float = 0.5,
    error_message: str = "Condition not met within timeout",
) -> bool:
    """Wait for a custom condition to be true."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if condition():
                return True
        except Exception as e:
            logger.debug(f"Condition check raised exception: {e}")
        time.sleep(poll_interval)

    raise TimeoutError(error_message)


def wait_for_element_state(
    page: Page, selector: str, state: str = "visible", timeout: int = 30000
) -> None:
    """Wait for an element to reach a specific state with retry logic."""
    try:
        page.wait_for_selector(selector, state=state, timeout=timeout)
        logger.debug(f"Element reached state '{state}': {selector}")
    except PlaywrightTimeoutError:
        logger.error(f"Timeout waiting for element state '{state}': {selector}")
        raise


def retry_on_failure(
    func: Callable[..., Any],
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple = (Exception,),
) -> Any:
    """Retry a function if it raises an exception."""
    last_exception = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}")
            if attempt < max_attempts:
                time.sleep(delay)

    logger.error(f"All {max_attempts} attempts failed")
    raise last_exception


def wait_for_text_to_appear(
    page: Page, text: str, timeout: int = 30000, exact: bool = False
) -> bool:
    """Wait for specific text to appear on the page."""
    try:
        locator = page.get_by_text(text, exact=exact)
        locator.wait_for(state="visible", timeout=timeout)
        logger.debug(f"Text appeared on page: '{text}'")
        return True
    except PlaywrightTimeoutError:
        logger.warning(f"Text did not appear within timeout: '{text}'")
        return False


def manual_wait_with_countdown(
    seconds: int, message: str = "Waiting for manual action"
) -> None:
    """Wait for a specified time with a countdown display."""
    print("\n" + "=" * 60)
    print(f"⏸️  {message.upper()}")
    print("=" * 60)
    print(f"⏰ You have {seconds} seconds...")
    print("=" * 60 + "\n")

    for i in range(seconds, 0, -1):
        print(f"⏳ {i} seconds remaining...", end="\r", flush=True)
        time.sleep(1)

    print("\n\n✅ Wait complete!\n")
