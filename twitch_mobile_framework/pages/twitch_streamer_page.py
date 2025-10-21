"""
Twitch streamer page object
"""
import time
from selenium.webdriver.common.by import By
from core.base_page import BaseMobilePage


class TwitchStreamerPage(BaseMobilePage):
    """Twitch streamer page object"""
    
    # Locators
    STREAMER_INFO = (By.CSS_SELECTOR, "[data-a-target='stream-info']")
    VIDEO_PLAYER = (By.CSS_SELECTOR, "[data-a-target='player']")
    STREAM_TITLE = (By.CSS_SELECTOR, "[data-a-target='stream-title']")
    STREAMER_NAME = (By.CSS_SELECTOR, "[data-a-target='streamer-name']")
    VIEWER_COUNT = (By.CSS_SELECTOR, "[data-a-target='viewer-count']")
    
    # Page elements
    PAGE_CONTENT = (By.CSS_SELECTOR, "[data-a-target='stream-page']")
    CHAT_SECTION = (By.CSS_SELECTOR, "[data-a-target='chat']")
    
    # Loading indicators
    LOADING_SPINNER = (By.CSS_SELECTOR, "[data-a-target='loading-spinner']")
    VIDEO_LOADING = (By.CSS_SELECTOR, "[data-a-target='video-loading']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def wait_for_page_to_load(self, timeout: int = 30) -> bool:
        """Wait for the streamer page to fully load"""
        print("Waiting for streamer page to load...")
        
        # Wait for page to be ready
        self.wait_for_page_load(timeout)
        
        # Handle any modals or popups that might appear
        self.handle_modal_or_popup()
        
        # Wait for key elements to be present
        try:
            # Wait for either stream info or video player to be visible
            WebDriverWait(self.driver, timeout).until(
                lambda driver: (
                    self.is_element_visible(self.STREAMER_INFO) or
                    self.is_element_visible(self.VIDEO_PLAYER) or
                    self.is_element_visible(self.PAGE_CONTENT)
                )
            )
            
            # Additional wait for video to start loading
            time.sleep(5)
            
            # Check if video is loading and wait for it
            if self.is_element_visible(self.VIDEO_LOADING):
                print("Video is loading, waiting for it to complete...")
                self.wait_for_element_to_disappear(self.VIDEO_LOADING)
            
            # Final wait to ensure everything is loaded
            time.sleep(3)
            
            print("Streamer page loaded successfully")
            return True
            
        except TimeoutException:
            print("Timeout waiting for streamer page to load")
            return False
    
    def is_streamer_page_loaded(self) -> bool:
        """Check if streamer page is loaded"""
        return (
            self.is_element_visible(self.STREAMER_INFO) or
            self.is_element_visible(self.VIDEO_PLAYER) or
            self.is_element_visible(self.PAGE_CONTENT)
        )
    
    def get_streamer_name(self) -> str:
        """Get the streamer's name"""
        try:
            return self.get_text(self.STREAMER_NAME)
        except:
            return "Unknown Streamer"
    
    def get_stream_title(self) -> str:
        """Get the stream title"""
        try:
            return self.get_text(self.STREAM_TITLE)
        except:
            return "Unknown Title"
    
    def get_viewer_count(self) -> str:
        """Get the viewer count"""
        try:
            return self.get_text(self.VIEWER_COUNT)
        except:
            return "Unknown"
    
    def take_streamer_screenshot(self, filename: str = "streamer_page") -> str:
        """Take a screenshot of the streamer page"""
        # Ensure page is fully loaded before taking screenshot
        self.wait_for_page_to_load()
        
        # Take screenshot
        screenshot_path = self.take_screenshot(filename)
        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def handle_video_modal(self) -> bool:
        """Handle video-related modals or popups"""
        # Common video modal selectors
        video_modal_selectors = [
            (By.CSS_SELECTOR, "[data-a-target='video-modal']"),
            (By.CSS_SELECTOR, ".video-modal"),
            (By.CSS_SELECTOR, "[data-a-target='player-modal']"),
            (By.CSS_SELECTOR, ".player-overlay"),
            (By.CSS_SELECTOR, "[data-a-target='age-gate']"),
            (By.CSS_SELECTOR, ".age-gate-modal")
        ]
        
        # Common modal close buttons
        close_selectors = [
            (By.CSS_SELECTOR, "[data-a-target='modal-close']"),
            (By.CSS_SELECTOR, ".modal-close"),
            (By.CSS_SELECTOR, "[aria-label='Close']"),
            (By.CSS_SELECTOR, "button[aria-label*='close']"),
            (By.CSS_SELECTOR, "[data-a-target='age-gate-confirm']"),
            (By.CSS_SELECTOR, ".age-gate-confirm")
        ]
        
        # Check for video modals
        for modal_selector in video_modal_selectors:
            if self.is_element_visible(modal_selector):
                print(f"Video modal detected: {modal_selector}")
                
                # Try to close the modal
                for close_selector in close_selectors:
                    if self.is_element_visible(close_selector):
                        try:
                            self.click_element(close_selector)
                            print(f"Video modal closed using: {close_selector}")
                            time.sleep(2)
                            return True
                        except Exception as e:
                            print(f"Failed to close video modal with {close_selector}: {e}")
                            continue
        
        return False
