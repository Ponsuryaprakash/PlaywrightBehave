from behave import given, when, then
from features.custom_context import CustomContext


@when('user logins to the application with valid credentials "{username}" and "{password}"')
def step_impl(context: CustomContext, username, password):
    context.page_manager.get_login_page().login(username, password)


@then('the error message should be displayed on login page')
def step_impl(context: CustomContext):
    context.page_manager.get_login_page().verify_login_error_message()


@when('user logins to the application with invalid credentials "{username}" and "{password}"')
def step_impl(context: CustomContext, username, password):
    context.page_manager.get_login_page().login(username, password)


@when('user clicks on the logout link')
def step_impl(context: CustomContext):
    """Click on logout link from account dropdown."""
    context.page_manager.get_login_page().click_logout_link()


@then('verify user is logged out successfully')
def step_impl(context: CustomContext):
    """Verify logout confirmation is displayed."""
    context.page_manager.get_login_page().verify_logout_successful()


@when('user clicks on continue button on logout page')
def step_impl(context: CustomContext):
    """Click continue button after logout."""
    context.page_manager.get_login_page().click_continue_button()


@then('the user should be redirected to the home page')
def step_impl(context: CustomContext):
    """Verify user is redirected to home page after clicking continue."""
    context.page_manager.get_login_page().verify_home_page_after_logout()