"""
Locator helper utilities for building robust element selectors.

This module provides utilities for creating and managing locators
with fallback strategies for better test resilience.
"""

import logging
from typing import List, Optional

from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


class LocatorStrategy:
	"""Helper class for managing multiple locator strategies with fallbacks."""

	def __init__(self, primary: str, fallbacks: Optional[List[str]] = None):
		"""
		Initialize locator strategy.
		"""
		self.primary = primary
		self.fallbacks = fallbacks or []

	def find_element(
			self, page: Page, timeout: int = 5000, state: str = "visible"
	) -> Optional[Locator]:
		"""
		Find element using primary selector or fallbacks.
		"""
		# Try primary selector
		try:
			page.wait_for_selector(self.primary, state=state, timeout=timeout)
			logger.debug(f"Element found with primary selector: {self.primary}")
			return page.locator(self.primary)
		except PlaywrightTimeoutError:
			logger.debug(f"Primary selector not found: {self.primary}")

		# Try fallback selectors
		for fallback in self.fallbacks:
			try:
				page.wait_for_selector(fallback, state=state, timeout=timeout)
				logger.info(f"Element found with fallback selector: {fallback}")
				return page.locator(fallback)
			except PlaywrightTimeoutError:
				logger.debug(f"Fallback selector not found: {fallback}")

		logger.error("Element not found with any selector strategy")
		return None


def build_data_testid_selector(testid: str) -> str:
	"""Build a data-testid selector."""
	return f'[data-testid="{testid}"]'


def build_role_selector(role: str, name: Optional[str] = None) -> str:
	"""Build an ARIA role selector."""
	if name:
		return f'role={role}[name="{name}"]'
	return f"role={role}"


def build_text_selector(text: str, exact: bool = False) -> str:
	"""Build a text-based selector."""
	if exact:
		return f'text="{text}"'
	return f"text={text}"


def combine_selectors(*selectors: str, operator: str = " ") -> str:
	"""Combine multiple selectors with an operator."""
	return operator.join(selectors)


class CommonLocators:
	"""Common locator patterns used across the application."""

	# Forms
	SUBMIT_BUTTON = 'button[type="submit"], input[type="submit"]'
	TEXT_INPUT = 'input[type="text"]'
	EMAIL_INPUT = 'input[type="email"]'
	PASSWORD_INPUT = 'input[type="password"]'

	# Navigation
	NAV_LINK = 'nav a, [role="navigation"] a'

	# Messages
	ERROR_MESSAGE = '.error, [role="alert"], .alert-error, .error-message'
	SUCCESS_MESSAGE = '.success, [role="status"], .alert-success'
	WARNING_MESSAGE = ".warning, .alert-warning"

	# Common elements
	MODAL = '[role="dialog"], .modal'
	LOADING_SPINNER = '.spinner, .loading, [aria-busy="true"]'
	HEADING = 'h1, h2, h3, [role="heading"]'

	@staticmethod
	def button_with_text(text: str) -> str:
		"""Get selector for button containing text."""
		return f'button:has-text("{text}"), input[value="{text}"]'

	@staticmethod
	def input_by_placeholder(placeholder: str) -> str:
		"""Get selector for input with placeholder."""
		return f'input[placeholder*="{placeholder}"]'

	@staticmethod
	def link_with_text(text: str) -> str:
		"""Get selector for link containing text."""
		return f'a:has-text("{text}")'
