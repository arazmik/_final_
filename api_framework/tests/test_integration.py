"""
Integration tests for API endpoints
"""
import pytest
import allure
from services.posts_service import PostsService
from services.users_service import UsersService
from services.comments_service import CommentsService


@allure.feature("Integration Tests")
@allure.story("Cross-API Integration")
class TestAPIIntegration:
    """Integration test class for cross-API functionality"""
    
    @allure.title("User-Post relationship validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_user_post_relationship(self, users_service, posts_service):
        """Test that posts are correctly associated with users"""
        user_id = 1
        
        with allure.step(f"Get user {user_id} information"):
            user_result = users_service.get_user_by_id(user_id)
            assert user_result["status_code"] == 200, "User should be retrieved successfully"
            user_data = user_result["data"]
        
        with allure.step(f"Get posts for user {user_id}"):
            posts_result = posts_service.get_posts_by_user(user_id)
            assert posts_result["status_code"] == 200, "Posts should be retrieved successfully"
            posts_data = posts_result["data"]
        
        with allure.step("Verify all posts belong to the user"):
            assert len(posts_data) > 0, "User should have at least one post"
            for post in posts_data:
                assert post["userId"] == user_id, f"Post {post['id']} should belong to user {user_id}"
    
    @allure.title("Post-Comment relationship validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_post_comment_relationship(self, posts_service, comments_service):
        """Test that comments are correctly associated with posts"""
        post_id = 1
        
        with allure.step(f"Get post {post_id} information"):
            post_result = posts_service.get_post_by_id(post_id)
            assert post_result["status_code"] == 200, "Post should be retrieved successfully"
            post_data = post_result["data"]
        
        with allure.step(f"Get comments for post {post_id}"):
            comments_result = comments_service.get_comments_by_post(post_id)
            assert comments_result["status_code"] == 200, "Comments should be retrieved successfully"
            comments_data = comments_result["data"]
        
        with allure.step("Verify all comments belong to the post"):
            assert len(comments_data) > 0, "Post should have at least one comment"
            for comment in comments_data:
                assert comment["postId"] == post_id, f"Comment {comment['id']} should belong to post {post_id}"
    
    @allure.title("Complete user workflow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_complete_user_workflow(self, users_service, posts_service, comments_service):
        """Test complete workflow: user -> posts -> comments"""
        user_id = 1
        
        with allure.step("Get user information"):
            user_result = users_service.get_user_by_id(user_id)
            assert user_result["status_code"] == 200, "User should be retrieved successfully"
            user_data = user_result["data"]
            user_name = user_data["name"]
        
        with allure.step("Get user's posts"):
            posts_result = posts_service.get_posts_by_user(user_id)
            assert posts_result["status_code"] == 200, "Posts should be retrieved successfully"
            posts_data = posts_result["data"]
        
        with allure.step("Get comments for each post"):
            total_comments = 0
            for post in posts_data:
                post_id = post["id"]
                comments_result = comments_service.get_comments_by_post(post_id)
                assert comments_result["status_code"] == 200, f"Comments for post {post_id} should be retrieved"
                comments_data = comments_result["data"]
                total_comments += len(comments_data)
        
        with allure.step("Verify workflow integrity"):
            assert len(posts_data) > 0, f"User {user_name} should have posts"
            assert total_comments > 0, f"User {user_name}'s posts should have comments"
    
    @allure.title("Data consistency across APIs")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.integration
    def test_data_consistency(self, users_service, posts_service, comments_service):
        """Test data consistency across different API endpoints"""
        user_id = 1
        post_id = 1
        
        with allure.step("Get user data"):
            user_result = users_service.get_user_by_id(user_id)
            user_data = user_result["data"]
        
        with allure.step("Get post data"):
            post_result = posts_service.get_post_by_id(post_id)
            post_data = post_result["data"]
        
        with allure.step("Verify post belongs to user"):
            assert post_data["userId"] == user_data["id"], "Post should belong to the specified user"
        
        with allure.step("Get comments for the post"):
            comments_result = comments_service.get_comments_by_post(post_id)
            comments_data = comments_result["data"]
        
        with allure.step("Verify comment-post relationship"):
            for comment in comments_data:
                assert comment["postId"] == post_data["id"], "Comment should belong to the specified post"
    
    @allure.title("API response format consistency")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.integration
    def test_response_format_consistency(self, users_service, posts_service, comments_service):
        """Test that all APIs return consistent response formats"""
        with allure.step("Get data from all APIs"):
            users_result = users_service.get_all_users()
            posts_result = posts_service.get_all_posts()
            comments_result = comments_service.get_all_comments()
        
        with allure.step("Verify response status codes"):
            assert users_result["status_code"] == 200, "Users API should return 200"
            assert posts_result["status_code"] == 200, "Posts API should return 200"
            assert comments_result["status_code"] == 200, "Comments API should return 200"
        
        with allure.step("Verify response data types"):
            assert isinstance(users_result["data"], list), "Users data should be a list"
            assert isinstance(posts_result["data"], list), "Posts data should be a list"
            assert isinstance(comments_result["data"], list), "Comments data should be a list"
        
        with allure.step("Verify response data is not empty"):
            assert len(users_result["data"]) > 0, "Users data should not be empty"
            assert len(posts_result["data"]) > 0, "Posts data should not be empty"
            assert len(comments_result["data"]) > 0, "Comments data should not be empty"
    
    @allure.title("Error handling consistency")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.integration
    def test_error_handling_consistency(self, users_service, posts_service, comments_service):
        """Test that all APIs handle errors consistently"""
        non_existent_id = 99999
        
        with allure.step("Test non-existent user"):
            user_result = users_service.get_user_by_id(non_existent_id)
            assert user_result["status_code"] == 404, "Non-existent user should return 404"
        
        with allure.step("Test non-existent post"):
            post_result = posts_service.get_post_by_id(non_existent_id)
            assert post_result["status_code"] == 404, "Non-existent post should return 404"
        
        with allure.step("Test non-existent comment"):
            comment_result = comments_service.get_comment_by_id(non_existent_id)
            assert comment_result["status_code"] == 404, "Non-existent comment should return 404"
