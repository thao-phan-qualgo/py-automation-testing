# pages/login_page.py
import time

from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for Login/Sign-in page with Microsoft SSO"""

    def __init__(self, page, base_url):
        super().__init__(page, base_url)

        # Locators - Sign-in page
        self.sign_in_with_microsoft_button = "button:has-text('Sign in with Microsoft')"

        # Locators - Microsoft login page
        self.email_input = 'input[type="email"][name="loginfmt"]'
        self.email_input_alt = 'input[placeholder*="email"]'
        self.password_input = 'input[type="password"][name="passwd"]'
        self.password_input_alt = 'input[placeholder*="password"]'
        self.next_button = 'input[type="submit"][value="Next"]'
        self.sign_in_button = 'input[type="submit"][value="Sign in"]'

        # Locators - MFA verification
        self.mfa_code_input = 'input[name="otc"]'
        self.mfa_code_input_alt = 'input[placeholder*="code"]'
        self.verify_button = 'input[type="submit"][value="Verify"]'

        # Locators - Stay signed in prompt
        self.dont_show_again_checkbox = 'input[type="checkbox"]'
        self.yes_button = 'input[type="submit"][value="Yes"]'
        self.no_button = 'input[type="submit"][value="No"]'

        # Locators - Dashboard
        self.dashboard_heading = 'h1, h2, [role="heading"]'

        # Error messages
        self.error_message = '.error-message, [role="alert"], .alert-error'

    def goto_sign_in(self):
        """Navigate to sign-in page"""
        self.navigate(f"{self.base_url}/sign-in")

    def click_sign_in_with_microsoft(self):
        """Click Sign in with Microsoft button"""
        self.click_and_wait(self.sign_in_with_microsoft_button)

    def enter_email(self, email):
        """Enter email address in Microsoft login form"""
        try:
            self.wait_for_selector(self.email_input, state="visible", timeout=5000)
            self.page.fill(self.email_input, email)
        except:
            self.wait_for_selector(self.email_input_alt, state="visible", timeout=5000)
            self.page.fill(self.email_input_alt, email)

    def click_next(self):
        """Click Next button"""
        self.click_and_wait(self.next_button)

    def enter_password(self, password):
        """Enter password in Microsoft login form"""
        try:
            self.wait_for_selector(self.password_input, state="visible", timeout=5000)
            self.page.fill(self.password_input, password)
        except:
            self.wait_for_selector(
                self.password_input_alt, state="visible", timeout=5000
            )
            self.page.fill(self.password_input_alt, password)

    def click_sign_in(self):
        """Click Sign in button and wait for navigation"""
        self.click_and_wait(self.sign_in_button)

        # After sign in, might go to MFA or directly to dashboard
        # Wait a moment to see which page we land on
        self.wait_for_page_load("networkidle")

    def manual_enter_mfa_code(self):
        """Wait 20 seconds for user to manually enter MFA code (script will click Verify)"""
        seconds = 20
        print("\n" + "=" * 60)
        print("⏸️  PAUSED FOR MANUAL MFA CODE ENTRY")
        print("=" * 60)
        print("📱 Please enter the MFA code from your authenticator app")
        print("⌨️  Just type the code - script will click Verify automatically")
        print(f"⏰ You have {seconds} seconds...")
        print("=" * 60 + "\n")

        # Wait 20 seconds for manual code entry
        for i in range(seconds, 0, -1):
            print(f"⏳ {i} seconds remaining...", end="\r", flush=True)
            time.sleep(1)

        print("\n\n✅ Code entry time complete!")
        print("🖱️  Script will now click Verify button...\n")

    def enter_mfa_code(self, code):
        """Enter MFA verification code"""
        try:
            self.wait_for_selector(self.mfa_code_input, state="visible", timeout=10000)
            self.page.fill(self.mfa_code_input, code)
        except Exception as e1:
            try:
                self.wait_for_selector(
                    self.mfa_code_input_alt, state="visible", timeout=10000
                )
                self.page.fill(self.mfa_code_input_alt, code)
            except Exception as e2:
                print(
                    f"MFA input not found. May not be required or already past this step."
                )

    def click_verify(self):
        """Click Verify button for MFA"""
        self.click_and_wait(self.verify_button)

    def check_dont_show_again(self):
        """Check 'Don't show this again' checkbox"""
        try:
            self.wait_for_selector(
                self.dont_show_again_checkbox, state="visible", timeout=5000
            )
            self.page.check(self.dont_show_again_checkbox)
        except:
            pass

    def click_stay_signed_in_yes(self):
        """Click Yes to stay signed in"""
        try:
            self.wait_for_selector(self.yes_button, state="visible", timeout=5000)
            self.check_dont_show_again()
            self.click_and_wait(self.yes_button)
        except Exception as e:
            print(f"Stay signed in prompt not found (may have already processed): {e}")
            pass

    def click_stay_signed_in_no(self):
        """Click No to not stay signed in"""
        self.click_and_wait(self.no_button)

    def get_dashboard_heading_text(self):
        """Get the dashboard heading text"""
        self.wait_for_selector(self.dashboard_heading, state="visible", timeout=15000)
        return self.page.locator(self.dashboard_heading).first.text_content()

    def verify_dashboard_heading(self, expected_text):
        """Verify dashboard heading contains expected text"""
        heading = self.get_dashboard_heading_text()
        return expected_text.lower() in heading.lower()

    def get_error_message(self):
        """Get error message text if present"""
        try:
            self.wait_for_selector(self.error_message, state="visible", timeout=5000)
            return self.page.locator(self.error_message).first.text_content()
        except:
            return None

    def is_error_visible(self):
        """Check if error message is visible"""
        return self.get_error_message() is not None

    def click_team_button(self, team_name: str) -> None:
        """Click the team selection button after successful login."""
        self.page.get_by_role("button", name=team_name).click()

    def select_team_from_dropdown(self, team_name: str) -> None:
        """Select a team from the team dropdown menu."""
        self.page.get_by_label(team_name).get_by_text(team_name).click()

    def complete_full_login(self, email, password, stay_signed_in=True):
        """Complete full login flow in one method"""
        self.click_sign_in_with_microsoft()
        self.enter_email(email)
        self.click_next()
        self.enter_password(password)
        self.click_sign_in()
        self.manual_enter_mfa_code()

        if stay_signed_in:
            self.click_stay_signed_in_yes()
        else:
            self.click_stay_signed_in_no()
        self.get_dashboard_heading_text()

    def complete_full_login_with_team(
        self, email: str, password: str, team_name: str, stay_signed_in: bool = True
    ) -> None:
        """Complete full login flow with team selection."""
        self.complete_full_login(email, password, stay_signed_in)
        self.click_team_button(team_name)
        self.select_team_from_dropdown(team_name)
