"""
Test cases for Posts API endpoints
"""
import pytest
import allure
from services.posts_service import PostsService
from core.validators import APIValidator


@allure.feature("Posts API")
@allure.story("Posts Management")
class TestPostsAPI:
    """Test class for Posts API functionality"""
    
    @allure.title("Get all posts")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_posts(self, posts_service):
        """Test retrieving all posts"""
        with allure.step("Make GET request to /posts"):
            result = posts_service.get_all_posts()
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data is not empty"):
            assert result["data"] is not None, "Response data should not be None"
            assert len(result["data"]) > 0, "Should return at least one post"
        
        with allure.step("Verify response structure"):
            first_post = result["data"][0]
            assert posts_service.validate_post_structure(first_post), "Post structure should be valid"
            assert posts_service.validate_post_data_types(first_post), "Post data types should be valid"
    
    @allure.title("Get post by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_post_by_id(self, posts_service):
        """Test retrieving a specific post by ID"""
        post_id = 1
        
        with allure.step(f"Make GET request to /posts/{post_id}"):
            result = posts_service.get_post_by_id(post_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == post_id, f"Post ID should be {post_id}"
        
        with allure.step("Verify post schema"):
            assert posts_service.validate_post_schema(result["data"]), "Post should match schema"
    
    @allure.title("Get posts by user ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_posts_by_user(self, posts_service):
        """Test retrieving posts by user ID"""
        user_id = 1
        
        with allure.step(f"Make GET request to /posts?userId={user_id}"):
            result = posts_service.get_posts_by_user(user_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert len(result["data"]) > 0, "Should return at least one post for user"
            
            # Verify all posts belong to the specified user
            for post in result["data"]:
                assert post["userId"] == user_id, f"All posts should belong to user {user_id}"
    
    @allure.title("Create new post")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_post(self, posts_service, sample_post_data):
        """Test creating a new post"""
        with allure.step("Make POST request to /posts"):
            result = posts_service.create_post(sample_post_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 201, f"Expected 201, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["title"] == sample_post_data["title"], "Title should match"
            assert result["data"]["body"] == sample_post_data["body"], "Body should match"
            assert result["data"]["userId"] == sample_post_data["userId"], "User ID should match"
            assert "id" in result["data"], "Response should include generated ID"
    
    @allure.title("Update existing post")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_post(self, posts_service, sample_post_data):
        """Test updating an existing post"""
        post_id = 1
        updated_data = sample_post_data.copy()
        updated_data["title"] = "Updated Test Post Title"
        updated_data["body"] = "This is an updated test post body."
        
        with allure.step(f"Make PUT request to /posts/{post_id}"):
            result = posts_service.update_post(post_id, updated_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == post_id, f"Post ID should remain {post_id}"
            assert result["data"]["title"] == updated_data["title"], "Title should be updated"
            assert result["data"]["body"] == updated_data["body"], "Body should be updated"
    
    @allure.title("Partially update post")
    @allure.severity(allure.severity_level.NORMAL)
    def test_patch_post(self, posts_service):
        """Test partially updating a post"""
        post_id = 1
        patch_data = {"title": "Patched Title"}
        
        with allure.step(f"Make PATCH request to /posts/{post_id}"):
            result = posts_service.patch_post(post_id, patch_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == post_id, f"Post ID should remain {post_id}"
            assert result["data"]["title"] == patch_data["title"], "Title should be patched"
    
    @allure.title("Delete post")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_post(self, posts_service):
        """Test deleting a post"""
        post_id = 1
        
        with allure.step(f"Make DELETE request to /posts/{post_id}"):
            result = posts_service.delete_post(post_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is None, "Response data should be None for DELETE"
    
    @allure.title("Get non-existent post")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_post(self, posts_service):
        """Test retrieving a non-existent post"""
        non_existent_id = 99999
        
        with allure.step(f"Make GET request to /posts/{non_existent_id}"):
            result = posts_service.get_post_by_id(non_existent_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 404, f"Expected 404, got {result['status_code']}"
    
    @allure.title("Validate post response time")
    @allure.severity(allure.severity_level.NORMAL)
    def test_posts_response_time(self, posts_service):
        """Test that posts API responds within acceptable time"""
        max_response_time = 2000  # 2 seconds in milliseconds
        
        with allure.step("Make GET request to /posts"):
            result = posts_service.get_all_posts()
        
        with allure.step("Verify response time"):
            validator = APIValidator()
            assert validator.validate_response_time(result["response"], max_response_time), \
                f"Response time should be less than {max_response_time}ms"
    
    @allure.title("Validate post content types")
    @allure.severity(allure.severity_level.NORMAL)
    def test_posts_content_type(self, posts_service):
        """Test that posts API returns correct content type"""
        with allure.step("Make GET request to /posts"):
            result = posts_service.get_all_posts()
        
        with allure.step("Verify content type"):
            content_type = result["response"].headers.get("content-type", "")
            assert "application/json" in content_type, f"Expected JSON content type, got {content_type}"
