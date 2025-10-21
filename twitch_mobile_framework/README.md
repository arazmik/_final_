# Twitch Mobile Test Framework

A specialized Selenium-based test automation framework for testing Twitch's mobile web application using Chrome mobile emulation.

## 🚀 Features

- **Chrome Mobile Emulation** - Uses Google Chrome's mobile emulator for authentic mobile testing
- **Modal/Popup Handling** - Automatic detection and handling of modals and popups
- **Screenshot Capture** - Automatic screenshots at key test steps
- **Page Object Model** - Clean separation of test logic and page elements
- **Comprehensive Reporting** - HTML and Allure reports with screenshots
- **Mobile-Optimized** - Specifically designed for mobile web testing

## 📋 Test Case Implementation

This framework implements the following test case:

1. **Navigate to** [https://m.twitch.tv/](https://m.twitch.tv/)
2. **Click** the search icon
3. **Input** "StarCraft II" in the search field
4. **Scroll down** 2 times
5. **Select** one streamer from the results
6. **Wait** for the streamer page to load completely
7. **Take a screenshot** of the loaded streamer page

### 🎯 Key Features

- ✅ **Mobile Emulation** - Uses Chrome's mobile emulator (iPhone 12 Pro by default)
- ✅ **Modal Handling** - Automatically handles modals and popups that appear before video loads
- ✅ **Screenshot Capture** - Takes screenshots at each step and final result
- ✅ **Robust Waiting** - Waits for page elements to load completely
- ✅ **Error Handling** - Comprehensive error handling and retry logic

## 📁 Project Structure

```
twitch_mobile_framework/
├── config/
│   ├── __init__.py
│   └── settings.py          # Mobile-specific configuration
├── core/
│   ├── __init__.py
│   ├── base_page.py         # Mobile-optimized base page class
│   └── driver_manager.py    # Chrome mobile emulation setup
├── pages/
│   ├── __init__.py
│   ├── twitch_home_page.py  # Twitch home page object
│   └── twitch_streamer_page.py # Twitch streamer page object
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures and configuration
│   └── test_twitch_mobile.py # Main test implementation
├── screenshots/             # Test screenshots
├── reports/                 # HTML test reports
├── allure-results/          # Allure test results
├── requirements.txt         # Python dependencies
├── pytest.ini             # Pytest configuration
├── run_tests.py           # Test runner script
├── env.example            # Environment variables example
└── README.md              # This file
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd twitch_mobile_framework
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
   # Edit .env file with your configuration if needed
   ```

## 🎯 Running Tests

### Run the main test case
```bash
python run_tests.py
```

### Run with specific options
```bash
# Run in headless mode
python run_tests.py --headless

# Use different mobile device
python run_tests.py --device "iPhone 13 Pro"

# Search for different term
python run_tests.py --search-term "League of Legends"

# Generate Allure report
python run_tests.py --report allure

# Run specific test markers
python run_tests.py --markers smoke
```

### Run with pytest directly
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_twitch_mobile.py::TestTwitchMobile::test_twitch_mobile_search_and_select_streamer

# Run with verbose output
pytest -v -s
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file based on `env.example`:

```env
# Mobile Browser Configuration
BROWSER=chrome
HEADLESS=false
MOBILE_EMULATION=true
DEVICE_NAME=iPhone 12 Pro

# Mobile Viewport Settings
MOBILE_WIDTH=390
MOBILE_HEIGHT=844

# Test Data
BASE_URL=https://m.twitch.tv
SEARCH_TERM=StarCraft II

# Screenshot Settings
SCREENSHOT_ON_FAILURE=true
SCREENSHOT_ON_SUCCESS=true
SCREENSHOTS_DIR=screenshots
```

### Supported Mobile Devices
The framework supports various mobile device emulations:
- iPhone 12 Pro (default)
- iPhone 13 Pro
- iPhone 14 Pro
- Samsung Galaxy S20
- Pixel 5
- And more...

## 📊 Test Reports

### HTML Report
```bash
python run_tests.py --report html
```

### Allure Report
```bash
python run_tests.py --report allure
```

## 🏗️ Framework Architecture

### Mobile Emulation
- Uses Chrome's built-in mobile emulation
- Configurable device profiles
- Authentic mobile user agent strings
- Mobile-optimized viewport settings

### Modal/Popup Handling
The framework automatically handles:
- Age verification modals
- Cookie consent popups
- Video loading overlays
- Login prompts
- Advertisements

### Page Object Model
Each page is represented by a class that encapsulates:
- Mobile-optimized element locators
- Touch-friendly interactions
- Mobile-specific wait strategies
- Screenshot capture methods

## 🧪 Test Implementation Details

### Main Test Flow
```python
def test_twitch_mobile_search_and_select_streamer():
    # 1. Navigate to Twitch mobile
    twitch_home_page.navigate_to_twitch()
    
    # 2. Click search icon
    twitch_home_page.click_search_icon()
    
    # 3. Input search term
    twitch_home_page.search_for_term("StarCraft II")
    
    # 4. Scroll down 2 times
    twitch_home_page.scroll_down_twice()
    
    # 5. Select streamer
    twitch_home_page.select_first_streamer()
    
    # 6. Wait for page load and take screenshot
    twitch_streamer_page.wait_for_page_to_load()
    twitch_streamer_page.take_streamer_screenshot()
```

### Screenshot Strategy
The framework captures screenshots at each step:
1. `01_twitch_home_page.png` - Initial page load
2. `02_search_icon_clicked.png` - After clicking search
3. `03_search_input.png` - After entering search term
4. `04_scrolled_down.png` - After scrolling
5. `05_streamer_selected.png` - After selecting streamer
6. `06_streamer_page_final.png` - Final loaded page

## 🚀 Demo GIF

![Twitch Mobile Test Execution Demo](demo.gif)

*Note: Replace with actual GIF showing test execution*

## 🔍 Troubleshooting

### Common Issues

1. **ChromeDriver not found**
   - Ensure WebDriver Manager is installed
   - Check internet connection for driver downloads

2. **Mobile emulation not working**
   - Verify Chrome browser is installed
   - Check mobile emulation settings in configuration

3. **Modals not being handled**
   - Check if modal selectors are up to date
   - Verify wait times are sufficient

4. **Screenshots not being captured**
   - Ensure screenshots directory exists
   - Check file permissions

### Debug Mode
```bash
# Run with verbose output
pytest -v -s

# Run single test with debug
pytest tests/test_twitch_mobile.py::TestTwitchMobile::test_twitch_mobile_search_and_select_streamer -v -s
```

## 📈 Best Practices

1. **Use Mobile Emulation** - Always test with mobile emulation enabled
2. **Handle Modals** - Implement robust modal/popup handling
3. **Take Screenshots** - Capture screenshots at key steps for debugging
4. **Wait for Elements** - Use explicit waits for mobile elements
5. **Test on Different Devices** - Test on various mobile device profiles
6. **Handle Network Issues** - Implement retry logic for network-dependent operations

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

---

**Note**: This framework is specifically designed for the Twitch mobile web application testing assignment and demonstrates mobile web automation best practices.
