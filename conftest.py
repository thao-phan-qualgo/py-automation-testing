# conftest.py
import pytest
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from config.settings import (
    BROWSER, 
    HEADLESS, 
    PORTAL_BASE_URL,
    DEBUG,
    SLOW_MO,
    TRACE,
    DEFAULT_TIMEOUT,
    SCREENSHOT_ON_FAILURE,
    SCREENSHOT_DIR,
    VIDEO_ON_FAILURE,
    VIDEO_DIR
)

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Launch browser with debug configuration"""
    launch_options = {
        "headless": HEADLESS,
        "slow_mo": SLOW_MO if DEBUG else 0
    }
    
    # Add debug arguments
    if DEBUG:
        launch_options["args"] = [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage"
        ]
    
    if BROWSER == "chromium":
        browser = playwright_instance.chromium.launch(**launch_options)
    elif BROWSER == "firefox":
        browser = playwright_instance.firefox.launch(**launch_options)
    elif BROWSER == "webkit":
        browser = playwright_instance.webkit.launch(**launch_options)
    else:
        raise ValueError(f"Unsupported browser: {BROWSER}")
    
    if DEBUG:
        print(f"\n🐛 DEBUG MODE ENABLED")
        print(f"   Browser: {BROWSER}")
        print(f"   Headless: {HEADLESS}")
        print(f"   Slow Motion: {SLOW_MO}ms")
        print(f"   Trace: {TRACE}\n")
    
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser, request):
    """Create page with debug and recording options"""
    # Context options
    context_options = {
        "viewport": {"width": 1280, "height": 920},
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    # Enable video recording if configured
    if VIDEO_ON_FAILURE:
        os.makedirs(VIDEO_DIR, exist_ok=True)
        context_options["record_video_dir"] = VIDEO_DIR
        context_options["record_video_size"] = {"width": 1280, "height": 920}
    
    context = browser.new_context(**context_options)
    
    # Start tracing if enabled
    if TRACE:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    page = context.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)
    
    # Enable console logging in debug mode
    if DEBUG:
        page.on("console", lambda msg: print(f"🖥️  Console [{msg.type}]: {msg.text}"))
        page.on("pageerror", lambda err: print(f"❌ Page Error: {err}"))
    
    yield page
    
    # Save trace on failure
    if TRACE and hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        trace_dir = "reports/traces"
        os.makedirs(trace_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace("::", "_")
        trace_path = f"{trace_dir}/{test_name}_{timestamp}.zip"
        context.tracing.stop(path=trace_path)
        print(f"📊 Trace saved: {trace_path}")
        print(f"   View with: playwright show-trace {trace_path}")
    elif TRACE:
        context.tracing.stop()
    
    context.close()

@pytest.fixture(scope="session")
def portal_base_url():
    return PORTAL_BASE_URL

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to add screenshots to pytest-html report on failures.
    """
    outcome = yield
    report = outcome.get_result()

    # We only care about test call phase (not setup/teardown) and failures
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page is not None:
            # Create screenshot dir
            screenshot_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            # Build filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = report.nodeid.replace("::", "_").replace("/", "_")
            filename = f"{test_name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            # Take screenshot
            page.screenshot(path=filepath, full_page=True)

            # Attach to pytest-html report
            if "pytest_html" in item.config.pluginmanager.list_name_plugin():
                extra = getattr(report, "extra", [])
                from pytest_html import extras

                extra.append(extras.png(filepath, mime_type="image/png"))
                report.extra = extra
