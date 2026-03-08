from pages.base_page import BasePage
from playwright.sync_api import Page

class HomePage(BasePage):
    def __init__(self, page: Page, context):
        super().__init__(page, context)
        self.login_link = page.get_by_role("link", name="Login or register")


    def launch_application(self):
        """
        Launch the application by navigating to the base URL defined in the configuration.
        This method uses the open_application method from the BasePage class to navigate to the URL and takes a screenshot for reporting purposes.
        """
        self.open_application(self.context.cfg['base_url'], screenshot=True)


    def click_login_link(self):
        """
        Click on the login link on the home page. This method uses the click_element method from the BasePage class to perform the click action and takes a screenshot for reporting purposes.
        """
        self.click_element(self.login_link, "Login Link", screenshot=True)


    

