"""
Base page object for all page classes.

This module provides the BasePage class with common functionality
for all page objects following the Page Object Model (POM) pattern.
"""

import logging
from typing import Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all page objects with common functionality.
    """

    def __init__(self, page: Page, base_url: str = ""):
        """
        Initialize the base page object.

        Args:
            page: Playwright page instance
            base_url: Base URL of the application
        """
        self.page = page
        self.base_url = base_url

    def wait_for_page_load(
        self, state: str = "networkidle", timeout: int = 30000
    ) -> None:
        """
        Wait for page to load completely.

        Args:
            state: Load state to wait for (load, domcontentloaded, networkidle)
            timeout: Maximum time to wait in milliseconds

        Raises:
            PlaywrightTimeoutError: If page doesn't reach the desired state within timeout
        """
        try:
            self.page.wait_for_load_state(state, timeout=timeout)
            logger.debug(f"Page loaded successfully (state: {state})")
        except PlaywrightTimeoutError:
            logger.error(f"Timeout waiting for page load state: {state}")
            raise

    def navigate(self, url: str, wait_state: str = "networkidle") -> None:
        """
        Navigate to a URL and wait for page load.

        Args:
            url: URL to navigate to
            wait_state: Load state to wait for after navigation

        Raises:
            PlaywrightTimeoutError: If navigation or page load times out
        """
        try:
            logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until=wait_state)
            logger.debug(f"Successfully navigated to: {url}")
        except PlaywrightTimeoutError:
            logger.error(f"Timeout navigating to: {url}")
            raise

    def click_and_wait(self, selector: str, wait_state: str = "networkidle") -> None:
        """
        Click an element and wait for navigation/load to complete.

        Args:
            selector: CSS selector of the element to click
            wait_state: Load state to wait for after clicking

        Raises:
            PlaywrightTimeoutError: If element not found or load times out
        """
        try:
            logger.debug(f"Clicking element: {selector}")
            self.page.click(selector)
            self.wait_for_page_load(wait_state)
        except PlaywrightTimeoutError:
            logger.error(f"Timeout clicking element: {selector}")
            raise

    def fill_input(self, selector: str, value: str, clear_first: bool = True) -> None:
        """
        Fill an input field with a value.

        Args:
            selector: CSS selector of the input element
            value: Value to fill
            clear_first: Whether to clear the field before filling

        Raises:
            PlaywrightTimeoutError: If input element not found
        """
        try:
            if clear_first:
                self.page.fill(selector, "")
            self.page.fill(selector, value)
            logger.debug(f"Filled input {selector} with value")
        except PlaywrightTimeoutError:
            logger.error(f"Timeout filling input: {selector}")
            raise

    def get_title(self) -> str:
        """
        Get the current page title.

        Returns:
            The page title
        """
        return self.page.title()

    def get_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            The current URL
        """
        return self.page.url

    def wait_for_selector(
        self, selector: str, state: str = "visible", timeout: int = 30000
    ) -> None:
        """
        Wait for a selector to be in a specific state.

        Args:
            selector: CSS selector to wait for
            state: State to wait for (visible, hidden, attached, detached)
            timeout: Maximum time to wait in milliseconds

        Raises:
            PlaywrightTimeoutError: If selector doesn't reach desired state within timeout
        """
        try:
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
            logger.debug(f"Selector found: {selector} (state: {state})")
        except PlaywrightTimeoutError:
            logger.error(f"Timeout waiting for selector: {selector} (state: {state})")
            raise

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            selector: CSS selector of the element
            timeout: Maximum time to wait in milliseconds

        Returns:
            True if element is visible, False otherwise
        """
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            logger.debug(f"Element not visible: {selector}")
            return False

    def get_text(self, selector: str, timeout: int = 5000) -> Optional[str]:
        """
        Get text content of an element.

        Args:
            selector: CSS selector of the element
            timeout: Maximum time to wait for element

        Returns:
            Text content of the element, or None if not found
        """
        try:
            self.wait_for_selector(selector, timeout=timeout)
            return self.page.locator(selector).first.text_content()
        except PlaywrightTimeoutError:
            logger.warning(f"Could not get text from selector: {selector}")
            return None
