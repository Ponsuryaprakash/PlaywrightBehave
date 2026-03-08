from pages.base_page import BasePage
from playwright.sync_api import Page

class DashboardPage(BasePage):
    def __init__(self, page: Page, context):
        super().__init__(page, context)
        self.account_user_name = page.locator('span.subtext')


    def verify_logged_in_username(self, expected_username):
        """
        Verify the logged-in username is displayed on the dashboard page. This method waits for the account username element to be visible and checks if it contains the expected username.
        """
        self.wait_for_element(self.account_user_name, "Account User Name", screenshot=True)
        self.verify_element_text(self.account_user_name, "Logged in username verification", expected_username)


