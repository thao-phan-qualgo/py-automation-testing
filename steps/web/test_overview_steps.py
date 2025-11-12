import pytest
from pathlib import Path
from pytest_bdd import scenarios, given, then

# Link the feature file using absolute path
CURRENT_DIR = Path(__file__).parent
FEATURE_FILE = CURRENT_DIR / "../../features/it_asset_inventory/overview.feature"
scenarios(str(FEATURE_FILE.resolve()))


@given("I am on the Overview page")
def on_overview_page(page):
    """Step placeholder: Navigate to Overview page"""
    # This step is not implemented yet
    pytest.skip("Step not implemented")


@then("I should see the Overview page")
def verify_overview_page(page):
    """Step placeholder: Verify Overview page is displayed"""
    assert page.get_by_text("Overview").is_visible(), "Overview page is not displayed"
