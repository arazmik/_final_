# Selenium Test Framework

A robust, scalable Selenium-based test automation framework built with Python and Pytest for testing web applications.

## 🚀 Features

- **Page Object Model (POM)** - Clean separation of test logic and page elements
- **Cross-browser Support** - Chrome, Firefox, and Edge browsers
- **Parallel Execution** - Run tests in parallel for faster execution
- **Comprehensive Reporting** - HTML and Allure reports with screenshots
- **Configuration Management** - Environment-based configuration
- **Retry Logic** - Automatic retry for flaky tests
- **Screenshot on Failure** - Automatic screenshots for failed tests
- **Data-driven Testing** - Support for parameterized tests

## 📁 Project Structure

```
selenium_framework/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration settings
├── core/
│   ├── __init__.py
│   ├── base_page.py         # Base page class with common methods
│   └── driver_manager.py    # WebDriver management
├── pages/
│   ├── __init__.py
│   ├── login_page.py        # Login page object
│   └── products_page.py     # Products page object
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures and configuration
│   ├── test_login.py        # Login functionality tests
│   └── test_products.py     # Products functionality tests
├── screenshots/             # Screenshots on test failures
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
   cd selenium_framework
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
pytest tests/test_login.py
```

### Run tests with specific markers
```bash
# Run only smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run slow tests
pytest -m slow
```

### Run tests in parallel
```bash
pytest -n auto  # Uses all available CPU cores
pytest -n 4     # Uses 4 parallel workers
```

### Run tests with different browsers
```bash
# Chrome (default)
pytest

# Firefox
BROWSER=firefox pytest

# Edge
BROWSER=edge pytest

# Headless mode
HEADLESS=true pytest
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
# Browser Configuration
BROWSER=chrome
HEADLESS=false
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080

# Timeouts (in seconds)
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
PAGE_LOAD_TIMEOUT=30

# Test Data
BASE_URL=https://www.saucedemo.com
USERNAME=standard_user
PASSWORD=secret_sauce

# Reporting
SCREENSHOT_ON_FAILURE=true
ALLURE_RESULTS_DIR=allure-results
```

### Test Markers
- `@pytest.mark.smoke` - Quick tests for basic functionality
- `@pytest.mark.regression` - Comprehensive test suite
- `@pytest.mark.slow` - Tests that take longer to execute

## 🏗️ Framework Architecture

### Page Object Model
Each page is represented by a class that encapsulates:
- Web element locators
- Page-specific methods
- Business logic for that page

### Base Page Class
Provides common functionality:
- Element finding with explicit waits
- Common interactions (click, send_keys, etc.)
- Screenshot capture
- Validation methods

### Driver Management
- Automatic driver installation using WebDriver Manager
- Cross-browser support
- Proper cleanup and resource management

## 🧪 Test Examples

### Login Test
```python
def test_successful_login(self, login_page, products_page):
    """Test successful login with valid credentials"""
    login_page.navigate_to_login()
    login_page.login()
    assert products_page.is_products_page_displayed()
```

### Product Management Test
```python
def test_add_product_to_cart(self, logged_in_user):
    """Test adding a product to cart"""
    login_page, products_page = logged_in_user
    products_page.add_product_to_cart(0)
    assert products_page.get_cart_item_count() == 1
```

## 🚀 Demo GIF

![Test Execution Demo](demo.gif)

*Note: Replace with actual GIF showing test execution*

## 📈 Best Practices

1. **Use Page Object Model** - Keep test logic separate from page elements
2. **Implement Explicit Waits** - Avoid flaky tests with proper waits
3. **Use Fixtures** - Reuse common setup and teardown logic
4. **Parameterize Tests** - Use `@pytest.mark.parametrize` for data-driven tests
5. **Clean Test Data** - Ensure tests don't depend on each other
6. **Meaningful Assertions** - Use descriptive assertion messages
7. **Proper Error Handling** - Handle exceptions gracefully

## 🔍 Troubleshooting

### Common Issues

1. **WebDriver not found**
   - Ensure WebDriver Manager is installed
   - Check internet connection for driver downloads

2. **Element not found**
   - Verify element locators are correct
   - Check if explicit waits are properly configured

3. **Tests are flaky**
   - Increase wait times
   - Use more stable locators
   - Implement retry logic

### Debug Mode
```bash
# Run with verbose output
pytest -v -s

# Run single test with debug
pytest tests/test_login.py::TestLogin::test_successful_login -v -s
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
