"""
Test cases for products page functionality
"""
import pytest
import allure
from pages.products_page import ProductsPage


@allure.feature("Products")
@allure.story("Product Management")
class TestProducts:
    """Test class for products page functionality"""
    
    @allure.title("Verify products page elements")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_products_page_elements(self, logged_in_user):
        """Test that all essential elements are present on products page"""
        login_page, products_page = logged_in_user
        
        with allure.step("Verify page title"):
            assert products_page.get_page_title() == "Products", "Page title should be 'Products'"
        
        with allure.step("Verify products are displayed"):
            product_count = products_page.get_product_count()
            assert product_count > 0, f"Should have products displayed, found {product_count}"
        
        with allure.step("Verify product names are present"):
            product_names = products_page.get_all_product_names()
            assert len(product_names) > 0, "Product names should be displayed"
            assert all(name.strip() for name in product_names), "Product names should not be empty"
        
        with allure.step("Verify product prices are present"):
            product_prices = products_page.get_all_product_prices()
            assert len(product_prices) > 0, "Product prices should be displayed"
            assert all(price.strip() for price in product_prices), "Product prices should not be empty"
    
    @allure.title("Add single product to cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_single_product_to_cart(self, logged_in_user):
        """Test adding a single product to cart"""
        login_page, products_page = logged_in_user
        
        with allure.step("Verify initial cart is empty"):
            initial_count = products_page.get_cart_item_count()
            assert initial_count == 0, f"Cart should be empty initially, found {initial_count} items"
        
        with allure.step("Add first product to cart"):
            products_page.add_product_to_cart(0)
        
        with allure.step("Verify product was added to cart"):
            cart_count = products_page.get_cart_item_count()
            assert cart_count == 1, f"Cart should have 1 item, found {cart_count}"
    
    @allure.title("Add multiple products to cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_multiple_products_to_cart(self, logged_in_user):
        """Test adding multiple products to cart"""
        login_page, products_page = logged_in_user
        
        with allure.step("Add multiple products to cart"):
            products_page.add_product_to_cart(0)  # Add first product
            products_page.add_product_to_cart(1)  # Add second product
            products_page.add_product_to_cart(2)  # Add third product
        
        with allure.step("Verify all products were added"):
            cart_count = products_page.get_cart_item_count()
            assert cart_count == 3, f"Cart should have 3 items, found {cart_count}"
    
    @allure.title("Add and remove product from cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_and_remove_product_from_cart(self, logged_in_user):
        """Test adding and then removing a product from cart"""
        login_page, products_page = logged_in_user
        
        with allure.step("Add product to cart"):
            products_page.add_product_to_cart(0)
            cart_count = products_page.get_cart_item_count()
            assert cart_count == 1, "Product should be added to cart"
        
        with allure.step("Remove product from cart"):
            products_page.remove_product_from_cart(0)
            cart_count = products_page.get_cart_item_count()
            assert cart_count == 0, "Cart should be empty after removing product"
    
    @allure.title("Test product sorting functionality")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_sorting(self, logged_in_user):
        """Test product sorting functionality"""
        login_page, products_page = logged_in_user
        
        with allure.step("Get initial product order"):
            initial_names = products_page.get_all_product_names()
            initial_prices = products_page.get_all_product_prices()
        
        with allure.step("Sort products by name A to Z"):
            products_page.sort_products("az")
            sorted_names_az = products_page.get_all_product_names()
            assert sorted_names_az == sorted(initial_names), "Products should be sorted A to Z"
        
        with allure.step("Sort products by name Z to A"):
            products_page.sort_products("za")
            sorted_names_za = products_page.get_all_product_names()
            assert sorted_names_za == sorted(initial_names, reverse=True), "Products should be sorted Z to A"
        
        with allure.step("Sort products by price low to high"):
            products_page.sort_products("lohi")
            sorted_prices_lohi = products_page.get_all_product_prices()
            # Convert prices to float for comparison
            price_values = [float(price.replace('$', '')) for price in sorted_prices_lohi]
            assert price_values == sorted(price_values), "Products should be sorted by price low to high"
        
        with allure.step("Sort products by price high to low"):
            products_page.sort_products("hilo")
            sorted_prices_hilo = products_page.get_all_product_prices()
            # Convert prices to float for comparison
            price_values = [float(price.replace('$', '')) for price in sorted_prices_hilo]
            assert price_values == sorted(price_values, reverse=True), "Products should be sorted by price high to low"
    
    @allure.title("Test shopping cart navigation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_shopping_cart_navigation(self, logged_in_user):
        """Test navigation to shopping cart"""
        login_page, products_page = logged_in_user
        
        with allure.step("Add product to cart"):
            products_page.add_product_to_cart(0)
        
        with allure.step("Click shopping cart"):
            products_page.click_shopping_cart()
        
        with allure.step("Verify navigation to cart page"):
            # This would typically verify cart page elements
            # For demo purposes, we'll just verify URL change
            assert "cart" in products_page.driver.current_url.lower(), "Should navigate to cart page"
    
    @allure.title("Test logout functionality")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout_functionality(self, logged_in_user):
        """Test logout functionality from products page"""
        login_page, products_page = logged_in_user
        
        with allure.step("Verify user is logged in"):
            assert products_page.is_products_page_displayed(), "User should be on products page"
        
        with allure.step("Logout from application"):
            products_page.logout()
        
        with allure.step("Verify user is logged out"):
            assert login_page.is_login_page_displayed(), "Should return to login page after logout"
    
    @allure.title("Test add product by name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_product_by_name(self, logged_in_user):
        """Test adding a product to cart by its name"""
        login_page, products_page = logged_in_user
        
        with allure.step("Get available product names"):
            product_names = products_page.get_all_product_names()
            assert len(product_names) > 0, "Should have products available"
        
        with allure.step("Add first product by name"):
            first_product_name = product_names[0]
            products_page.add_product_to_cart_by_name(first_product_name)
        
        with allure.step("Verify product was added"):
            cart_count = products_page.get_cart_item_count()
            assert cart_count == 1, f"Product '{first_product_name}' should be added to cart"
