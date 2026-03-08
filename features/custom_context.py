from typing import Protocol, Dict, TYPE_CHECKING
from playwright.sync_api import Playwright, Browser, BrowserContext, Page
from pages.page_manager import PageManager


class CustomContext(Protocol):
    """
    CustomContext is a protocol that defines the structure for a custom context
    used in the Playwright framework. It includes the following attributes:

    - cfg (Dict[str, str]): A dictionary containing configuration settings.
    - playwright (Playwright): An instance of the Playwright class, which is used
        to control browser interactions.
    - browser (Browser): An instance of the Browser class, representing the
        browser being used for testing.
    - browser_context (BrowserContext): An instance of the BrowserContext class,
        which manages the context for the browser sessions.
    - page (Page): An instance of the Page class, representing a single tab or
        page in the browser.
    - log (object): An object for logging purposes, which can be used to capture
        and store log messages.
    - page_manager ("PageManager"): An instance of the PageManager class, which
        handles the management of pages within the context.

    This protocol is essential for ensuring that any class implementing it adheres
    to the expected structure and provides the necessary attributes for seamless
    integration with the Playwright framework.
    """
    cfg: Dict[str, str]
    playwright: Playwright
    browser: Browser
    browser_context: BrowserContext
    page: Page
    log: object
    page_manager: PageManager


