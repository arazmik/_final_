"""
Configuration settings for the Selenium test framework
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Browser settings
    browser: str = "chrome"
    headless: bool = False
    window_width: int = 1920
    window_height: int = 1080
    
    # Test settings
    implicit_wait: int = 10
    explicit_wait: int = 20
    page_load_timeout: int = 30
    
    # Test data
    base_url: str = "https://www.saucedemo.com"
    username: str = "standard_user"
    password: str = "secret_sauce"
    
    # Reporting
    screenshot_on_failure: bool = True
    allure_results_dir: str = "allure-results"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
