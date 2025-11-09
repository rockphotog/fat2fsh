#!/usr/bin/env python3
"""
Test script to verify the fat2fsh setup and basic functionality.
"""

import sys
import json
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import requests
        import click
        import pydantic
        print("✓ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_api_connection():
    """Test connection to the FAT API."""
    try:
        import requests
        
        # Test basic connectivity to the FAT API
        url = "https://fat.kote.helsedirektoratet.no"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✓ FAT API is reachable")
            return True
        else:
            print(f"✗ FAT API returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error connecting to FAT API: {e}")
        return False

def test_directories():
    """Test that output directories can be created."""
    try:
        test_dir = Path("test_output")
        fat_dir = test_dir / "fat"
        fsh_dir = test_dir / "fsh"
        
        # Create directories
        fat_dir.mkdir(parents=True, exist_ok=True)
        fsh_dir.mkdir(parents=True, exist_ok=True)
        
        # Test writing files
        test_file = fat_dir / "test.json"
        with open(test_file, 'w') as f:
            json.dump({"test": "data"}, f)
        
        # Clean up
        test_file.unlink()
        fsh_dir.rmdir()
        fat_dir.rmdir()
        test_dir.rmdir()
        
        print("✓ Directory creation and file writing works")
        return True
        
    except Exception as e:
        print(f"✗ Error with directories: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing fat2fsh setup...\n")
    
    tests = [
        ("Import test", test_imports),
        ("API connectivity test", test_api_connection),
        ("Directory test", test_directories)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The setup is working correctly.")
        print("\nNext steps:")
        print("1. Find valid code system IDs from the FAT API documentation")
        print("2. Run: python fat2fsh.py -c <code-system-id> -v")
    else:
        print("❌ Some tests failed. Please check the setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()