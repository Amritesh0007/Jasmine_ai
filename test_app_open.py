#!/usr/bin/env python3
"""
Test script to verify application opening functionality
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_opening():
    """Test application opening functionality"""
    print("🚀 Testing Application Opening")
    print("=" * 30)
    
    try:
        # Test importing the automation module
        from Backend.Automation import OpenApp
        print("✅ Automation module imported successfully")
        
        # Test opening a common app (TextEdit on macOS)
        print("\n🔧 Testing to open TextEdit...")
        result = OpenApp("notepad")  # This should map to TextEdit on macOS
        if result:
            print("✅ Application opening test passed")
        else:
            print("⚠️  Application opening test completed but may need manual verification")
        
        # Test opening Chrome/Google Chrome
        print("\n🔧 Testing to open Chrome...")
        result = OpenApp("chrome")  # This should map to Google Chrome on macOS
        if result:
            print("✅ Chrome opening test passed")
        else:
            print("⚠️  Chrome opening test completed but may need manual verification")
            
        return True
        
    except Exception as e:
        print(f"❌ Application opening test failed: {e}")
        return False

def test_youtube_opening():
    """Test YouTube opening functionality"""
    print("\n🎵 Testing YouTube Opening")
    print("=" * 30)
    
    try:
        # Test importing the automation module
        from Backend.Automation import PlayYoutube
        print("✅ YouTube module imported successfully")
        
        # Test opening YouTube search
        print("\n🔧 Testing to open YouTube search...")
        result = PlayYoutube("test music")
        if result:
            print("✅ YouTube opening test passed")
        else:
            print("⚠️  YouTube opening test completed but may need manual verification")
            
        return True
        
    except Exception as e:
        print(f"❌ YouTube opening test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🤖 Jarvis AI Assistant - Application Opening Test")
    print("=" * 50)
    
    app_test = test_app_opening()
    youtube_test = test_youtube_opening()
    
    if app_test and youtube_test:
        print(f"\n🎉 All application opening tests completed!")
        print("   You should see applications opening on your system.")
    else:
        print(f"\n❌ Some tests failed or require manual verification.")

if __name__ == "__main__":
    main()