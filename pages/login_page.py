from pages.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    def __init__(self, page: Page, context):
        super().__init__(page, context)
        self.username_input = page.locator("input#loginFrm_loginname")
        self.password_input = page.locator("input#loginFrm_password")
        self.login_button = page.get_by_title("Login")
        self.title = page.locator("div.menu-text")  # Fixed: changed menu_text to menu-text
        self.error_message_login = page.get_by_text("× Error: Incorrect login or")
        self.account_dropdown = page.locator("li").nth(4)
        self.logout_confirmation_text = page.get_by_text("Account Logout", exact=True)
        self.continue_button = page.get_by_role("link", name=" Continue")
        self.login_register_link = page.get_by_role("link", name="Login or register")


    def login(self, user, pwd):
        """
        Perform login action by entering username and password, then clicking the login button. Screenshots are taken for each step for reporting purposes.
        Args:
            user (str): The username to be entered in the login form.
            pwd (str): The password to be entered in the login form.
        """
        self.enter_text(self.username_input, user, "Username")
        self.enter_text(self.password_input, pwd, "Password")
        self.click_element(self.login_button, "Login Button", screenshot=True)

    def verify_login_error_message(self):
        """
        Verify that the error message is displayed on the login page when invalid credentials are used. This method waits for the error message element to be visible and checks if it contains the expected text.
        """
        self.wait_for_element(self.error_message_login, "Login Error Message", screenshot=True)
        self.context.log.info("Login error message is displayed as expected.")
        self.context.add_step_log("Login error message is displayed as expected.")


    def verify_user_logged_in(self, expected_title: str):
        """Verify user is logged in by checking page title."""
        self.verify_element_text(self.title, "Page Title", expected_title, screenshot=True)
        self.log.info(f"Verified user logged in - page title: {expected_title}")

    def click_logout_link(self):
        """Click on the account dropdown to access logout link."""
        self.click_element(self.account_dropdown, "Account Dropdown", screenshot=True)
        self.log.info("Clicked on account dropdown to logout")

    def verify_logout_successful(self):
        """Verify user is logged out by checking logout confirmation text."""
        self.wait_for_element(self.logout_confirmation_text, "Logout Confirmation Text", screenshot=True)
        self.log.info("Verified logout successful - Account Logout text displayed")

    def click_continue_button(self):
        """Click continue button on logout page."""
        self.click_element(self.continue_button, "Continue Button", screenshot=True)
        self.log.info("Clicked continue button on logout page")

    def verify_home_page_after_logout(self):
        """Verify user is redirected to home page after logout by checking login/register link."""
        self.wait_for_element(self.login_register_link, "Login or Register Link", screenshot=True)
        self.log.info("Verified home page displayed after logout - Login or register link visible")