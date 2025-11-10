# pages/base_page.py

class BasePage:
    """Base class for all page objects with common functionality"""
    
    def __init__(self, page, base_url=""):
        self.page = page
        self.base_url = base_url
    
    def wait_for_page_load(self, state="networkidle"):
        """Wait for page to load completely."""
        self.page.wait_for_load_state(state)
    
    def navigate(self, url):
        """Navigate to a URL and wait for page load"""
        self.page.goto(url)
        self.wait_for_page_load()
    
    def click_and_wait(self, selector, wait_state="networkidle"):
        """Click an element and wait for navigation/load to complete"""
        self.page.click(selector)
        self.wait_for_page_load(wait_state)
    
    def get_title(self):
        """Get the current page title"""
        return self.page.title()
    
    def get_url(self):
        """Get the current page URL"""
        return self.page.url
    
    def wait_for_selector(self, selector, state="visible", timeout=30000):
        """Wait for a selector to be in a specific state."""
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

