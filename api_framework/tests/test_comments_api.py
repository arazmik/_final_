"""
Test cases for Comments API endpoints
"""
import pytest
import allure
from services.comments_service import CommentsService
from core.validators import APIValidator


@allure.feature("Comments API")
@allure.story("Comments Management")
class TestCommentsAPI:
    """Test class for Comments API functionality"""
    
    @allure.title("Get all comments")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_comments(self, comments_service):
        """Test retrieving all comments"""
        with allure.step("Make GET request to /comments"):
            result = comments_service.get_all_comments()
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data is not empty"):
            assert result["data"] is not None, "Response data should not be None"
            assert len(result["data"]) > 0, "Should return at least one comment"
        
        with allure.step("Verify response structure"):
            first_comment = result["data"][0]
            assert comments_service.validate_comment_structure(first_comment), "Comment structure should be valid"
            assert comments_service.validate_comment_data_types(first_comment), "Comment data types should be valid"
    
    @allure.title("Get comment by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_comment_by_id(self, comments_service):
        """Test retrieving a specific comment by ID"""
        comment_id = 1
        
        with allure.step(f"Make GET request to /comments/{comment_id}"):
            result = comments_service.get_comment_by_id(comment_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == comment_id, f"Comment ID should be {comment_id}"
        
        with allure.step("Verify comment schema"):
            assert comments_service.validate_comment_schema(result["data"]), "Comment should match schema"
    
    @allure.title("Get comments by post ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_comments_by_post(self, comments_service):
        """Test retrieving comments by post ID"""
        post_id = 1
        
        with allure.step(f"Make GET request to /comments?postId={post_id}"):
            result = comments_service.get_comments_by_post(post_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            
            # Verify all comments belong to the specified post
            for comment in result["data"]:
                assert comment["postId"] == post_id, f"All comments should belong to post {post_id}"
    
    @allure.title("Create new comment")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_comment(self, comments_service, sample_comment_data):
        """Test creating a new comment"""
        with allure.step("Make POST request to /comments"):
            result = comments_service.create_comment(sample_comment_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 201, f"Expected 201, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["postId"] == sample_comment_data["postId"], "Post ID should match"
            assert result["data"]["name"] == sample_comment_data["name"], "Name should match"
            assert result["data"]["email"] == sample_comment_data["email"], "Email should match"
            assert result["data"]["body"] == sample_comment_data["body"], "Body should match"
            assert "id" in result["data"], "Response should include generated ID"
    
    @allure.title("Update existing comment")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_comment(self, comments_service, sample_comment_data):
        """Test updating an existing comment"""
        comment_id = 1
        updated_data = sample_comment_data.copy()
        updated_data["name"] = "Updated Test Comment"
        updated_data["body"] = "This is an updated test comment body."
        
        with allure.step(f"Make PUT request to /comments/{comment_id}"):
            result = comments_service.update_comment(comment_id, updated_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == comment_id, f"Comment ID should remain {comment_id}"
            assert result["data"]["name"] == updated_data["name"], "Name should be updated"
            assert result["data"]["body"] == updated_data["body"], "Body should be updated"
    
    @allure.title("Partially update comment")
    @allure.severity(allure.severity_level.NORMAL)
    def test_patch_comment(self, comments_service):
        """Test partially updating a comment"""
        comment_id = 1
        patch_data = {"name": "Patched Comment Name"}
        
        with allure.step(f"Make PATCH request to /comments/{comment_id}"):
            result = comments_service.patch_comment(comment_id, patch_data)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is not None, "Response data should not be None"
            assert result["data"]["id"] == comment_id, f"Comment ID should remain {comment_id}"
            assert result["data"]["name"] == patch_data["name"], "Name should be patched"
    
    @allure.title("Delete comment")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_comment(self, comments_service):
        """Test deleting a comment"""
        comment_id = 1
        
        with allure.step(f"Make DELETE request to /comments/{comment_id}"):
            result = comments_service.delete_comment(comment_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 200, f"Expected 200, got {result['status_code']}"
        
        with allure.step("Verify response data"):
            assert result["data"] is None, "Response data should be None for DELETE"
    
    @allure.title("Get non-existent comment")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_comment(self, comments_service):
        """Test retrieving a non-existent comment"""
        non_existent_id = 99999
        
        with allure.step(f"Make GET request to /comments/{non_existent_id}"):
            result = comments_service.get_comment_by_id(non_existent_id)
        
        with allure.step("Verify response status code"):
            assert result["status_code"] == 404, f"Expected 404, got {result['status_code']}"
    
    @allure.title("Validate comment email format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_comment_email_format(self, comments_service):
        """Test that comment emails are in valid format"""
        comment_id = 1
        
        with allure.step(f"Get comment {comment_id} data"):
            result = comments_service.get_comment_by_id(comment_id)
        
        with allure.step("Verify email format"):
            assert result["status_code"] == 200, "Comment should be retrieved successfully"
            comment_data = result["data"]
            
            email = comment_data["email"]
            assert "@" in email, "Email should contain @ symbol"
            assert "." in email, "Email should contain domain extension"
    
    @allure.title("Validate comments response time")
    @allure.severity(allure.severity_level.NORMAL)
    def test_comments_response_time(self, comments_service):
        """Test that comments API responds within acceptable time"""
        max_response_time = 2000  # 2 seconds in milliseconds
        
        with allure.step("Make GET request to /comments"):
            result = comments_service.get_all_comments()
        
        with allure.step("Verify response time"):
            validator = APIValidator()
            assert validator.validate_response_time(result["response"], max_response_time), \
                f"Response time should be less than {max_response_time}ms"
    
    @allure.title("Validate comment content types")
    @allure.severity(allure.severity_level.NORMAL)
    def test_comments_content_type(self, comments_service):
        """Test that comments API returns correct content type"""
        with allure.step("Make GET request to /comments"):
            result = comments_service.get_all_comments()
        
        with allure.step("Verify content type"):
            content_type = result["response"].headers.get("content-type", "")
            assert "application/json" in content_type, f"Expected JSON content type, got {content_type}"
