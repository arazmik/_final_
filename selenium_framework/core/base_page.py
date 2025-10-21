"""
Base page class with common functionality for all page objects
"""
import os
from typing import List, Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import settings


class BasePage:
    """Base page class with common web element interactions"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.explicit_wait)
    
    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """Find a single element with explicit wait"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise NoSuchElementException(f"Element not found: {locator}")
    
    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Find multiple elements"""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
    
    def click_element(self, locator: Tuple[str, str]) -> None:
        """Click an element with explicit wait"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys(self, locator: Tuple[str, str], text: str) -> None:
        """Send keys to an element"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Get text from an element"""
        element = self.find_element(locator)
        return element.text
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if element is present"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """Check if element is visible"""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except TimeoutException:
            return False
    
    def wait_for_element_to_disappear(self, locator: Tuple[str, str]) -> bool:
        """Wait for element to disappear"""
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """Get attribute value from element"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def take_screenshot(self, filename: str) -> str:
        """Take screenshot and return file path"""
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        filepath = os.path.join("screenshots", f"{filename}.png")
        self.driver.save_screenshot(filepath)
        return filepath
    
    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def wait_for_url_contains(self, url_fragment: str) -> bool:
        """Wait for URL to contain specific text"""
        try:
            self.wait.until(EC.url_contains(url_fragment))
            return True
        except TimeoutException:
            return False
