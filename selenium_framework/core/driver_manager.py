"""
WebDriver management for Selenium tests
"""
import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from config.settings import settings


class DriverManager:
    """Manages WebDriver instances with proper configuration"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Remote] = None
    
    def create_driver(self) -> webdriver.Remote:
        """Create and configure WebDriver instance"""
        browser = settings.browser.lower()
        
        if browser == "chrome":
            self.driver = self._create_chrome_driver()
        elif browser == "firefox":
            self.driver = self._create_firefox_driver()
        elif browser == "edge":
            self.driver = self._create_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        self._configure_driver()
        return self.driver
    
    def _create_chrome_driver(self) -> webdriver.Chrome:
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        
        if settings.headless:
            options.add_argument("--headless")
        
        options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _create_firefox_driver(self) -> webdriver.Firefox:
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if settings.headless:
            options.add_argument("--headless")
        
        options.add_argument(f"--width={settings.window_width}")
        options.add_argument(f"--height={settings.window_height}")
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _create_edge_driver(self) -> webdriver.Edge:
        """Create Edge WebDriver"""
        options = EdgeOptions()
        
        if settings.headless:
            options.add_argument("--headless")
        
        options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def _configure_driver(self):
        """Configure driver with timeouts and other settings"""
        self.driver.implicitly_wait(settings.implicit_wait)
        self.driver.set_page_load_timeout(settings.page_load_timeout)
        self.driver.maximize_window()
    
    def quit_driver(self):
        """Safely quit the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
