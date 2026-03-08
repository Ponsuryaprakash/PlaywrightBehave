from playwright.sync_api import Locator, Page
from utils.logger import get_logger



class BasePage:
    def __init__(self, page: Page, context):
        """
        Initialize BasePage with page and context.

        Args:
            page (Page): Playwright page object.
            context (CustomContext, optional): Test context for logging and screenshots.
        """
        self.page = page
        self.context = context
        self.log = get_logger(self.__class__.__name__)


    def _get_locator(self, selector_or_locator):
        """
        Get a Locator object from selector string or return existing Locator.

        Args:
            selector_or_locator (str | Locator): Selector string or Locator object.

        Returns:
            Locator: Locator object.
        """
        return (
            selector_or_locator
            if isinstance(selector_or_locator, Locator)
            else self.page.locator(selector_or_locator)
        )


    def open_application(self, url, screenshot=None):
        """
        Open the application URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.log.info(f"Navigating to URL: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        if screenshot:
            self.context.add_screenshot()
        self.context.add_step_log(f"Opened application at URL: {url}")

    def click_element(self, selector, field_name, screenshot=None, timeout=None):
        """
        Click an element on the page.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(
                f"Clicking element '{field_name}' using selector '{selector}' "
                f"with timeout={timeout}"
            )

            if timeout:
                locator.click(timeout=timeout)
            else:
                locator.click()

            self.log.info(f"Successfully clicked '{field_name}'")

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Clicked on '{field_name}'")

        except Exception as e:
            self.log.error(
                f"Failed to click '{field_name}' using selector '{selector}'. "
                f"Error: {str(e)}"
            )
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed to click on '{field_name}'")
            raise Exception(f"Failed to click element '{field_name}': {str(e)}")

   


    def enter_text(self, selector, text, field_name, screenshot=None, timeout=None):
        """
        Enter text into an input field.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            text (str): Text value to enter.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(
                f"Entering text into '{field_name}' using selector '{selector}' "
                f"with timeout={timeout}. Value='{text}'"
            )

            if timeout:
                locator.fill(text, timeout=timeout)
            else:
                locator.fill(text)

            self.log.info(f"Successfully entered text into '{field_name}'")

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Entered text '{text}' into '{field_name}'")

        except Exception as e:
            self.log.error(
                f"Failed to enter text into '{field_name}' "
                f"using selector '{selector}'. Error: {str(e)}"
            )
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed to enter text into '{field_name}'")
            raise Exception(f"Failed to enter text into '{field_name}': {str(e)}")


    def get_text(self, selector, field_name, screenshot=None, timeout=None):
        """
        Get text content from an element.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.

        Returns:
            str: Text content from the element.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(f"Getting text from '{field_name}'")
            text = (
                locator.inner_text(timeout=timeout)
                if timeout
                else locator.inner_text()
            )

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Retrieved text from '{field_name}' → {text}")
            return text

        except Exception as e:
            self.log.error(f"Failed to get text from '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed to get text from '{field_name}'")
            raise Exception(f"Failed to get text from '{field_name}': {str(e)}")



    def wait_for_element(
        self, selector, field_name, screenshot=None, timeout=None, state="visible"
    ):
        """
        Wait for an element to reach a specific state.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
            state (str, optional): State to wait for ('visible', 'hidden', 'attached', 'detached'). Defaults to 'visible'.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(f"Waiting for '{field_name}' to be {state}")
            if timeout:
                locator.wait_for(state=state, timeout=timeout)
            else:
                locator.wait_for(state=state)

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Waited for '{field_name}'")

        except Exception as e:
            self.log.error(f"Failed waiting for '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Wait failed for '{field_name}'")
            raise Exception(f"Failed waiting for element '{field_name}': {str(e)}")



    def double_click(self, selector, field_name, screenshot=None, timeout=None):
        """
        Double click an element.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(f"Double clicking '{field_name}'")
            if timeout:
                locator.dblclick(timeout=timeout)
            else:
                locator.dblclick()

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Double clicked '{field_name}'")

        except Exception as e:
            self.log.error(f"Failed to double click '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed to double click '{field_name}'")
            raise Exception(f"Failed to double click element '{field_name}': {str(e)}")



    def hover(self, selector, field_name, screenshot=None, timeout=None):
        """
        Hover over an element.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
        """
        locator = self._get_locator(selector)

        try:
            locator.wait_for(state='visible')
            self.log.info(f"Hovering over '{field_name}'")
            if timeout:
                locator.hover(timeout=timeout)
            else:
                locator.hover()

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Hovered over '{field_name}'")

        except Exception as e:
            self.log.error(f"Failed to hover '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed to hover '{field_name}'")
            raise Exception(f"Failed to hover element '{field_name}': {str(e)}")



    def is_visible(self, selector, field_name, screenshot=None, timeout=None):
        """
        Check if an element is visible.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.

        Returns:
            bool: True if element is visible, False otherwise.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(f"Checking visibility of '{field_name}'")
            visible = (
                locator.is_visible(timeout=timeout)
                if timeout
                else locator.is_visible()
            )

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Visibility of '{field_name}' → {visible}")
            return visible

        except Exception as e:
            self.log.error(f"Visibility check failed for '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Visibility check failed for '{field_name}'")
            raise Exception(f"Failed to check visibility of '{field_name}': {str(e)}")



    def get_attribute(self, selector, field_name, attribute_name, screenshot=None, timeout=None):
        """
        Get an attribute value from an element.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            attribute_name (str): Name of the attribute to retrieve.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.

        Returns:
            str: Attribute value.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(
                f"Getting attribute '{attribute_name}' from '{field_name}'"
            )
            value = (
                locator.get_attribute(attribute_name, timeout=timeout)
                if timeout
                else locator.get_attribute(attribute_name)
            )

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(
                f"Attribute '{attribute_name}' of '{field_name}' → {value}"
            )
            return value

        except Exception as e:
            self.log.error(
                f"Failed getting attribute from '{field_name}': {str(e)}"
            )
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed getting attribute from '{field_name}'")
            raise Exception(
                f"Failed to get attribute '{attribute_name}' from '{field_name}': {str(e)}"
            )    
        

    def check_checkbox(self, selector, field_name, screenshot=None, timeout=None):
        """
        Check a checkbox element.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(f"Checking checkbox '{field_name}'")

            if timeout:
                locator.check(timeout=timeout)
            else:
                locator.check()

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Checked checkbox '{field_name}'")

        except Exception as e:
            self.log.error(f"Failed to check checkbox '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed to check checkbox '{field_name}'")
            raise Exception(f"Failed to check checkbox '{field_name}': {str(e)}")


    def uncheck_checkbox(self, selector, field_name, screenshot=None, timeout=None):
        """
        Uncheck a checkbox element.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(f"Unchecking checkbox '{field_name}'")

            if timeout:
                locator.uncheck(timeout=timeout)
            else:
                locator.uncheck()

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Unchecked checkbox '{field_name}'")

        except Exception as e:
            self.log.error(f"Failed to uncheck checkbox '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed to uncheck checkbox '{field_name}'")
            raise Exception(f"Failed to uncheck checkbox '{field_name}': {str(e)}")
    
    def select_radio_option(self, selector, field_name, screenshot=None, timeout=None):
        """
        Select a radio button option.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(f"Selecting radio option '{field_name}'")

            if timeout:
                locator.check(timeout=timeout)
            else:
                locator.check()

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(f"Selected radio option '{field_name}'")

        except Exception as e:
            self.log.error(f"Failed to select radio option '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed to select radio option '{field_name}'")
            raise Exception(f"Failed to select radio option '{field_name}': {str(e)}")  
    
    def select_dropdown_by_value(self, selector, field_name, value, screenshot=None, timeout=None):
        """
        Select an option from a dropdown by value.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            value (str): Value of the option to select.
            screenshot (bool, optional): Take screenshot after success.
            timeout (int, optional): Timeout in milliseconds.
        """
        locator = self._get_locator(selector)

        try:
            self.log.info(
                f"Selecting value '{value}' from dropdown '{field_name}'"
            )

            if timeout:
                locator.select_option(value=value, timeout=timeout)
            else:
                locator.select_option(value=value)

            if screenshot:
                self.context.add_screenshot()

            self.context.add_step_log(
                f"Selected value '{value}' from dropdown '{field_name}'"
            )

        except Exception as e:
            self.log.error(f"Dropdown selection failed for '{field_name}': {str(e)}")
            self.context.add_screenshot()
            self.context.add_step_log(f"Failed selecting from dropdown '{field_name}'")
            raise Exception(
                f"Failed to select value '{value}' from dropdown '{field_name}': {str(e)}"
            )
        
    
    def verify_element_text(self, selector, field_name, expected_text, screenshot=None, timeout=None):
        """
        Verify that an element's text matches the expected value.

        Args:
            selector (str | Locator): Selector string or Locator.
            field_name (str): Logical name for logging/reporting.
            expected_text (str): The expected text to verify against.
            screenshot (bool, optional): Take screenshot after verification.
            timeout (int, optional): Timeout in milliseconds.

        Raises:
            AssertionError: If the actual text does not match the expected text.
        """
        actual_text = self.get_text(selector, field_name, screenshot=False, timeout=timeout)

        if actual_text.strip() == expected_text.strip():
            self.log.info(f"Text verification passed for '{field_name} → Expected: '{expected_text}', Actual: '{actual_text}'")
            self.context.add_step_log(f"Verified text of '{field_name}' matches expected value → '{expected_text}'")
            if screenshot:
                self.context.add_screenshot()
        else:
            self.log.error(
                f"Text verification failed for '{field_name}'. "
                f"Expected: '{expected_text}', Actual: '{actual_text}'"
            )
            self.context.add_step_log(
                f"Text verification failed for '{field_name}'. Expected: '{expected_text}', Actual: '{actual_text}'"
            )
            self.context.add_screenshot()
            raise AssertionError(
                f"Text verification failed for '{field_name}'. Expected: '{expected_text}', Actual: '{actual_text}'"
            )