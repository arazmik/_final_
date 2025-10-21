"""
Simplified test case for Twitch mobile web application
"""
import pytest
import allure
import time
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_streamer_page import TwitchStreamerPage


@allure.feature("Twitch Mobile")
@allure.story("Mobile Web Testing")
class TestTwitchMobileSimple:
    """Simplified test class for Twitch mobile web functionality"""
    
    @allure.title("Twitch Mobile Test - Search and Select Streamer")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
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
            
            with allure.step("1. Navigate to Twitch mobile home page"):
                twitch_home_page.navigate_to_twitch()
                # Simple URL check instead of complex element validation
                assert "twitch.tv" in driver.current_url, "Should be on Twitch website"
                print("✅ Successfully navigated to Twitch mobile")
            
            with allure.step("2. Click the search icon"):
                twitch_home_page.click_search_icon()
                twitch_home_page.take_screenshot("02_search_icon_clicked")
                print("✅ Successfully clicked search icon")
            
            with allure.step("3. Input 'StarCraft II' in search field"):
                twitch_home_page.input_search_query("StarCraft II")
                twitch_home_page.take_screenshot("03_search_input")
                print("✅ Successfully entered search term")
            
            with allure.step("4. Scroll down 2 times"):
                twitch_home_page.scroll_down_n_times(2)
                twitch_home_page.take_screenshot("04_scrolled_down")
                print("✅ Successfully scrolled down 2 times")
            
            with allure.step("5. Select one streamer"):
                # Get current URL before clicking
                current_url = driver.current_url
                twitch_home_page.select_streamer()
                time.sleep(3)  # Wait for navigation
                new_url = driver.current_url
                assert new_url != current_url, "Should navigate to streamer page"
                twitch_home_page.take_screenshot("05_streamer_selected")
                print("✅ Successfully selected a streamer")
            
            with allure.step("6. Wait for streamer page to load and take screenshot"):
                # Wait for page to load
                time.sleep(5)
                twitch_streamer_page.handle_streamer_modal()
                twitch_streamer_page.take_final_screenshot()
                
                # Take final screenshot
                final_screenshot = f"screenshots/06_streamer_page_final_{int(time.time())}.png"
                driver.save_screenshot(final_screenshot)
                
                # Attach screenshot to Allure report
                try:
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name="Final Streamer Page Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    print(f"Could not attach screenshot to Allure: {e}")
                
                print("✅ Successfully completed all test steps")
                print(f"📸 Final screenshot saved: {final_screenshot}")
                
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            # Take a screenshot even if test fails
            try:
                driver.save_screenshot("screenshots/test_failure.png")
                print("📸 Failure screenshot saved")
            except:
                pass
            raise
