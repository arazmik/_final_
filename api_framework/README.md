# API Test Framework

A comprehensive, scalable API test automation framework built with Python, Pytest, and Requests for testing REST APIs.

## 🚀 Features

- **Service Layer Architecture** - Clean separation of API logic and test cases
- **Comprehensive Validation** - JSON schema validation, response time checks, and data type validation
- **Retry Logic** - Automatic retry for failed requests with exponential backoff
- **Detailed Logging** - Request/response logging for debugging
- **Multiple Report Formats** - HTML and Allure reports
- **Data-driven Testing** - Support for parameterized tests with test data
- **Integration Testing** - Cross-API relationship validation
- **Error Handling** - Robust error handling and validation

## 📁 Project Structure

```
api_framework/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration settings
├── core/
│   ├── __init__.py
│   ├── api_client.py        # HTTP client with retry logic
│   └── validators.py        # Response validation utilities
├── services/
│   ├── __init__.py
│   ├── posts_service.py     # Posts API service
│   ├── users_service.py     # Users API service
│   └── comments_service.py  # Comments API service
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures and configuration
│   ├── test_posts_api.py    # Posts API tests
│   ├── test_users_api.py    # Users API tests
│   ├── test_comments_api.py # Comments API tests
│   └── test_integration.py  # Integration tests
├── reports/                 # HTML test reports
├── allure-results/          # Allure test results
├── requirements.txt         # Python dependencies
├── pytest.ini             # Pytest configuration
├── env.example            # Environment variables example
└── README.md              # This file
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd api_framework
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

## 🎯 Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_posts_api.py
```

### Run tests with specific markers
```bash
# Run only smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run integration tests
pytest -m integration

# Run slow tests
pytest -m slow
```

### Run tests in parallel
```bash
pytest -n auto  # Uses all available CPU cores
pytest -n 4     # Uses 4 parallel workers
```

### Run specific test class or method
```bash
# Run specific test class
pytest tests/test_posts_api.py::TestPostsAPI

# Run specific test method
pytest tests/test_posts_api.py::TestPostsAPI::test_get_all_posts
```

## 📊 Test Reports

### HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Allure Report
```bash
# Generate Allure results
pytest --alluredir=allure-results

# Serve Allure report
allure serve allure-results
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file based on `env.example`:

```env
# API Configuration
BASE_URL=https://jsonplaceholder.typicode.com
API_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=1

# Test Data
TEST_USER_ID=1
TEST_POST_ID=1
TEST_COMMENT_ID=1

# Reporting
ALLURE_RESULTS_DIR=allure-results
LOG_LEVEL=INFO
```

### Test Markers
- `@pytest.mark.smoke` - Quick tests for basic functionality
- `@pytest.mark.regression` - Comprehensive test suite
- `@pytest.mark.integration` - Cross-API integration tests
- `@pytest.mark.slow` - Tests that take longer to execute

## 🏗️ Framework Architecture

### Service Layer Pattern
Each API endpoint is represented by a service class that encapsulates:
- HTTP request methods (GET, POST, PUT, PATCH, DELETE)
- Request/response handling
- Data validation
- Business logic for that API

### API Client
Centralized HTTP client with:
- Automatic retry logic
- Request/response logging
- Timeout handling
- Session management

### Validation Framework
Comprehensive validation utilities:
- JSON schema validation
- Response time validation
- Data type validation
- Header validation

## 🧪 Test Examples

### Basic API Test
```python
def test_get_all_posts(self, posts_service):
    """Test retrieving all posts"""
    result = posts_service.get_all_posts()
    assert result["status_code"] == 200
    assert result["data"] is not None
    assert len(result["data"]) > 0
```

### Schema Validation Test
```python
def test_post_schema_validation(self, posts_service):
    """Test post data schema validation"""
    result = posts_service.get_post_by_id(1)
    assert posts_service.validate_post_schema(result["data"])
```

### Integration Test
```python
def test_user_post_relationship(self, users_service, posts_service):
    """Test user-post relationship"""
    user_result = users_service.get_user_by_id(1)
    posts_result = posts_service.get_posts_by_user(1)
    
    for post in posts_result["data"]:
        assert post["userId"] == 1
```

## 🚀 Demo GIF

![API Test Execution Demo](demo.gif)

*Note: Replace with actual GIF showing test execution*

## 📈 Best Practices

1. **Use Service Layer** - Keep API logic separate from test logic
2. **Validate Everything** - Schema, response time, data types, headers
3. **Use Fixtures** - Reuse common setup and test data
4. **Parameterize Tests** - Use `@pytest.mark.parametrize` for data-driven tests
5. **Clean Test Data** - Ensure tests don't depend on each other
6. **Meaningful Assertions** - Use descriptive assertion messages
7. **Proper Error Handling** - Handle API errors gracefully
8. **Logging** - Implement comprehensive logging for debugging

## 🔍 API Endpoints Tested

### Posts API (JSONPlaceholder)
- `GET /posts` - Get all posts
- `GET /posts/{id}` - Get post by ID
- `GET /posts?userId={id}` - Get posts by user
- `POST /posts` - Create new post
- `PUT /posts/{id}` - Update post
- `PATCH /posts/{id}` - Partially update post
- `DELETE /posts/{id}` - Delete post

### Users API (JSONPlaceholder)
- `GET /users` - Get all users
- `GET /users/{id}` - Get user by ID
- `POST /users` - Create new user
- `PUT /users/{id}` - Update user
- `PATCH /users/{id}` - Partially update user
- `DELETE /users/{id}` - Delete user

### Comments API (JSONPlaceholder)
- `GET /comments` - Get all comments
- `GET /comments/{id}` - Get comment by ID
- `GET /comments?postId={id}` - Get comments by post
- `POST /comments` - Create new comment
- `PUT /comments/{id}` - Update comment
- `PATCH /comments/{id}` - Partially update comment
- `DELETE /comments/{id}` - Delete comment

### Cat Facts API (catfact.ninja)
- `GET /fact` - Get random cat fact
- `GET /facts` - Get multiple cat facts with pagination
- `GET /breeds` - Get cat breeds with pagination

## 📋 Cat Facts API Test Cases

| Test Case Name | Description | Validation Approach |
|---|---|---|
| `test_api_endpoints` | Tests various API endpoints for expected status codes using pytest parametrize | Uses `@pytest.mark.parametrize` to test multiple endpoints (`/fact`, `/facts`, `/breeds`, `/invalid_endpoint`) with their expected HTTP status codes (200, 200, 200, 404) |
| `test_random_fact_content` | Verifies that the `/fact` endpoint returns a valid fact with proper structure | Validates response status code (200), checks for required fields (`fact`, `length`), ensures fact content is non-empty, and verifies data types |
| `test_facts_pagination` | Tests pagination functionality with different limit and page parameters | Uses `@pytest.mark.parametrize` to test multiple pagination scenarios, validates response structure, verifies pagination metadata (`current_page`, `per_page`, `total`), and ensures correct number of items returned |
| `test_breeds_structure` | Ensures that the `/breeds` endpoint returns data with the expected structure | Validates response status code, checks for required breed fields (`breed`, `country`, `origin`, `coat`, `pattern`), verifies data types, and ensures non-empty string values |

### Validation Methods Used

1. **Status Code Validation**: Each test verifies that the API returns the expected HTTP status code, ensuring endpoints are functioning correctly.

2. **Schema Validation**: Tests validate that API responses contain the expected fields and data structures using custom validation methods.

3. **Data Type Validation**: Ensures that response fields contain the correct data types (strings, integers, arrays).

4. **Content Validation**: Verifies that returned data is not empty and contains meaningful content.

5. **Pagination Validation**: Tests pagination parameters to ensure correct page numbers, item counts, and metadata.

6. **Response Time Validation**: Validates that API responses are returned within acceptable time limits (2 seconds).

7. **Error Handling Validation**: Tests API behavior with invalid requests to ensure proper error responses.

8. **Data Consistency Validation**: Verifies that multiple requests return consistent data structures.

The framework uses pytest parametrize extensively to reduce code duplication while maintaining high test coverage across different scenarios and edge cases.

## 🔍 Troubleshooting

### Common Issues

1. **Connection timeout**
   - Check network connectivity
   - Increase timeout values in configuration
   - Verify API endpoint is accessible

2. **Schema validation failures**
   - Check if API response structure has changed
   - Update schema definitions if needed
   - Verify test data matches expected format

3. **Test data issues**
   - Ensure test data is valid and consistent
   - Check for data dependencies between tests
   - Use unique identifiers for test data

### Debug Mode
```bash
# Run with verbose output and logging
pytest -v -s --log-cli-level=DEBUG

# Run single test with debug
pytest tests/test_posts_api.py::TestPostsAPI::test_get_all_posts -v -s
```

## 🧪 Test Data Management

### Sample Data Fixtures
```python
@pytest.fixture
def sample_post_data():
    return {
        "title": "Test Post Title",
        "body": "This is a test post body content.",
        "userId": 1
    }
```

### Data Validation
```python
def validate_post_data(post_data):
    required_fields = ["userId", "id", "title", "body"]
    for field in required_fields:
        assert field in post_data, f"Missing required field: {field}"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or support, please contact the development team or create an issue in the repository.
