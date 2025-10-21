"""
Base page class with common functionality for mobile web testing
"""
import os
import time
from typing import List, Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from config.settings import settings


class BaseMobilePage:
    """Base page class with common mobile web element interactions"""
    
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
        # Use JavaScript click for better mobile compatibility
        self.driver.execute_script("arguments[0].click();", element)
    
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
        if not os.path.exists(settings.screenshots_dir):
            os.makedirs(settings.screenshots_dir)
        
        filepath = os.path.join(settings.screenshots_dir, f"{filename}.png")
        self.driver.save_screenshot(filepath)
        return filepath
    
    def scroll_down(self, times: int = 1) -> None:
        """Scroll down the page"""
        for _ in range(times):
            # Get page height
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            current_position = self.driver.execute_script("return window.pageYOffset")
            
            # Scroll down by viewport height
            scroll_amount = settings.mobile_height
            new_position = min(current_position + scroll_amount, page_height - settings.mobile_height)
            
            self.driver.execute_script(f"window.scrollTo(0, {new_position});")
            time.sleep(1)  # Wait for content to load
    
    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
    
    def wait_for_url_contains(self, url_fragment: str) -> bool:
        """Wait for URL to contain specific text"""
        try:
            self.wait.until(EC.url_contains(url_fragment))
            return True
        except TimeoutException:
            return False
    
    def handle_modal_or_popup(self) -> bool:
        """Handle common modals and popups"""
        try:
            # Common modal/popup selectors for Twitch
            modal_selectors = [
                (By.CSS_SELECTOR, "[data-a-target='modal']"),
                (By.CSS_SELECTOR, ".modal"),
                (By.CSS_SELECTOR, "[role='dialog']"),
                (By.CSS_SELECTOR, ".popup"),
                (By.CSS_SELECTOR, "[data-testid='modal']"),
                (By.CSS_SELECTOR, ".overlay"),
                (By.CSS_SELECTOR, "[aria-modal='true']")
            ]
            
            # Common close button selectors
            close_selectors = [
                (By.CSS_SELECTOR, "[data-a-target='modal-close-button']"),
                (By.CSS_SELECTOR, ".modal-close"),
                (By.CSS_SELECTOR, "[aria-label='Close']"),
                (By.CSS_SELECTOR, ".close-button"),
                (By.CSS_SELECTOR, "[data-testid='close-button']"),
                (By.CSS_SELECTOR, "button[aria-label*='close']"),
                (By.CSS_SELECTOR, "button[aria-label*='Close']")
            ]
            
            # Check for modals and try to close them
            for modal_selector in modal_selectors:
                try:
                    if self.is_element_visible(modal_selector):
                        print(f"Modal detected: {modal_selector}")
                        
                        # Try to find and click close button
                        for close_selector in close_selectors:
                            try:
                                if self.is_element_visible(close_selector):
                                    self.click_element(close_selector)
                                    print(f"Modal closed using: {close_selector}")
                                    time.sleep(2)  # Wait for modal to disappear
                                    return True
                            except Exception as e:
                                print(f"Failed to close modal with {close_selector}: {e}")
                                continue
                        
                        # If no close button found, try pressing Escape
                        try:
                            from selenium.webdriver.common.keys import Keys
                            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                            print("Modal closed using Escape key")
                            time.sleep(2)
                            return True
                        except Exception as e:
                            print(f"Failed to close modal with Escape: {e}")
                except Exception as e:
                    print(f"Error checking modal {modal_selector}: {e}")
                    continue
            
            return False
        except Exception as e:
            print(f"Error in handle_modal_or_popup: {e}")
            return False
    
    def wait_for_page_load(self, timeout: int = 30) -> bool:
        """Wait for page to fully load"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False
