"""
Service class for Cat Facts API endpoints
"""
from typing import Dict, Any, List, Optional
from core.api_client import APIClient
from core.validators import APIValidator


class CatFactsService:
    """Service class for Cat Facts API operations"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.validator = APIValidator()
    
    def get_random_fact(self) -> Dict[str, Any]:
        """Get a random cat fact"""
        response = self.api_client.get("/fact")
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def get_facts(self, limit: int = 10, page: int = 1) -> Dict[str, Any]:
        """Get multiple cat facts with pagination"""
        params = {"limit": limit, "page": page}
        response = self.api_client.get("/facts", params=params)
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def get_breeds(self, limit: int = 10, page: int = 1) -> Dict[str, Any]:
        """Get cat breeds with pagination"""
        params = {"limit": limit, "page": page}
        response = self.api_client.get("/breeds", params=params)
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def validate_fact_schema(self, response_data: Dict[str, Any]) -> bool:
        """Validate fact data against expected schema"""
        required_fields = ["fact", "length"]
        return all(field in response_data for field in required_fields)
    
    def validate_facts_schema(self, response_data: Dict[str, Any]) -> bool:
        """Validate facts list data against expected schema"""
        required_fields = ["data", "current_page", "per_page", "total"]
        if not all(field in response_data for field in required_fields):
            return False
        
        # Validate data array structure
        if "data" in response_data and response_data["data"]:
            first_fact = response_data["data"][0]
            return self.validate_fact_schema(first_fact)
        
        return True
    
    def validate_breed_schema(self, breed_data: Dict[str, Any]) -> bool:
        """Validate breed data against expected schema"""
        required_fields = ["breed", "country", "origin", "coat", "pattern"]
        return all(field in breed_data for field in required_fields)
    
    def validate_breeds_schema(self, response_data: Dict[str, Any]) -> bool:
        """Validate breeds list data against expected schema"""
        required_fields = ["data", "current_page", "per_page", "total"]
        if not all(field in response_data for field in required_fields):
            return False
        
        # Validate data array structure
        if "data" in response_data and response_data["data"]:
            first_breed = response_data["data"][0]
            return self.validate_breed_schema(first_breed)
        
        return True
    
    def validate_response_time(self, max_time_ms: int = 2000) -> bool:
        """Validate that API response time is within acceptable limits"""
        result = self.get_random_fact()
        return self.validator.validate_response_time(result["response"], max_time_ms)
