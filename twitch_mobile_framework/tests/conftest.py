"""
Pytest configuration and fixtures for Twitch Mobile tests
"""
import pytest
from core.driver_manager import MobileDriverManager
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_streamer_page import TwitchStreamerPage

try:
    import allure
except ImportError:
    allure = None


@pytest.fixture(scope="function")
def driver():
    """Create and manage WebDriver instance with mobile emulation"""
    driver_manager = MobileDriverManager()
    driver = driver_manager.create_driver()
    
    yield driver
    
    # Cleanup
    driver_manager.quit_driver()


@pytest.fixture(scope="function")
def twitch_home_page(driver):
    """Create TwitchHomePage instance"""
    return TwitchHomePage(driver)


@pytest.fixture(scope="function")
def twitch_streamer_page(driver):
    """Create TwitchStreamerPage instance"""
    return TwitchStreamerPage(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Get the driver from the test item
        if hasattr(item, "funcargs") and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            try:
                # Check if driver is still active
                if driver and hasattr(driver, 'current_url'):
                    screenshot_path = f"screenshots/failure_{item.name}_{rep.when}.png"
                    driver.save_screenshot(screenshot_path)
                if allure:
                    allure.attach.file(screenshot_path, name="Screenshot on Failure", 
                                     attachment_type=allure.attachment_type.PNG)
                else:
                    print("Driver not available for screenshot capture")
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "mobile: mark test as mobile specific test"
    )
    config.addinivalue_line(
        "markers", "twitch: mark test as Twitch specific test"
    )
