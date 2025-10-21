"""
Configuration settings for the Twitch Mobile Test framework
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Browser settings - Mobile Chrome emulator
    browser: str = "chrome"
    headless: bool = False    
    # mobile_emulation: bool = True
    mobile_emulation: bool = False
    device_name: str = "iPhone 12 Pro"  # Default mobile device
    
    # Mobile viewport settings
    mobile_width: int = 390
    mobile_height: int = 844
    
    # Test settings
    implicit_wait: int = 10
    explicit_wait: int = 20
    page_load_timeout: int = 30
    
    # Test data
    base_url: str = "https://m.twitch.tv"
    search_page_url: str = "https://m.twitch.tv/directory"
    search_term: str = "StarCraft II"
    
    # Screenshot settings
    screenshot_on_failure: bool = True
    screenshot_on_success: bool = True
    screenshots_dir: str = "screenshots"
    
    # Reporting
    allure_results_dir: str = "allure-results"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
