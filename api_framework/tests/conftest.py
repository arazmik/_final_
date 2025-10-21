"""
Pytest configuration and fixtures for API tests
"""
import pytest
import allure
from core.api_client import APIClient
from services.posts_service import PostsService
from services.users_service import UsersService
from services.comments_service import CommentsService
from services.cat_facts_service import CatFactsService


@pytest.fixture(scope="session")
def api_client():
    """Create API client instance"""
    client = APIClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def posts_service(api_client):
    """Create PostsService instance"""
    return PostsService(api_client)


@pytest.fixture(scope="session")
def users_service(api_client):
    """Create UsersService instance"""
    return UsersService(api_client)


@pytest.fixture(scope="session")
def comments_service(api_client):
    """Create CommentsService instance"""
    return CommentsService(api_client)


@pytest.fixture(scope="session")
def cat_facts_service():
    """Create CatFactsService instance with cat facts API client"""
    from config.settings import settings
    # Create a separate API client for cat facts API
    cat_facts_client = APIClient(base_url="https://catfact.ninja")
    return CatFactsService(cat_facts_client)


@pytest.fixture
def sample_post_data():
    """Sample post data for testing"""
    return {
        "title": "Test Post Title",
        "body": "This is a test post body content.",
        "userId": 1
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "address": {
            "street": "123 Test St",
            "suite": "Apt 1",
            "city": "Test City",
            "zipcode": "12345",
            "geo": {
                "lat": "0.0",
                "lng": "0.0"
            }
        },
        "phone": "123-456-7890",
        "website": "test.com",
        "company": {
            "name": "Test Company",
            "catchPhrase": "Test catchphrase",
            "bs": "Test business"
        }
    }


@pytest.fixture
def sample_comment_data():
    """Sample comment data for testing"""
    return {
        "postId": 1,
        "name": "Test Comment",
        "email": "comment@example.com",
        "body": "This is a test comment body."
    }


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
