"""
Configuration settings for the API test framework
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    base_url: str = "https://jsonplaceholder.typicode.com"
    cat_facts_base_url: str = "https://catfact.ninja"
    api_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 1
    
    # Test Data
    test_user_id: int = 1
    test_post_id: int = 1
    test_comment_id: int = 1
    
    # Reporting
    allure_results_dir: str = "allure-results"
    log_level: str = "INFO"
    
    # Headers
    default_headers: dict = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
