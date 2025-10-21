"""
Validation utilities for API responses
"""
import json
from typing import Dict, Any, List, Optional, Union
import jsonschema
from jsonschema import validate, ValidationError


class APIValidator:
    """Utility class for validating API responses"""
    
    @staticmethod
    def validate_status_code(response, expected_status: Union[int, List[int]]) -> bool:
        """Validate response status code"""
        if isinstance(expected_status, int):
            return response.status_code == expected_status
        return response.status_code in expected_status
    
    @staticmethod
    def validate_json_schema(response, schema: Dict[str, Any]) -> bool:
        """Validate response JSON against schema"""
        try:
            response_json = response.json()
            validate(instance=response_json, schema=schema)
            return True
        except (ValueError, json.JSONDecodeError, ValidationError) as e:
            print(f"Schema validation failed: {e}")
            return False
    
    @staticmethod
    def validate_response_time(response, max_time_ms: int) -> bool:
        """Validate response time is within acceptable limits"""
        response_time_ms = response.elapsed.total_seconds() * 1000
        return response_time_ms <= max_time_ms
    
    @staticmethod
    def validate_headers(response, required_headers: Dict[str, str]) -> bool:
        """Validate response headers"""
        for header_name, expected_value in required_headers.items():
            if header_name not in response.headers:
                return False
            if response.headers[header_name] != expected_value:
                return False
        return True
    
    @staticmethod
    def validate_json_structure(response, expected_keys: List[str]) -> bool:
        """Validate that response JSON contains expected keys"""
        try:
            response_json = response.json()
            if isinstance(response_json, list):
                # For array responses, check first element
                if len(response_json) > 0:
                    response_json = response_json[0]
                else:
                    return False
            
            for key in expected_keys:
                if key not in response_json:
                    return False
            return True
        except (ValueError, json.JSONDecodeError):
            return False
    
    @staticmethod
    def validate_data_types(response, field_types: Dict[str, type]) -> bool:
        """Validate data types of specific fields"""
        try:
            response_json = response.json()
            if isinstance(response_json, list):
                # For array responses, check first element
                if len(response_json) > 0:
                    response_json = response_json[0]
                else:
                    return False
            
            for field, expected_type in field_types.items():
                if field not in response_json:
                    return False
                if not isinstance(response_json[field], expected_type):
                    return False
            return True
        except (ValueError, json.JSONDecodeError):
            return False


# Common JSON schemas for JSONPlaceholder API
POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"}
    },
    "required": ["userId", "id", "title", "body"]
}

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"}
                    }
                }
            }
        },
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs": {"type": "string"}
            }
        }
    },
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"]
}

COMMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "postId": {"type": "integer"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "body": {"type": "string"}
    },
    "required": ["postId", "id", "name", "email", "body"]
}
