from behave import given, when, then
from features.custom_context import CustomContext


@given('the user is on the home page')
def step_given(context: CustomContext):
    """This step definition launches the application and navigates to the home page."""
    context.page_manager.get_home_page().launch_application()

@given('User clicks on the login link')
def step_when(context: CustomContext):
    context.page_manager.get_home_page().click_login_link()