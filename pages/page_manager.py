"""
Page Manager for managing page object creation and instances.

This module provides a centralized way to manage the creation and storage of page objects.
It follows the Singleton pattern to ensure that each page object is created only once
per test session and reused throughout the test execution.
"""

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage  
from utils.logger import get_logger
from playwright.sync_api import Page


class PageManager:
    """
    Manages the creation and lifecycle of page objects.
    
    This class ensures that page objects are created only once and provides
    easy access to them throughout the test execution.
    """
    
    def __init__(self, page: Page, context):
        """
        Initialize the PageManager with a Playwright page and test context.
        
        Args:
            page (Page): Playwright sync Page object
            context (CustomContext): Behave context object
        """
        self.page = page
        self.context = context
        self.log = get_logger(self.__class__.__name__)
        self._pages = {}
    
    def get_login_page(self):
        """
        Get or create the LoginPage object.
        
        Returns:
            LoginPage: An instance of the LoginPage class
        """
        if 'login_page' not in self._pages:
            self._pages['login_page'] = LoginPage(self.page, self.context)
            self.log.info("LoginPage object created")
        return self._pages['login_page']
    

    def get_home_page(self):
        """
        Get or create the HomePage object.
        
        Returns:
            HomePage: An instance of the HomePage class
        """
        if 'home_page' not in self._pages:
            self._pages['home_page'] = HomePage(self.page, self.context)
            self.log.info("HomePage object created")
        return self._pages['home_page']


    def get_dashboard_page(self):
        """
        Get or create the DashboardPage object.
        
        Returns:
            DashboardPage: An instance of the DashboardPage class
        """
        if 'dashboard_page' not in self._pages:
             # Import here to avoid circular imports
            self._pages['dashboard_page'] = DashboardPage(self.page, self.context)
            self.log.info("DashboardPage object created")
        return self._pages['dashboard_page']


    def reset_pages(self):
        """Reset all page objects."""
        self._pages = {}
        self.log.info("All page objects have been reset")
    

    
    def get_page(self, page_name):
        """
        Get a specific page object by name.
        
        Args:
            page_name (str): The name of the page to retrieve
            
        Returns:
            object: The requested page object or None if not found
        """
        return self._pages.get(page_name)


    

