#!/usr/bin/env python3
"""
Health check script for VisionText API.
Exit codes:
  0 = healthy
  1 = unhealthy
"""
import sys
import urllib.request
import urllib.error
import time

def check_health(max_retries=3):
    """Check if the API is responding"""
    for attempt in range(max_retries):
        try:
            # Try localhost (internal container check)
            response = urllib.request.urlopen('http://127.0.0.1:8000/models', timeout=5)
            
            if response.status == 200:
                print("✓ Health check passed")
                return 0
            else:
                print(f"✗ HTTP {response.status}")
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            else:
                print(f"✗ Failed: {e}")
                return 1
    
    return 1

if __name__ == '__main__':
    sys.exit(check_health())

