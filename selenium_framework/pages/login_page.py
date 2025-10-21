"""
Login page object for Sauce Demo application
"""
from selenium.webdriver.common.by import By
from core.base_page import BasePage
from config.settings import settings


class LoginPage(BasePage):
    """Login page object with all login-related elements and actions"""
    
    # Locators
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    LOGIN_CONTAINER = (By.CLASS_NAME, "login_container")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = settings.base_url
    
    def navigate_to_login(self) -> None:
        """Navigate to login page"""
        self.driver.get(self.url)
        self.wait_for_element_to_be_visible(self.LOGIN_CONTAINER)
    
    def enter_username(self, username: str) -> None:
        """Enter username in the username field"""
        self.send_keys(self.USERNAME_FIELD, username)
    
    def enter_password(self, password: str) -> None:
        """Enter password in the password field"""
        self.send_keys(self.PASSWORD_FIELD, password)
    
    def click_login_button(self) -> None:
        """Click the login button"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username: str = None, password: str = None) -> None:
        """Perform complete login action"""
        username = username or settings.username
        password = password or settings.password
        
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_error_message(self) -> str:
        """Get error message text if present"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_login_page_displayed(self) -> bool:
        """Check if login page is displayed"""
        return self.is_element_visible(self.LOGIN_CONTAINER)
    
    def clear_username_field(self) -> None:
        """Clear username field"""
        element = self.find_element(self.USERNAME_FIELD)
        element.clear()
    
    def clear_password_field(self) -> None:
        """Clear password field"""
        element = self.find_element(self.PASSWORD_FIELD)
        element.clear()
    
    def wait_for_element_to_be_visible(self, locator) -> bool:
        """Wait for element to be visible"""
        try:
            from selenium.webdriver.support import expected_conditions as EC
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
