"""
Test cases for Twitch mobile web application
"""
import pytest
import allure
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_streamer_page import TwitchStreamerPage
from config.settings import settings


@allure.feature("Twitch Mobile")
@allure.story("Mobile Web Testing")
class TestTwitchMobile:
    """Test class for Twitch mobile web functionality"""
    
    @allure.title("Twitch Mobile Test - Search and Select Streamer")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.mobile
    @pytest.mark.twitch
    def test_twitch_mobile_search_and_select_streamer(self, driver, twitch_home_page, twitch_streamer_page):
        """
        Test case for Twitch mobile web application:
        1. Go to https://m.twitch.tv/
        2. Click in the search icon
        3. Input StarCraft II
        4. Scroll down 2 times
        5. Select one streamer
        6. On the streamer page wait until all is load and take a screenshot
        """
        
        with allure.step("1. Navigate to Twitch mobile home page"):
            twitch_home_page.navigate_to_twitch()
            assert twitch_home_page.is_home_page_loaded(), "Twitch home page should be loaded"
            allure.attach.file(
                twitch_home_page.take_screenshot("01_twitch_home_page"),
                name="Twitch Home Page",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("2. Click the search icon"):
            twitch_home_page.click_search_icon()
            allure.attach.file(
                twitch_home_page.take_screenshot("02_search_icon_clicked"),
                name="Search Icon Clicked",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("3. Input 'StarCraft II' in search"):
            twitch_home_page.search_for_term(settings.search_term)
            allure.attach.file(
                twitch_home_page.take_screenshot("03_search_input"),
                name="Search Input",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("4. Scroll down 2 times"):
            twitch_home_page.scroll_down_twice()
            allure.attach.file(
                twitch_home_page.take_screenshot("04_scrolled_down"),
                name="Scrolled Down",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("5. Select one streamer"):
            # Get current URL before clicking
            current_url = driver.current_url
            
            # Select first streamer
            twitch_home_page.select_first_streamer()
            
            # Wait for navigation to streamer page
            import time
            time.sleep(3)
            
            # Verify we navigated to a different page
            new_url = driver.current_url
            assert new_url != current_url, "Should navigate to streamer page"
            
            allure.attach.file(
                twitch_streamer_page.take_screenshot("05_streamer_selected"),
                name="Streamer Selected",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("6. Wait for streamer page to load and take screenshot"):
            # Wait for page to fully load
            assert twitch_streamer_page.wait_for_page_to_load(), "Streamer page should load completely"
            
            # Handle any modals or popups
            twitch_streamer_page.handle_modal_or_popup()
            twitch_streamer_page.handle_video_modal()
            
            # Take final screenshot
            final_screenshot = twitch_streamer_page.take_streamer_screenshot("06_streamer_page_final")
            
            # Attach screenshot to Allure report
            allure.attach.file(
                final_screenshot,
                name="Final Streamer Page Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            
            # Verify page is loaded
            assert twitch_streamer_page.is_streamer_page_loaded(), "Streamer page should be fully loaded"
            
            # Log streamer information
            streamer_name = twitch_streamer_page.get_streamer_name()
            stream_title = twitch_streamer_page.get_stream_title()
            viewer_count = twitch_streamer_page.get_viewer_count()
            
            allure.attach(
                f"Streamer: {streamer_name}\nTitle: {stream_title}\nViewers: {viewer_count}",
                name="Streamer Information",
                attachment_type=allure.attachment_type.TEXT
            )
            
            print(f"✅ Test completed successfully!")
            print(f"📺 Streamer: {streamer_name}")
            print(f"📝 Title: {stream_title}")
            print(f"👥 Viewers: {viewer_count}")
            print(f"📸 Screenshot: {final_screenshot}")
    
    @allure.title("Twitch Mobile Test - Handle Modals and Popups")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.twitch
    def test_handle_modals_and_popups(self, driver, twitch_home_page):
        """Test handling of modals and popups on Twitch mobile"""
        
        with allure.step("Navigate to Twitch and handle initial modals"):
            twitch_home_page.navigate_to_twitch()
            
            # Handle any modals that might appear
            modal_handled = twitch_home_page.handle_modal_or_popup()
            
            if modal_handled:
                allure.attach("Modal or popup was detected and handled", 
                            name="Modal Handling", 
                            attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach("No modals or popups detected", 
                            name="Modal Handling", 
                            attachment_type=allure.attachment_type.TEXT)
            
            assert twitch_home_page.is_home_page_loaded(), "Home page should be loaded after modal handling"
    
    @allure.title("Twitch Mobile Test - Search Functionality")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.twitch
    def test_search_functionality(self, driver, twitch_home_page):
        """Test search functionality on Twitch mobile"""
        
        with allure.step("Navigate to Twitch home page"):
            twitch_home_page.navigate_to_twitch()
            assert twitch_home_page.is_home_page_loaded(), "Home page should be loaded"
        
        with allure.step("Test search functionality"):
            twitch_home_page.search_for_term("StarCraft II")
            
            # Check if search results are present
            search_results = twitch_home_page.get_search_results()
            
            allure.attach(
                f"Found {len(search_results)} search results",
                name="Search Results",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Take screenshot of search results
            allure.attach.file(
                twitch_home_page.take_screenshot("search_results"),
                name="Search Results",
                attachment_type=allure.attachment_type.PNG
            )
