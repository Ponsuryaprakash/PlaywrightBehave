import os
import json
import time
from datetime import datetime
import traceback
from behave import step
from playwright.sync_api import sync_playwright, BrowserContext, Page

from features.custom_context import CustomContext
from pages.page_manager import PageManager
from utils.config_loader import ConfigLoader
from utils.logger import get_logger
from utils.reporter import generate_html_report
from utils.report_helper_util import add_screenshot, add_step_log

log = get_logger("Environment")



def before_all(context: CustomContext):
    log.info("Loading configuration and initializing Playwright")
    context.cfg = ConfigLoader.get_config()
    context.playwright = sync_playwright().start()
    browser_type = os.getenv("BROWSER", "chromium")
    headless = os.getenv("HEADLESS", "False") == "True"
    if browser_type.lower() == "chromium":
        context.browser = context.playwright.chromium.launch(headless=headless)
    elif browser_type.lower() == "firefox":
        context.browser = context.playwright.firefox.launch(headless=headless)
    elif browser_type.lower() == "webkit":
        context.browser = context.playwright.webkit.launch(headless=headless)
    else:
        log.warning(f"Unknown BROWSER '{browser_type}', defaulting to chromium")
        context.browser = context.playwright.chromium.launch(headless=headless)
    
    # Initialize execution data tracking
    context.execution_data = {
        'start_time': datetime.now().isoformat(),
        'scenarios': []
    }
    
    #  initialize step_logs HERE
    context.step_logs = []
    context.step_screenshots = []

    # Add helper methods to context for logging and screenshots
    context.add_screenshot = lambda: add_screenshot(context)
    context.add_step_log = lambda message: add_step_log(context, message)


def before_scenario(context: CustomContext, scenario):
    context.scenario_start_time = time.time()
    context.browser_context = context.browser.new_context()
    context.browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.page = context.browser_context.new_page()
    context.page_manager = PageManager(context.page, context)
    log.info(f"Running scenario '{scenario.name}'")
    context.log = log
    
    # Track scenario execution time
    
    context.current_scenario = {
        "name": scenario.name,
        "tags": scenario.tags,
        "status": "",
        "steps": []
    }


       # Pre-register all steps as skipped
    for step in scenario.steps:
        context.current_scenario["steps"].append({
            "keyword": step.keyword,
            "name": step.name,
            "status": "skipped",
            "duration": 0,
            "events": [],
            "error_message": None,
            "stack_trace": None,
            "datatable": None
        })


def before_step(context: CustomContext, step):
    # Reset logs for this step
    context.step_events = []   # single ordered timeline
    context.step_start_time = time.time()

       # Find index of this step
    for i, s in enumerate(context.current_scenario["steps"]):
        if s["name"] == step.name:
            context.current_step_index = i
            break

def after_step(context: CustomContext, step):
        duration = round(time.time() - context.step_start_time, 3)
        datatable = None

        if step.table:
            datatable = {
                "headings": step.table.headings,
                "rows": [row.cells for row in step.table]
                }

        step_data = context.current_scenario["steps"][context.current_step_index]

        step_data["status"] = step.status.name
        step_data["duration"] = duration
        step_data["datatable"] = datatable
        step_data["events"] = context.step_events

        step_data = {
        "keyword": step.keyword,
        "name": step.name,
        "status": step.status.name,
        "datatable": datatable,
        "duration": duration,
        "events": context.step_events
    }

        if step.status.name in ["failed", "error"]:
            if step.exception:
                step_data["error_message"] = str(step.exception)
                step_data["stack_trace"] = traceback.format_exc()

            context.add_screenshot()


def after_scenario(context: CustomContext, scenario):
    scenario_duration = round(time.time() - context.scenario_start_time, 3)
    context.current_scenario["duration"] = scenario_duration

# Normalize status: treat "error" as "failed"
    raw_status = scenario.status.name

    if raw_status in ["failed", "error"]:
        normalized_status = "failed"
    else:
        normalized_status = raw_status

# If scenario failed (including error), save trace
    if normalized_status == "failed":
        log.error(f"Scenario '{scenario.name}' status: {raw_status}")
    
        sanitized_name = scenario.name.replace(" ", "_").replace(".", "_")
        trace_path = os.path.abspath(f"reports/traces/{sanitized_name}.zip")
        log.info(f"Saving trace to: {trace_path}")
    
        try:
            context.browser_context.tracing.stop(path=trace_path)
            log.info(f"Trace saved for scenario '{scenario.name}'")
        except Exception as e:
            log.error(f"Failed to save trace: {e}")
    else:
        try:
            context.browser_context.tracing.stop()
        except Exception as e:
            log.error(f"Failed to stop tracing: {e}")

# Store normalized status
    context.current_scenario["status"] = normalized_status
    context.execution_data["scenarios"].append(context.current_scenario)

    try:
        context.page_manager.reset_pages()  # Reset page objects for next scenario
        context.page.close()
        context.browser_context.close()
    except Exception as e:
        log.warning(f"Failed to close page or browser context: {e}")


def after_all(context):
    context.browser.close()
    context.playwright.stop()
    log.info("Playwright stopped and browser closed")
    log.info("Test execution completed")
    log.info("***********************************************************************")
    
    # Write execution data to JSON file
 
    context.execution_data['end_time'] = datetime.now().isoformat()
           # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)

    json_path = os.path.join("reports", "report.json")
    html_path = os.path.join("reports", "report.html")
    template_path = os.path.join("reports", "report_template.html")

    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(context.execution_data, f, indent=4)

    # Generate HTML
    generate_html_report(json_path, html_path, template_path)
