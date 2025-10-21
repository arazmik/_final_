"""
Twitch mobile home page object
"""
import time
from selenium.webdriver.common.by import By
from core.base_page import BaseMobilePage
from config.settings import settings


class TwitchHomePage(BaseMobilePage):
    """Twitch mobile home page object"""
    
    # Locators
    # SEARCH_ICON = (By.CSS_SELECTOR, "[data-a-target='search-button']")
    # SEARCH_INPUT = (By.CSS_SELECTOR, "input[data-a-target='search-input']")
    # SEARCH_SUGGESTIONS = (By.CSS_SELECTOR, "[data-a-target='search-suggestions']")
    # SEARCH_RESULTS = (By.CSS_SELECTOR, "[data-a-target='search-results']")
    SEARCH_ICON = (By.XPATH, "//div[contains(text(),'Browse')]")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search']")
    SEARCH_SUGGESTIONS = (By.XPATH, "//div[contains(text(),'StarCraft II')]")
    SEARCH_RESULTS = (By.XPATH, "//div[contains(text(),'StarCraft II')] ")
    
    # Navigation elements
    NAVIGATION = (By.CSS_SELECTOR, "[data-a-target='navigation']")
    MAIN_CONTENT = (By.CSS_SELECTOR, "[data-a-target='main-content']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = settings.base_url
    
    def navigate_to_twitch(self) -> None:
        """Navigate to Twitch mobile home page"""
        self.driver.get(self.url)
        # self.driver.get(settings.search_page_url)
        self.wait_for_page_load()
        
        # Handle any initial modals/popups
        self.handle_modal_or_popup()
    
    def click_search_icon(self) -> None:
        """Click the search icon"""
        self.click_element(self.SEARCH_ICON)
        time.sleep(2)  # Wait for search interface to load
    
    def search_for_term(self, search_term: str) -> None:
        """Search for a specific term"""
        # Click search icon first
        self.click_search_icon()
        
        # Enter search term
        self.send_keys(self.SEARCH_INPUT, search_term)
        time.sleep(2)  # Wait for search suggestions/results
    
    def get_search_results(self) -> list:
        """Get list of search result elements"""
        # Wait for search results to appear
        if self.is_element_visible(self.SEARCH_RESULTS):
            return self.find_elements(self.SEARCH_RESULTS)
        return []
    
    def scroll_down_twice(self) -> None:
        """Scroll down the page 2 times"""
        self.scroll_down(2)
    
    def select_first_streamer(self) -> None:
        """Select the first available streamer from search results"""
        # Look for streamer links in search results
        streamer_selectors = [
            (By.CSS_SELECTOR, "[data-a-target='search-result'] a"),
            (By.CSS_SELECTOR, "[data-a-target='search-suggestion'] a"),
            (By.CSS_SELECTOR, ".search-result a"),
            (By.CSS_SELECTOR, ".search-suggestion a"),
            (By.CSS_SELECTOR, "a[href*='/']")  # Generic link selector
        ]
        
        for selector in streamer_selectors:
            elements = self.find_elements(selector)
            if elements:
                # Click the first streamer link
                self.driver.execute_script("arguments[0].click();", elements[0])
                break
    
    def is_home_page_loaded(self) -> bool:
        """Check if home page is loaded"""
        return self.is_element_visible(self.NAVIGATION) or self.is_element_visible(self.MAIN_CONTENT)
