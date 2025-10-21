"""
Service class for Posts API endpoints
"""
from typing import Dict, Any, List, Optional
from core.api_client import APIClient
from core.validators import APIValidator, POST_SCHEMA


class PostsService:
    """Service class for Posts API operations"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.validator = APIValidator()
    
    def get_all_posts(self) -> Dict[str, Any]:
        """Get all posts"""
        response = self.api_client.get("/posts")
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def get_post_by_id(self, post_id: int) -> Dict[str, Any]:
        """Get a specific post by ID"""
        response = self.api_client.get(f"/posts/{post_id}")
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def get_posts_by_user(self, user_id: int) -> Dict[str, Any]:
        """Get all posts by a specific user"""
        response = self.api_client.get("/posts", params={"userId": user_id})
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def create_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new post"""
        response = self.api_client.post("/posts", json_data=post_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 201 else None,
            "status_code": response.status_code
        }
    
    def update_post(self, post_id: int, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing post"""
        response = self.api_client.put(f"/posts/{post_id}", json_data=post_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def patch_post(self, post_id: int, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Partially update a post"""
        response = self.api_client.patch(f"/posts/{post_id}", json_data=post_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def delete_post(self, post_id: int) -> Dict[str, Any]:
        """Delete a post"""
        response = self.api_client.delete(f"/posts/{post_id}")
        return {
            "response": response,
            "data": None,
            "status_code": response.status_code
        }
    
    def validate_post_schema(self, response_data: Dict[str, Any]) -> bool:
        """Validate post data against schema"""
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_json_schema(MockResponse(), POST_SCHEMA)
    
    def validate_post_structure(self, response_data: Dict[str, Any]) -> bool:
        """Validate post data structure"""
        required_fields = ["userId", "id", "title", "body"]
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_json_structure(MockResponse(), required_fields)
    
    def validate_post_data_types(self, response_data: Dict[str, Any]) -> bool:
        """Validate post data types"""
        field_types = {
            "userId": int,
            "id": int,
            "title": str,
            "body": str
        }
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_data_types(MockResponse(), field_types)
