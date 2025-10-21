"""
Service class for Comments API endpoints
"""
from typing import Dict, Any, List, Optional
from core.api_client import APIClient
from core.validators import APIValidator, COMMENT_SCHEMA


class CommentsService:
    """Service class for Comments API operations"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.validator = APIValidator()
    
    def get_all_comments(self) -> Dict[str, Any]:
        """Get all comments"""
        response = self.api_client.get("/comments")
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def get_comment_by_id(self, comment_id: int) -> Dict[str, Any]:
        """Get a specific comment by ID"""
        response = self.api_client.get(f"/comments/{comment_id}")
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def get_comments_by_post(self, post_id: int) -> Dict[str, Any]:
        """Get all comments for a specific post"""
        response = self.api_client.get("/comments", params={"postId": post_id})
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def create_comment(self, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new comment"""
        response = self.api_client.post("/comments", json_data=comment_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 201 else None,
            "status_code": response.status_code
        }
    
    def update_comment(self, comment_id: int, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing comment"""
        response = self.api_client.put(f"/comments/{comment_id}", json_data=comment_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def patch_comment(self, comment_id: int, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Partially update a comment"""
        response = self.api_client.patch(f"/comments/{comment_id}", json_data=comment_data)
        return {
            "response": response,
            "data": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    
    def delete_comment(self, comment_id: int) -> Dict[str, Any]:
        """Delete a comment"""
        response = self.api_client.delete(f"/comments/{comment_id}")
        return {
            "response": response,
            "data": None,
            "status_code": response.status_code
        }
    
    def validate_comment_schema(self, response_data: Dict[str, Any]) -> bool:
        """Validate comment data against schema"""
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_json_schema(MockResponse(), COMMENT_SCHEMA)
    
    def validate_comment_structure(self, response_data: Dict[str, Any]) -> bool:
        """Validate comment data structure"""
        required_fields = ["postId", "id", "name", "email", "body"]
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_json_structure(MockResponse(), required_fields)
    
    def validate_comment_data_types(self, response_data: Dict[str, Any]) -> bool:
        """Validate comment data types"""
        field_types = {
            "postId": int,
            "id": int,
            "name": str,
            "email": str,
            "body": str
        }
        class MockResponse:
            def json(self):
                return response_data
        return self.validator.validate_data_types(MockResponse(), field_types)
