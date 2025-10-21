"""
WebDriver management for Twitch Mobile tests with Chrome mobile emulation
"""
import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import settings


class MobileDriverManager:
    """Manages WebDriver instances with mobile emulation configuration"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Remote] = None
    
    def create_driver(self) -> webdriver.Remote:
        """Create and configure WebDriver instance with mobile emulation"""
        browser = settings.browser.lower()
        
        if browser == "chrome":
            self.driver = self._create_chrome_mobile_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        self._configure_driver()
        return self.driver
    
    def _create_chrome_mobile_driver(self) -> webdriver.Chrome:
        """Create Chrome WebDriver with mobile emulation"""
        options = ChromeOptions()
        
        # Mobile emulation settings
        if settings.mobile_emulation:
            mobile_emulation = {
                "deviceMetrics": {
                    "width": settings.mobile_width,
                    "height": settings.mobile_height,
                    "pixelRatio": 3.0
                },
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Additional Chrome options
        if settings.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Set window size for mobile viewport
        options.add_argument(f"--window-size={settings.mobile_width},{settings.mobile_height}")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _configure_driver(self):
        """Configure driver with timeouts and other settings"""
        self.driver.implicitly_wait(settings.implicit_wait)
        self.driver.set_page_load_timeout(settings.page_load_timeout)
        
        # Set mobile viewport size
        self.driver.set_window_size(settings.mobile_width, settings.mobile_height)
    
    def quit_driver(self):
        """Safely quit the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
