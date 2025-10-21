"""
Test cases for login functionality
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@allure.feature("Login")
@allure.story("User Authentication")
class TestLogin:
    """Test class for login functionality"""
    
    @allure.title("Successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_successful_login(self, login_page, products_page):
        """Test successful login with valid credentials"""
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
            assert login_page.is_login_page_displayed(), "Login page should be displayed"
        
        with allure.step("Enter valid credentials"):
            login_page.login()
        
        with allure.step("Verify successful login"):
            assert products_page.is_products_page_displayed(), "Products page should be displayed after login"
            assert products_page.get_page_title() == "Products", "Page title should be 'Products'"
    
    @allure.title("Login with invalid username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_username(self, login_page):
        """Test login with invalid username"""
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
        
        with allure.step("Enter invalid username"):
            login_page.login(username="invalid_user", password="secret_sauce")
        
        with allure.step("Verify error message"):
            error_message = login_page.get_error_message()
            assert "Epic sadface: Username and password do not match" in error_message
            assert login_page.is_login_page_displayed(), "Should remain on login page"
    
    @allure.title("Login with invalid password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_password(self, login_page):
        """Test login with invalid password"""
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
        
        with allure.step("Enter invalid password"):
            login_page.login(username="standard_user", password="wrong_password")
        
        with allure.step("Verify error message"):
            error_message = login_page.get_error_message()
            assert "Epic sadface: Username and password do not match" in error_message
            assert login_page.is_login_page_displayed(), "Should remain on login page"
    
    @allure.title("Login with empty credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_credentials(self, login_page):
        """Test login with empty username and password"""
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
        
        with allure.step("Click login without entering credentials"):
            login_page.click_login_button()
        
        with allure.step("Verify error message"):
            error_message = login_page.get_error_message()
            assert "Epic sadface: Username is required" in error_message
            assert login_page.is_login_page_displayed(), "Should remain on login page"
    
    @allure.title("Login with empty username only")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_username(self, login_page):
        """Test login with empty username but valid password"""
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
        
        with allure.step("Enter only password"):
            login_page.enter_password("secret_sauce")
            login_page.click_login_button()
        
        with allure.step("Verify error message"):
            error_message = login_page.get_error_message()
            assert "Epic sadface: Username is required" in error_message
    
    @allure.title("Login with empty password only")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_password(self, login_page):
        """Test login with valid username but empty password"""
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
        
        with allure.step("Enter only username"):
            login_page.enter_username("standard_user")
            login_page.click_login_button()
        
        with allure.step("Verify error message"):
            error_message = login_page.get_error_message()
            assert "Epic sadface: Password is required" in error_message
    
    @allure.title("Login with locked out user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_locked_out_user(self, login_page):
        """Test login with locked out user credentials"""
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
        
        with allure.step("Enter locked out user credentials"):
            login_page.login(username="locked_out_user", password="secret_sauce")
        
        with allure.step("Verify error message"):
            error_message = login_page.get_error_message()
            assert "Epic sadface: Sorry, this user has been locked out" in error_message
            assert login_page.is_login_page_displayed(), "Should remain on login page"
    
    @allure.title("Login with performance glitch user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_performance_glitch_user(self, login_page, products_page):
        """Test login with performance glitch user (should work but be slow)"""
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
        
        with allure.step("Enter performance glitch user credentials"):
            login_page.login(username="performance_glitch_user", password="secret_sauce")
        
        with allure.step("Verify successful login despite performance issues"):
            assert products_page.is_products_page_displayed(), "Products page should be displayed"
            assert products_page.get_page_title() == "Products", "Page title should be 'Products'"
