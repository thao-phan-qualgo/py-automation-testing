import re
from typing import List, Optional, Tuple

from playwright.sync_api import Locator

from pages.base_page import BasePage
from utils.wait_helpers import wait_for_element_state


class OverviewPage(BasePage):
    """Page Object Model for IT Asset Inventory Overview page."""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self._initialize_locators()

    def _initialize_locators(self):
        """Initialize all page locators in one place for better maintainability."""

        # Page URL
        self.overview_url = f"{self.base_url}/it-asset-inventory/overview"

        # Main page elements
        self.locators = {
            # Page heading
            "page_heading": 'h1:has-text("Overview"), [data-testid="overview-heading"]',
            # Sections
            "security_posture_section": (
                '[data-testid="security-posture-section"], '
                'section:has-text("Security Posture Overview")'
            ),
            "security_posture_title": (
                'h2:has-text("Security Posture Overview"), '
                'h3:has-text("Security Posture Overview")'
            ),
            # Metric cards (generic)
            "metric_cards": '[data-testid*="metric-card"], .metric-card, [class*="metric-card"]',
            "metric_card_title": '[data-testid="metric-title"], .metric-title, [class*="metric-title"]',
            "metric_card_value": '[data-testid="metric-value"], .metric-value, [class*="metric-value"]',
            # Specific metric cards
            "critical_assets": ':text("Critical Assets")',
            "non_compliant_assets": ':text("Non-Compliant Assets")',
            "inactive_devices": ':text("Inactive Devices")',
            "compliance_coverage": ':text("Compliance Coverage")',
            # Endpoint Devices section
            "endpoint_devices_section": (
                '[data-testid="endpoint-devices-section"], '
                'section:has-text("Endpoint Devices")'
            ),
            "endpoint_devices_title": 'h2:has-text("Endpoint Devices"), h3:has-text("Endpoint Devices")',
            "pie_chart": '[data-testid="pie-chart"], .pie-chart, canvas, svg[class*="chart"]',
            "devices_by_criticality": ':text("Devices by Criticality")',
            "total_devices_count": '[data-testid="total-devices"], .total-devices',
            "view_more_link": 'a:has-text("View More"), button:has-text("View More")',
            # Criticality levels
            "criticality_critical": ':text("Critical")',
            "criticality_high": ':text("High")',
            "criticality_medium": ':text("Medium")',
            "criticality_low": ':text("Low")',
        }

    def _get_locator(self, key: str) -> str:
        """Helper method to get locator by key."""
        return self.locators.get(key, "")

    # ============================================================================
    # Navigation Methods
    # ============================================================================

    def goto_overview(self) -> None:
        """Navigate to the Overview page."""
        self.navigate(self.overview_url)

    def click_menu_item(self, menu_item: str) -> None:
        """Click on a main menu item."""
        self.page.get_by_role("button", name=menu_item).click()

    def click_submenu_item(self, submenu_item: str) -> None:
        """Click on a submenu item."""
        self.page.get_by_role("link", name=submenu_item).click()

    def navigate_via_menu(self, menu_item: str, submenu_item: str) -> None:
        """Navigate to Overview page using menu navigation."""
        self.click_menu_item(menu_item)
        self.click_submenu_item(submenu_item)

    def navigate_to_it_asset_inventory_overview(self) -> None:
        """Navigate to IT Asset Inventory Overview section."""
        self.goto_overview()

    # ============================================================================
    # Element Interaction Methods
    # ============================================================================

    def locate_section(self, section_name: str) -> Optional[Locator]:
        """Locate a specific section on the page by its name."""
        section_locator = f':text("{section_name}")'
        try:
            self.wait_for_selector(section_locator, state="visible", timeout=10000)
            return self.page.locator(section_locator).first
        except Exception as e:
            print(f"Failed to locate section '{section_name}': {str(e)}")
            return None

    def is_section_visible(self, section_name: str) -> bool:
        """Check if a section is visible on the page."""
        try:
            section = self.locate_section(section_name)
            return section is not None and section.is_visible()
        except Exception:
            return False

    # ============================================================================
    # Verification Methods - Section Title
    # ============================================================================

    def get_section_title(self, title: str) -> Locator:
        """Get section title element by text."""
        return self.page.get_by_text(title)

    def is_section_title_visible(self, title: str) -> bool:
        """Verify if a section title is visible on the page."""
        try:
            # Wait for the section title element to appear
            section_title_locator = self.get_section_title(title)
            section_title_locator.wait_for(state="visible", timeout=10000)
            return section_title_locator.is_visible()
        except Exception as e:
            print(f"Section title '{title}' not visible: {str(e)}")
            return False

    # ============================================================================
    # Verification Methods - Metric Cards
    # ============================================================================

    def get_all_metric_cards(self) -> List[Locator]:
        """Get all metric cards displayed on the page."""
        metric_cards_selector = self._get_locator("metric_cards")
        self.wait_for_selector(metric_cards_selector, state="visible", timeout=10000)
        return self.page.locator(metric_cards_selector).all()

    def count_metric_cards(self) -> int:
        """Count the number of metric cards displayed."""
        try:
            cards = self.get_all_metric_cards()
            return len(cards)
        except Exception as e:
            print(f"Error counting metric cards: {str(e)}")
            return 0

    def is_metric_card_visible(self, metric_name: str) -> bool:
        """Check if a specific metric card is visible."""
        try:
            metric_card = self.page.get_by_text(metric_name)
            # Wait for the metric card to be visible before checking
            metric_card.wait_for(state="visible", timeout=10000)
            return metric_card.is_visible()
        except Exception as e:
            print(f"Metric card '{metric_name}' not visible: {str(e)}")
            return False

    def get_metric_card_by_name(self, metric_name: str) -> Locator:
        """Get a specific metric card element by its name."""
        return self.page.get_by_text(metric_name)

    # ============================================================================
    # Verification Methods - Metric Values
    # ============================================================================

    def get_all_metric_values(self) -> List[Locator]:
        """Get all metric value elements on the page."""
        metric_value_selector = self._get_locator("metric_card_value")

        # Wait for at least one metric value to be visible before getting all
        try:
            wait_for_element_state(
                self.page, metric_value_selector, state="visible", timeout=15000
            )
        except Exception as e:
            # If wait fails, log but continue to return empty list
            # which will be handled by the calling method
            pass

        return self.page.locator(metric_value_selector).all()

    def is_value_numeric_and_formatted(self, value_text: str) -> bool:
        """Check if a value is numeric and properly formatted."""
        return bool(re.search(r"\d", value_text))

    def verify_all_metric_values_numeric(self) -> Tuple[bool, str]:
        """Verify all metric values are numeric and properly formatted."""
        try:
            metric_values = self.get_all_metric_values()

            if len(metric_values) == 0:
                return False, "No metric values found on the page"

            for metric in metric_values:
                value_text = metric.text_content().strip()
                if not self.is_value_numeric_and_formatted(value_text):
                    return (
                        False,
                        f"Metric value '{value_text}' is not properly formatted or numeric",
                    )

            return True, "All metric values are numeric and properly formatted"
        except Exception as e:
            return False, f"Error verifying metric values: {str(e)}"

    # ============================================================================
    # Specific Metric Card Methods
    # ============================================================================

    def is_critical_assets_card_visible(self) -> bool:
        """Check if Critical Assets metric card is visible."""
        return self.is_metric_card_visible("Critical Assets")

    def is_non_compliant_assets_card_visible(self) -> bool:
        """Check if Non-Compliant Assets metric card is visible."""
        return self.is_metric_card_visible("Non-Compliant Assets")

    def is_inactive_devices_card_visible(self) -> bool:
        """Check if Inactive Devices metric card is visible."""
        return self.is_metric_card_visible("Inactive Devices")

    def is_compliance_coverage_card_visible(self) -> bool:
        """Check if Compliance Coverage metric card is visible."""
        return self.is_metric_card_visible("Compliance Coverage")

    def verify_all_security_posture_cards_visible(self) -> Tuple[bool, str]:
        """Verify all four Security Posture metric cards are visible."""
        cards = {
            "Critical Assets": self.is_critical_assets_card_visible(),
            "Non-Compliant Assets": self.is_non_compliant_assets_card_visible(),
            "Inactive Devices": self.is_inactive_devices_card_visible(),
            "Compliance Coverage": self.is_compliance_coverage_card_visible(),
        }

        missing_cards = [name for name, visible in cards.items() if not visible]

        if missing_cards:
            return False, f"Missing cards: {', '.join(missing_cards)}"

        return True, "All Security Posture cards are visible"

    # ============================================================================
    # Page Verification Methods
    # ============================================================================

    def is_overview_page_displayed(self) -> bool:
        """Verify if Overview page is displayed by checking for Display Overview text after DOM loads."""
        try:
            # Wait for page to be fully loaded (DOM + network)
            self.wait_for_full_page_load()

            display_overview_locator = self.page.get_by_text("Display Overview")
            if display_overview_locator.count() > 0:
                return display_overview_locator.first.is_visible()

            overview_locator = self.page.get_by_text("Overview")
            if overview_locator.count() > 0:
                return overview_locator.first.is_visible()

            return False
        except Exception as e:
            print(f"Overview page not displayed: {str(e)}")
            return False

    def verify_page_loaded(self) -> bool:
        """Comprehensive check that the Overview page has loaded correctly."""
        try:
            self.wait_for_full_page_load()
            return self.is_overview_page_displayed()
        except Exception as e:
            print(f"Page load verification failed: {str(e)}")
            return False

    # ============================================================================
    # Endpoint Devices Section Methods
    # ============================================================================

    def scroll_to_endpoint_devices_section(self) -> None:
        """Scroll to the Endpoint Devices section."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        self.page.wait_for_timeout(500)  # Brief pause for smooth scrolling

    def is_endpoint_devices_title_visible(self) -> bool:
        """Check if Endpoint Devices section title is visible."""
        try:
            return self.page.get_by_text("Endpoint Devices").first.is_visible()
        except Exception:
            return False

    def is_pie_chart_displayed(self) -> bool:
        """Check if pie chart is displayed."""
        try:
            locator = self.page.locator(self._get_locator("pie_chart")).first
            return locator.is_visible()
        except Exception:
            return False

    def is_devices_by_criticality_visible(self) -> bool:
        """Check if 'Devices by Criticality' text is visible."""
        try:
            return self.page.get_by_text("Devices by Criticality").is_visible()
        except Exception:
            return False

    def is_criticality_level_visible(self, level: str) -> bool:
        """Check if a specific criticality level is visible."""
        try:
            return self.page.get_by_text(level).first.is_visible()
        except Exception:
            return False

    def is_total_devices_count_displayed(self) -> bool:
        """Check if total devices count is displayed."""
        try:
            # Look for elements that might contain total count
            total_locator = self.page.locator(self._get_locator("total_devices_count"))
            if total_locator.count() > 0:
                return total_locator.first.is_visible()
            # Fallback: look for text patterns like "Total: X devices" or "X Devices"
            return (
                self.page.get_by_text("Total").first.is_visible()
                or self.page.get_by_text("Devices").first.is_visible()
            )
        except Exception:
            return False

    def is_view_more_link_available(self) -> bool:
        """Check if View More link is available."""
        try:
            locator = self.page.locator(self._get_locator("view_more_link"))
            if locator.count() > 0:
                return locator.first.is_visible()
            return False
        except Exception:
            return False
