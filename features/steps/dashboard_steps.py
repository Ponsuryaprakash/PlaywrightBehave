from behave import given, when, then
from features.custom_context import CustomContext

@then('the username "{username}" should be displayed on dashboard page')
def step_then(context: CustomContext, username):
    context.page_manager.get_dashboard_page().verify_logged_in_username(username)