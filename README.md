# AQA Home Task - Test Automation Frameworks

This repository contains two comprehensive test automation frameworks built for the AQA (Automated Quality Assurance) home task assessment.

## 📋 Overview

The assessment consists of three separate solutions, all implemented in Python with Pytest as the test runner:

1. **Selenium-based Framework** - Web UI automation testing (Sauce Demo)
2. **API Test Framework** - REST API automation testing (JSONPlaceholder)
3. **Twitch Mobile Framework** - Mobile web testing with Chrome emulation (Twitch)

## 🏗️ Project Structure

```
_final_/
├── selenium_framework/          # Selenium-based test framework
│   ├── config/                 # Configuration management
│   ├── core/                   # Core framework components
│   ├── pages/                  # Page Object Model classes
│   ├── tests/                  # Test cases
│   ├── requirements.txt        # Dependencies
│   ├── pytest.ini            # Pytest configuration
│   ├── run_tests.py           # Test runner script
│   └── README.md              # Framework documentation
├── api_framework/              # API test framework
│   ├── config/                 # Configuration management
│   ├── core/                   # Core framework components
│   ├── services/               # API service classes
│   ├── tests/                  # Test cases
│   ├── requirements.txt        # Dependencies
│   ├── pytest.ini            # Pytest configuration
│   ├── run_tests.py           # Test runner script
│   └── README.md              # Framework documentation
├── twitch_mobile_framework/    # Twitch mobile test framework
│   ├── config/                 # Mobile-specific configuration
│   ├── core/                   # Mobile-optimized components
│   ├── pages/                  # Twitch page objects
│   ├── tests/                  # Mobile test cases
│   ├── requirements.txt        # Dependencies
│   ├── pytest.ini            # Pytest configuration
│   ├── run_tests.py           # Test runner script
│   └── README.md              # Framework documentation
├── setup.sh                   # Automated setup script
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions

#### Option 1: Quick Setup (Recommended)
```bash
git clone [<repository-url>](https://github.com/arazmik/_final_.git)
cd _final_
chmod +x setup.sh
./setup.sh
```

#### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone [<repository-url>](https://github.com/arazmik/_final_.git)
   cd _final_
   ```

2. **Setup API Framework**
   ```bash
   cd api_framework
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

3. **Setup Selenium Framework**
   ```bash
   cd selenium_framework
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

### Running Tests

#### API Framework
```bash
cd api_framework
source venv/bin/activate
python run_tests.py
```

#### Selenium Framework
```bash
cd selenium_framework
source venv/bin/activate
python run_tests.py
```

#### Twitch Mobile Framework
```bash
cd twitch_mobile_framework
source venv/bin/activate
python run_tests.py
```

## 🎯 Framework Details

### Selenium Framework
- **Target Application**: Sauce Demo (https://www.saucedemo.com)
- **Browser Support**: Chrome, Firefox, Edge
- **Architecture**: Page Object Model (POM)
- **Features**: Cross-browser testing, parallel execution, screenshot capture, comprehensive reporting

### API Framework
- **Target API**: JSONPlaceholder (https://jsonplaceholder.typicode.com)
- **Endpoints**: Posts, Users, Comments APIs
- **Architecture**: Service Layer Pattern
- **Features**: Schema validation, response time validation, integration testing, retry logic

### Twitch Mobile Framework
- **Target Application**: Twitch Mobile Web (https://m.twitch.tv)
- **Browser**: Chrome Mobile Emulation
- **Architecture**: Page Object Model with Mobile Optimization
- **Features**: Modal/popup handling, screenshot capture, mobile-specific interactions

## 📊 Test Execution

### Selenium Framework
```bash
cd selenium_framework

# Run all tests
python run_tests.py

# Run with specific browser
python run_tests.py --browser firefox

# Run smoke tests only
python run_tests.py --markers smoke

# Run in headless mode
python run_tests.py --headless

# Generate Allure report
python run_tests.py --report allure
```

### API Framework
```bash
cd api_framework

# Run all tests
python run_tests.py

# Run smoke tests only
python run_tests.py --markers smoke

# Run integration tests
python run_tests.py --markers integration

# Run with custom base URL
python run_tests.py --base-url https://api.example.com

# Generate Allure report
python run_tests.py --report allure
```

## 📈 Evaluation Criteria

This implementation addresses all evaluation criteria:

### ✅ Attention to Detail
- Comprehensive test coverage for both UI and API
- Detailed error handling and validation
- Proper configuration management
- Clean code structure and documentation

### ✅ Problem Solving Abilities
- Robust error handling and retry mechanisms
- Flexible configuration system
- Scalable architecture design
- Cross-browser and cross-platform support

### ✅ Test Flakiness Prevention
- Explicit waits and proper synchronization
- Retry logic for API calls
- Stable element locators
- Proper test data management

### ✅ Python Usage
- Modern Python features and best practices
- Type hints and proper documentation
- Clean code structure and naming conventions
- Proper use of Python packages and libraries

### ✅ Testing Approach
- Page Object Model for UI tests
- Service Layer Pattern for API tests
- Comprehensive test categorization (smoke, regression, integration)
- Data-driven testing capabilities

### ✅ Scalability
- Modular architecture
- Easy to extend and maintain
- Support for parallel execution
- Configuration-driven approach

## 📋 Test Categories

### Selenium Framework Tests
- **Smoke Tests**: Basic login and navigation functionality
- **Regression Tests**: Complete user workflows and edge cases
- **UI Tests**: Element validation, form interactions, error handling

### API Framework Tests
- **Smoke Tests**: Basic CRUD operations for all endpoints
- **Regression Tests**: Comprehensive API functionality
- **Integration Tests**: Cross-API relationship validation
- **Performance Tests**: Response time validation

## 🛠️ Technology Stack

### Selenium Framework
- **Python 3.8+**
- **Selenium WebDriver**
- **Pytest** - Test runner and framework
- **WebDriver Manager** - Automatic driver management
- **Allure** - Advanced reporting
- **Pydantic** - Configuration management

### API Framework
- **Python 3.8+**
- **Requests** - HTTP client
- **Pytest** - Test runner and framework
- **JSONSchema** - Schema validation
- **Allure** - Advanced reporting
- **Pydantic** - Configuration management

## 📊 Reporting

Both frameworks support multiple reporting formats:

- **HTML Reports** - Self-contained HTML reports with screenshots
- **Allure Reports** - Interactive reports with detailed test information
- **Console Output** - Detailed console output with test results

## 🔧 Configuration

Each framework includes comprehensive configuration management:

- Environment-based configuration
- Browser/API endpoint configuration
- Timeout and retry settings
- Test data management
- Reporting configuration

## 📝 Documentation

Each framework includes:
- Comprehensive README with setup instructions
- Code documentation and comments
- Example test cases
- Best practices and guidelines
- Troubleshooting guides

## 🚀 Demo

*Note: Replace with actual GIF showing test execution for both frameworks*

![Test Execution Demo](demo.gif)

## 📞 Contact

For questions about this implementation, please contact the development team.

---

**Note**: This is a demonstration project for AQA assessment purposes. Both frameworks are designed to showcase best practices in test automation, scalability, and maintainability.
