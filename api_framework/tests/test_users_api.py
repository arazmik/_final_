"""
Test cases for Users API endpoints
"""
import pytest
import allure
from services.users_service import UsersService
from core.validators import APIValidator


@allure.feature("Users API")
@allure.story("Users Management")
class TestUsersAPI:
    """Test class for Users API functionality"""
    
    @allure.title("Get all users")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_users(self, users_service):
        """Test retrieving all users"""
        with allure.step("Make GET request to /users"):
            result = users_service.get_all_users()
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data is not empty"):
            assert result["data"] is not None, "Response data should not be None"
            assert len(result["data"]) > 0, "Should return at least one user"
        
        with allure.step("Verify response structure"):
            first_user = result["data"][0]
            assert users_service.validate_user_structure(first_user), "User structure should be valid"
            assert users_service.validate_user_data_types(first_user), "User data types should be valid"
    
    @allure.title("Get user by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_user_by_id(self, users_service):
        """Test retrieving a specific user by ID"""
        user_id = 1
        
        with allure.step(f"Make GET request to /users/{user_id}"):
            result = users_service.get_user_by_id(user_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == user_id, f"User ID should be {user_id}"
        
        with allure.step("Verify user schema"):
            assert users_service.validate_user_schema(result["data"]), "User should match schema"
    
    @allure.title("Create new user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_user(self, users_service, sample_user_data):
        """Test creating a new user"""
        with allure.step("Make POST request to /users"):
            result = users_service.create_user(sample_user_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 201, f"Expected 201, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["name"] == sample_user_data["name"], "Name should match"
            assert result["data"]["username"] == sample_user_data["username"], "Username should match"
            assert result["data"]["email"] == sample_user_data["email"], "Email should match"
            assert "id" in result["data"], "Response should include generated ID"
    
    @allure.title("Update existing user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self, users_service, sample_user_data):
        """Test updating an existing user"""
        user_id = 1
        updated_data = sample_user_data.copy()
        updated_data["name"] = "Updated Test User"
        updated_data["email"] = "updated@example.com"
        
        with allure.step(f"Make PUT request to /users/{user_id}"):
            result = users_service.update_user(user_id, updated_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == user_id, f"User ID should remain {user_id}"
            assert result["data"]["name"] == updated_data["name"], "Name should be updated"
            assert result["data"]["email"] == updated_data["email"], "Email should be updated"
    
    @allure.title("Partially update user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_patch_user(self, users_service):
        """Test partially updating a user"""
        user_id = 1
        patch_data = {"name": "Patched User Name"}
        
        with allure.step(f"Make PATCH request to /users/{user_id}"):
            result = users_service.patch_user(user_id, patch_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == user_id, f"User ID should remain {user_id}"
            assert result["data"]["name"] == patch_data["name"], "Name should be patched"
    
    @allure.title("Delete user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user(self, users_service):
        """Test deleting a user"""
        user_id = 1
        
        with allure.step(f"Make DELETE request to /users/{user_id}"):
            result = users_service.delete_user(user_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is None, "Response data should be None for DELETE"
    
    @allure.title("Get non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_user(self, users_service):
        """Test retrieving a non-existent user"""
        non_existent_id = 99999
        
        with allure.step(f"Make GET request to /users/{non_existent_id}"):
            result = users_service.get_user_by_id(non_existent_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 404, f"Expected 404, got {result['status_code']}"
    
    @allure.title("Validate user address structure")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_address_structure(self, users_service):
        """Test that user address structure is correct"""
        user_id = 1
        
        with allure.step(f"Get user {user_id} data"):
            result = users_service.get_user_by_id(user_id)
        
        with allure.step("Verify address structure"):
            assert result["status_code"] == 200, "User should be retrieved successfully"
            user_data = result["data"]
            
            # Verify address fields
            assert "address" in user_data, "User should have address field"
            address = user_data["address"]
            
            required_address_fields = ["street", "suite", "city", "zipcode", "geo"]
            for field in required_address_fields:
                assert field in address, f"Address should have {field} field"
            
            # Verify geo fields
            geo = address["geo"]
            assert "lat" in geo, "Geo should have lat field"
            assert "lng" in geo, "Geo should have lng field"
    
    @allure.title("Validate user company structure")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_company_structure(self, users_service):
        """Test that user company structure is correct"""
        user_id = 1
        
        with allure.step(f"Get user {user_id} data"):
            result = users_service.get_user_by_id(user_id)
        
        with allure.step("Verify company structure"):
            assert result["status_code"] == 200, "User should be retrieved successfully"
            user_data = result["data"]
            
            # Verify company fields
            assert "company" in user_data, "User should have company field"
            company = user_data["company"]
            
            required_company_fields = ["name", "catchPhrase", "bs"]
            for field in required_company_fields:
                assert field in company, f"Company should have {field} field"
    
    @allure.title("Validate users response time")
    @allure.severity(allure.severity_level.NORMAL)
    def test_users_response_time(self, users_service):
        """Test that users API responds within acceptable time"""
        max_response_time = 2000  # 2 seconds in milliseconds
        
        with allure.step("Make GET request to /users"):
            result = users_service.get_all_users()
        
        with allure.step("Verify response time"):
            validator = APIValidator()
            assert validator.validate_response_time(result["response"], max_response_time), \
                f"Response time should be less than {max_response_time}ms"
