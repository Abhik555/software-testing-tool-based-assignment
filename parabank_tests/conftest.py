import pytest
import os
from datetime import datetime
from utils.driver_factory import DriverFactory
from utils.screenshot_helper import take_screenshot

@pytest.fixture(scope="function")
def driver(request):
    driver_instance = DriverFactory.get_driver()
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()

# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()

#     # set a report attribute for each phase of a call, which can
#     # be "setup", "call", "teardown"
#     setattr(item, "rep_" + rep.when, rep)

# @pytest.fixture(scope="function", autouse=True)
# def check_test_result(request):
#     yield
#     # request.node is an "item" because we use the default
#     # "function" scope
#     if request.node.rep_call.failed:
#         try:
#             fixture_driver = request.node.funcargs.get('driver', None)
#             if fixture_driver:
#                 timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#                 take_screenshot(fixture_driver, f"{request.node.name}_{timestamp}")
#         except Exception as e:
#             print(f"Failed to capture screenshot: {e}")
