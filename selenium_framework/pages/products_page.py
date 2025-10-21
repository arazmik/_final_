"""
Products page object for Sauce Demo application
"""
from typing import List
from selenium.webdriver.common.by import By
from core.base_page import BasePage


class ProductsPage(BasePage):
    """Products page object with all product-related elements and actions"""
    
    # Locators
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='remove']")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_products_page_displayed(self) -> bool:
        """Check if products page is displayed"""
        return self.is_element_visible(self.PRODUCTS_TITLE)
    
    def get_page_title(self) -> str:
        """Get the products page title"""
        return self.get_text(self.PRODUCTS_TITLE)
    
    def get_product_count(self) -> int:
        """Get total number of products on the page"""
        products = self.find_elements(self.PRODUCT_ITEMS)
        return len(products)
    
    def get_all_product_names(self) -> List[str]:
        """Get all product names"""
        name_elements = self.find_elements(self.PRODUCT_NAMES)
        return [element.text for element in name_elements]
    
    def get_all_product_prices(self) -> List[str]:
        """Get all product prices"""
        price_elements = self.find_elements(self.PRODUCT_PRICES)
        return [element.text for element in price_elements]
    
    def add_product_to_cart(self, product_index: int = 0) -> None:
        """Add a product to cart by index"""
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if product_index < len(add_buttons):
            add_buttons[product_index].click()
    
    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """Add a product to cart by name"""
        product_names = self.find_elements(self.PRODUCT_NAMES)
        for i, name_element in enumerate(product_names):
            if name_element.text == product_name:
                self.add_product_to_cart(i)
                break
    
    def remove_product_from_cart(self, product_index: int = 0) -> None:
        """Remove a product from cart by index"""
        remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
        if product_index < len(remove_buttons):
            remove_buttons[product_index].click()
    
    def get_cart_item_count(self) -> int:
        """Get the number of items in the cart"""
        if self.is_element_visible(self.SHOPPING_CART_BADGE):
            return int(self.get_text(self.SHOPPING_CART_BADGE))
        return 0
    
    def click_shopping_cart(self) -> None:
        """Click on shopping cart"""
        self.click_element(self.SHOPPING_CART_LINK)
    
    def sort_products(self, sort_option: str) -> None:
        """Sort products by given option"""
        from selenium.webdriver.support.ui import Select
        sort_dropdown = self.find_element(self.SORT_DROPDOWN)
        select = Select(sort_dropdown)
        select.select_by_value(sort_option)
    
    def get_sort_options(self) -> List[str]:
        """Get all available sort options"""
        from selenium.webdriver.support.ui import Select
        sort_dropdown = self.find_element(self.SORT_DROPDOWN)
        select = Select(sort_dropdown)
        return [option.get_attribute("value") for option in select.options]
    
    def logout(self) -> None:
        """Logout from the application"""
        self.click_element(self.MENU_BUTTON)
        self.click_element(self.LOGOUT_LINK)
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if a specific product is in the cart"""
        # This would typically check the cart page, but for demo purposes
        # we'll check if the remove button is present for the product
        product_names = self.find_elements(self.PRODUCT_NAMES)
        for i, name_element in enumerate(product_names):
            if name_element.text == product_name:
                remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
                return i < len(remove_buttons) and remove_buttons[i].is_displayed()
        return False
