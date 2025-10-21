"""
Pytest configuration and fixtures for Selenium tests
"""
import pytest
import allure
from core.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@pytest.fixture(scope="function")
def driver():
    """Create and manage WebDriver instance"""
    driver_manager = DriverManager()
    driver = driver_manager.create_driver()
    
    yield driver
    
    # Cleanup
    driver_manager.quit_driver()


@pytest.fixture(scope="function")
def login_page(driver):
    """Create LoginPage instance"""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def products_page(driver):
    """Create ProductsPage instance"""
    return ProductsPage(driver)


@pytest.fixture(scope="function")
def logged_in_user(login_page, products_page):
    """Fixture that provides a logged-in user session"""
    login_page.navigate_to_login()
    login_page.login()
    
    # Verify login was successful
    assert products_page.is_products_page_displayed(), "Login failed - products page not displayed"
    
    return login_page, products_page


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
                screenshot_path = f"screenshots/failure_{item.name}_{rep.when}.png"
                driver.save_screenshot(screenshot_path)
                allure.attach.file(screenshot_path, name="Screenshot on Failure", 
                                 attachment_type=allure.attachment_type.PNG)
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
        "markers", "slow: mark test as slow running"
    )
