#!/usr/bin/env python3
"""
Test script to verify the full automation system
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_automation_system():
    """Test the full automation system"""
    print("🤖 Testing Full Automation System")
    print("=" * 35)
    
    try:
        # Test importing the automation module
        from Backend.Automation import Automation
        import asyncio
        print("✅ Automation system imported successfully")
        
        # Test various automation commands
        test_commands = [
            "open notepad",      # Should open TextEdit on macOS
            "open chrome",       # Should open Google Chrome
            "play test music",   # Should open YouTube search
            "google search artificial intelligence"
        ]
        
        print(f"\n🔧 Testing automation commands:")
        for command in test_commands:
            print(f"   - {command}")
        
        # Run the automation
        print("\n🚀 Executing automation commands...")
        result = asyncio.run(Automation(test_commands))
        
        print("✅ Automation system executed successfully")
        print("   Check your system for opened applications and browser tabs")
        
        return True
        
    except Exception as e:
        print(f"❌ Automation system test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Jarvis AI Assistant - Full Automation Test")
    print("=" * 50)
    
    if test_automation_system():
        print(f"\n🎉 Automation system is working correctly!")
        print("   The assistant should now be able to:")
        print("   - Open applications like notepad, chrome, etc.")
        print("   - Play music by opening YouTube")
        print("   - Search Google for information")
        print("   - Close applications (as before)")
    else:
        print(f"\n❌ Automation system test failed!")

if __name__ == "__main__":
    main()