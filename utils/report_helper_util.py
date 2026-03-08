"""
Helper utilities for screenshot and logging functionality.
"""

import base64
import time


def add_screenshot(context):
    """
    Capture a screenshot and add it to step events with timestamp.

    Args:
        context: Behave context object containing page and step tracking data.
    """
    screenshot_bytes = context.page.screenshot()
    screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
    context.step_events.append(
        {
            "type": "screenshot",
            "timestamp": round(time.time() - context.step_start_time, 3),
            "data": screenshot_base64,
        }
    )


def add_step_log(context, message):
    """
    Add a log message to step events with timestamp.

    Args:
        context: Behave context object containing step tracking data.
        message: Log message to add.
    """
    context.step_events.append(
        {
            "type": "log",
            "timestamp": round(time.time() - context.step_start_time, 3),
            "message": str(message),
        }
    )
