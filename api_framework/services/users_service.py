"""
Service class for Users API endpoints
"""
from typing import Dict, Any, List, Optional
from core.api_client import APIClient
from core.validators import APIValidator, USER_SCHEMA


class UsersService:
    """Service class for Users API operations"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.validator = APIValidator()
    
    def get_all_users(self) -> Dict[str, Any]:
        """Get all users"""
        response = self.api_client.get("/users")
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID"""
        response = self.api_client.get(f"/users/{user_id}")
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        response = self.api_client.post("/users", json_data=user_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 201 else None,
            "status_code": response.status_code
        }
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing user"""
        response = self.api_client.put(f"/users/{user_id}", json_data=user_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def patch_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Partially update a user"""
        response = self.api_client.patch(f"/users/{user_id}", json_data=user_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete a user"""
        response = self.api_client.delete(f"/users/{user_id}")
        return {
            "response": response,
            "data": None,
            "status_code": response.status_code
        }
    
    def validate_user_schema(self, response_data: Dict[str, Any]) -> bool:
        """Validate user data against schema"""
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_json_schema(MockResponse(), USER_SCHEMA)
    
    def validate_user_structure(self, response_data: Dict[str, Any]) -> bool:
        """Validate user data structure"""
        required_fields = ["id", "name", "username", "email", "address", "phone", "website", "company"]
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_json_structure(MockResponse(), required_fields)
    
    def validate_user_data_types(self, response_data: Dict[str, Any]) -> bool:
        """Validate user data types"""
        field_types = {
            "id": int,
            "name": str,
            "username": str,
            "email": str,
            "phone": str,
            "website": str
        }
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_data_types(MockResponse(), field_types)
