"""
Test cases for Cat Facts API endpoints
"""
import pytest
import allure
from services.cat_facts_service import CatFactsService
from core.validators import APIValidator


@allure.feature("Cat Facts API")
@allure.story("Cat Facts Management")
class TestCatFactsAPI:
    """Test class for Cat Facts API functionality"""
    
    @allure.title("Test API endpoints with parametrize")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("endpoint,expected_status", [
        ("/fact", 200),
        ("/facts", 200),
        ("/breeds", 200),
        ("/invalid_endpoint", 404)
    ])
    def test_api_endpoints(self, cat_facts_service, endpoint, expected_status):
        """Test various API endpoints for expected status codes using parametrize"""
        with allure.step(f"Make GET request to {endpoint}"):
            if endpoint == "/fact":
                result = cat_facts_service.get_random_fact()
            elif endpoint == "/facts":
                result = cat_facts_service.get_facts()
            elif endpoint == "/breeds":
                result = cat_facts_service.get_breeds()
            else:
                # For invalid endpoint, we'll make a direct request
                response = cat_facts_service.api_client.get(endpoint)
                result = {
                    "response": response,
                    "data": None,
                    "status_code": response.status_code
                }
        
        with allure.step(f"Verify response status code is {expected_status}"):
            assert result["status_code"] == expected_status, \
                f"Expected {expected_status}, got {result['status_code']}"
    
    @allure.title("Test random fact content validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_random_fact_content(self, cat_facts_service):
        """Verify that the /fact endpoint returns a valid fact with proper structure"""
        with allure.step("Make GET request to /fact"):
            result = cat_facts_service.get_random_fact()
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data structure"):
            assert result["data"] is not None, "Response data should not be None"
            assert cat_facts_service.validate_fact_schema(result["data"]), \
                "Fact should match expected schema"
        
        with allure.step("Verify fact content"):
            fact_data = result["data"]
            assert "fact" in fact_data, "Response should contain 'fact' field"
            assert "length" in fact_data, "Response should contain 'length' field"
            assert len(fact_data["fact"]) > 0, "Fact should not be empty"
            assert isinstance(fact_data["length"], int), "Length should be an integer"
            assert fact_data["length"] > 0, "Length should be positive"
    
    @allure.title("Test facts pagination with parametrize")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("limit,page,expected_count", [
        (5, 1, 5),
        (10, 2, 10),
        (3, 1, 3),
        (1, 1, 1)
    ])
    def test_facts_pagination(self, cat_facts_service, limit, page, expected_count):
        """Test that the /facts endpoint supports pagination with different parameters"""
        with allure.step(f"Make GET request to /facts with limit={limit}, page={page}"):
            result = cat_facts_service.get_facts(limit=limit, page=page)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify pagination structure"):
            assert result["data"] is not None, "Response data should not be None"
            assert cat_facts_service.validate_facts_schema(result["data"]), \
                "Facts response should match expected schema"
        
        with allure.step("Verify pagination parameters"):
            facts_data = result["data"]
            assert "data" in facts_data, "Response should contain 'data' field"
            assert "current_page" in facts_data, "Response should contain 'current_page' field"
            assert "per_page" in facts_data, "Response should contain 'per_page' field"
            assert "total" in facts_data, "Response should contain 'total' field"
            
            assert facts_data["current_page"] == page, f"Current page should be {page}"
            assert facts_data["per_page"] == limit, f"Per page should be {limit}"
            assert len(facts_data["data"]) <= expected_count, \
                f"Should return at most {expected_count} facts"
    
    @allure.title("Test breeds structure validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_breeds_structure(self, cat_facts_service):
        """Ensure that the /breeds endpoint returns data with the expected structure"""
        with allure.step("Make GET request to /breeds"):
            result = cat_facts_service.get_breeds(limit=5)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify breeds structure"):
            assert result["data"] is not None, "Response data should not be None"
            assert cat_facts_service.validate_breeds_schema(result["data"]), \
                "Breeds response should match expected schema"
        
        with allure.step("Verify individual breed structure"):
            breeds_data = result["data"]
            assert "data" in breeds_data, "Response should contain 'data' field"
            
            if breeds_data["data"]:  # If there are breeds returned
                first_breed = breeds_data["data"][0]
                required_fields = ["breed", "country", "origin", "coat", "pattern"]
                
                for field in required_fields:
                    assert field in first_breed, f"Breed should have {field} field"
                    assert isinstance(first_breed[field], str), f"{field} should be a string"
                    assert len(first_breed[field]) > 0, f"{field} should not be empty"
    
    @allure.title("Test API response time validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_response_time(self, cat_facts_service):
        """Test that API responds within acceptable time limits"""
        max_response_time = 2000  # 2 seconds in milliseconds
        
        with allure.step("Make GET request to /fact and measure response time"):
            result = cat_facts_service.get_random_fact()
        
        with allure.step("Verify response time"):
            validator = APIValidator()
            assert validator.validate_response_time(result["response"], max_response_time), \
                f"Response time should be less than {max_response_time}ms"
    
    @allure.title("Test error handling for invalid requests")
    @allure.severity(allure.severity_level.NORMAL)
    def test_error_handling(self, cat_facts_service):
        """Test API error handling for invalid requests"""
        with allure.step("Make request to non-existent endpoint"):
            response = cat_facts_service.api_client.get("/nonexistent")
            result = {
                "response": response,
                "data": None,
                "status_code": response.status_code
            }
        
        with allure.step("Verify error response"):
            assert result["status_code"] == 404, f"Expected 404, got {result['status_code']}"
            assert result["data"] is None, "Error response should not contain data"
    
    @allure.title("Test data consistency across multiple requests")
    @allure.severity(allure.severity_level.NORMAL)
    def test_data_consistency(self, cat_facts_service):
        """Test that API returns consistent data structure across multiple requests"""
        with allure.step("Make multiple requests to verify consistency"):
            results = []
            for _ in range(3):
                result = cat_facts_service.get_random_fact()
                results.append(result)
        
        with allure.step("Verify all responses have consistent structure"):
            for i, result in enumerate(results):
                assert result["status_code"] == 200, f"Request {i+1} should return 200"
                assert result["data"] is not None, f"Request {i+1} data should not be None"
                assert cat_facts_service.validate_fact_schema(result["data"]), \
                    f"Request {i+1} should match schema"
        
        with allure.step("Verify facts are different (randomness)"):
            facts = [result["data"]["fact"] for result in results]
            # At least one fact should be different (very high probability)
            assert len(set(facts)) > 1, "Random facts should be different"
