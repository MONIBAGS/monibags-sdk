"""
MoniBags SDK Core Implementation
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
from .exceptions import MoniBagsException, RateLimitError, APIError


class MoniBagsSDK:
    """SDK for MoniBags Twitter History Checker API"""
    
    def __init__(self, base_url: str = "https://monibags.xyz"):
        """
        Initialize SDK
        
        Args:
            base_url: Base URL of MoniBags API (default: https://monibags.xyz)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'MoniBags-SDK/1.0'
        })
    
    def check_username_history(self, username: str, timeout: int = 30) -> Dict:
        """
        Check username history for a Twitter account
        
        Args:
            username: Twitter username (with or without @)
            timeout: Request timeout in seconds
        
        Returns:
            dict: API response with history data
        
        Raises:
            RateLimitError: If rate limit is exceeded
            APIError: If API returns an error
        """
        # Clean username
        username = username.lstrip('@')
        
        try:
            # Make API request
            response = self.session.post(
                f"{self.base_url}/api/check-username-history",
                json={'username': username},
                timeout=timeout
            )
            
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded. Please wait before making another request.")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise APIError(f"API returned status code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            raise MoniBagsException(f"Request timed out after {timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise MoniBagsException(f"Request failed: {str(e)}")
    
    def analyze_profile(self, username: str, timeout: int = 60) -> Dict:
        """
        Full profile analysis including network and interactions
        
        Args:
            username: Twitter username
            timeout: Request timeout in seconds
        
        Returns:
            dict: Full analysis results
        
        Raises:
            APIError: If API returns an error
        """
        username = username.lstrip('@')
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/analyze",
                json={'username': username},
                timeout=timeout
            )
            
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise APIError(f"API returned status code {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise MoniBagsException(f"Request failed: {str(e)}")
    
    def batch_check(self, usernames: List[str], delay: float = 2.0, 
                   progress_callback: Optional[callable] = None) -> List[Dict]:
        """
        Check multiple usernames with delay between requests
        
        Args:
            usernames: List of Twitter usernames
            delay: Delay between requests in seconds
            progress_callback: Optional callback function for progress updates
        
        Returns:
            list: Results for each username
        """
        results = []
        total = len(usernames)
        
        for i, username in enumerate(usernames):
            if progress_callback:
                progress_callback(i + 1, total, username)
            else:
                print(f"Checking {i+1}/{total}: @{username}")
            
            try:
                result = self.check_username_history(username)
                result['username'] = username
                result['timestamp'] = datetime.now().isoformat()
                results.append(result)
            except Exception as e:
                results.append({
                    'username': username,
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
            
            # Delay between requests (except for last one)
            if i < total - 1:
                time.sleep(delay)
        
        return results
    
    def get_rate_limit_status(self) -> Dict:
        """
        Get current rate limit status
        
        Returns:
            dict: Rate limit information
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/rate-limit",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Failed to get rate limit status'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def format_result(self, result: Dict) -> str:
        """
        Format result for pretty printing
        
        Args:
            result: API response
        
        Returns:
            str: Formatted result
        """
        output = []
        output.append("="*50)
        
        if result.get('success'):
            data = result.get('data', {})
            output.append(f"Username: @{data.get('current_username', 'unknown')}")
            output.append(f"Status: {'CLEAN ✅' if data.get('is_clean') else 'CHANGES DETECTED ⚠️'}")
            
            if data.get('total_changes', 0) > 0:
                output.append(f"Total Changes: {data['total_changes']}")
                output.append("\nPrevious Usernames:")
                for item in data.get('history', []):
                    output.append(f"  • {item}")
            
            insights = data.get('insights', [])
            if insights:
                output.append("\nInsights:")
                for insight in insights:
                    output.append(f"  {insight}")
        else:
            output.append(f"Error: {result.get('error', 'Unknown error')}")
            if result.get('message'):
                output.append(f"Message: {result['message']}")
        
        output.append("="*50)
        return "\n".join(output)
    
    def export_results(self, results: List[Dict], filename: str, format: str = 'json') -> None:
        """
        Export results to file
        
        Args:
            results: List of results to export
            filename: Output filename
            format: Export format ('json' or 'csv')
        """
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
        elif format == 'csv':
            import csv
            with open(filename, 'w', newline='') as f:
                if results:
                    fieldnames = ['username', 'is_clean', 'total_changes', 'history', 'timestamp']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for result in results:
                        if result.get('success'):
                            data = result.get('data', {})
                            writer.writerow({
                                'username': result.get('username', ''),
                                'is_clean': data.get('is_clean', ''),
                                'total_changes': data.get('total_changes', 0),
                                'history': ', '.join(data.get('history', [])),
                                'timestamp': result.get('timestamp', '')
                            })
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"Results exported to {filename}")