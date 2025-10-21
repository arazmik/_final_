"""
API client for making HTTP requests with proper error handling and logging
"""
import json
import time
import logging
from typing import Dict, Any, Optional, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import settings


class APIClient:
    """HTTP client with retry logic and proper error handling"""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = settings.base_url
        self.timeout = settings.api_timeout
        self._setup_session()
        self._setup_logging()
    
    def _setup_session(self):
        """Configure session with retry strategy"""
        retry_strategy = Retry(
            total=settings.max_retries,
            backoff_factor=settings.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update(settings.default_headers)
    
    def _setup_logging(self):
        """Setup logging for API requests"""
        logging.basicConfig(level=getattr(logging, settings.log_level))
        self.logger = logging.getLogger(__name__)
    
    def _log_request(self, method: str, url: str, **kwargs):
        """Log API request details"""
        self.logger.info(f"{method.upper()} {url}")
        if 'json' in kwargs:
            self.logger.debug(f"Request body: {json.dumps(kwargs['json'], indent=2)}")
        if 'params' in kwargs:
            self.logger.debug(f"Request params: {kwargs['params']}")
    
    def _log_response(self, response: requests.Response):
        """Log API response details"""
        self.logger.info(f"Response: {response.status_code} {response.reason}")
        try:
            if response.headers.get('content-type', '').startswith('application/json'):
                self.logger.debug(f"Response body: {json.dumps(response.json(), indent=2)}")
        except (ValueError, json.JSONDecodeError):
            self.logger.debug(f"Response body: {response.text[:500]}...")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with logging and error handling"""
        url = f"{self.base_url}{endpoint}"
        
        # Add timeout if not specified
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        self._log_request(method, url, **kwargs)
        
        try:
            response = self.session.request(method, url, **kwargs)
            self._log_response(response)
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make GET request"""
        return self._make_request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, json_data: Optional[Dict] = None, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make POST request"""
        return self._make_request('POST', endpoint, json=json_data, data=data, **kwargs)
    
    def put(self, endpoint: str, json_data: Optional[Dict] = None, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make PUT request"""
        return self._make_request('PUT', endpoint, json=json_data, data=data, **kwargs)
    
    def patch(self, endpoint: str, json_data: Optional[Dict] = None, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make PATCH request"""
        return self._make_request('PATCH', endpoint, json=json_data, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request"""
        return self._make_request('DELETE', endpoint, **kwargs)
    
    def head(self, endpoint: str, **kwargs) -> requests.Response:
        """Make HEAD request"""
        return self._make_request('HEAD', endpoint, **kwargs)
    
    def options(self, endpoint: str, **kwargs) -> requests.Response:
        """Make OPTIONS request"""
        return self._make_request('OPTIONS', endpoint, **kwargs)
    
    def close(self):
        """Close the session"""
        self.session.close()
