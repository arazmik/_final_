"""
Basic test case for Twitch mobile web application (no Allure dependencies)
"""
import pytest
import time
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_streamer_page import TwitchStreamerPage


class TestTwitchMobileBasic:
    """Basic test class for Twitch mobile web functionality"""
    
    def test_twitch_mobile_search_and_select_streamer(self, driver):
        """
        Test case for Twitch mobile web application:
        1. Go to https://m.twitch.tv/
        2. Click in the search icon
        3. Input StarCraft II
        4. Scroll down 2 times
        5. Select one streamer
        6. On the streamer page wait until all is load and take a screenshot
        """
        
        try:
            twitch_home_page = TwitchHomePage(driver)
            twitch_streamer_page = TwitchStreamerPage(driver)
                        
            print("🚀 Starting Twitch Mobile Test")
            
            # Step 1: Navigate to Twitch mobile home page
            print("1️⃣ Navigating to Twitch mobile home page...")
            twitch_home_page.navigate_to_twitch()
            assert "twitch.tv" in driver.current_url, "Should be on Twitch website"
            print("✅ Successfully navigated to Twitch mobile")
            
            # Step 2: Click the search icon
            print("2️⃣ Clicking the search icon...")
            twitch_home_page.click_search_icon()
            twitch_home_page.take_screenshot("02_search_icon_clicked")
            print("✅ Successfully clicked search icon")
            
            # Step 3: Input 'StarCraft II' in search field
            print("3️⃣ Inputting 'StarCraft II' in search field...")
            twitch_home_page.input_search_query("StarCraft II")
            twitch_home_page.take_screenshot("03_search_input")
            print("✅ Successfully entered search term")
            
            # Step 4: Scroll down 2 times
            print("4️⃣ Scrolling down 2 times...")
            twitch_home_page.scroll_down_n_times(2)
            twitch_home_page.take_screenshot("04_scrolled_down")
            print("✅ Successfully scrolled down 2 times")
            
            # Step 5: Select one streamer
            print("5️⃣ Selecting a streamer...")
            current_url = driver.current_url
            twitch_home_page.select_streamer()
            time.sleep(3)  # Wait for navigation
            new_url = driver.current_url
            assert new_url != current_url, "Should navigate to streamer page"
            twitch_home_page.take_screenshot("05_streamer_selected")
            print("✅ Successfully selected a streamer")
            
            # Step 6: Wait for streamer page to load and take screenshot
            print("6️⃣ Waiting for streamer page to load and taking screenshot...")
            time.sleep(5)  # Wait for page to load
            twitch_streamer_page.handle_streamer_modal()
            twitch_streamer_page.take_final_screenshot()
            
            # Take final screenshot
            final_screenshot = f"screenshots/06_streamer_page_final_{int(time.time())}.png"
            driver.save_screenshot(final_screenshot)
            
            print("✅ Successfully completed all test steps")
            print(f"📸 Final screenshot saved: {final_screenshot}")
            print("🎉 Test completed successfully!")
                
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            # Take a screenshot even if test fails
            try:
                driver.save_screenshot("screenshots/test_failure.png")
                print("📸 Failure screenshot saved")
            except:
                pass
            raise
