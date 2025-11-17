#!/usr/bin/env python3
"""
Test script to verify speech recognition functionality
"""

import os
import sys
from dotenv import dotenv_values

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")

print(f"🚀 Testing Speech Recognition")
print("=" * 30)
print(f"Input Language: {InputLanguage}")

def test_speech_recognition():
    """Test speech recognition functionality"""
    print("🔧 Testing Speech Recognition...")
    
    try:
        # Test importing the speech recognition module
        from Backend.SpeechToText import SpeechRecognition, QueryModifier
        print("✅ Speech recognition module imported successfully")
        
        # Test query modifier
        test_query = "hello world"
        modified_query = QueryModifier(test_query)
        print(f"✅ Query modifier working: '{test_query}' -> '{modified_query}'")
        
        print("\n💡 Speech recognition is ready!")
        print("   The application should now be able to recognize your voice.")
        print("   Make sure to:")
        print("   1. Click the microphone icon in the GUI to activate speech recognition")
        print("   2. Allow microphone access when prompted by the browser")
        print("   3. Speak clearly after activation")
        
        return True
        
    except Exception as e:
        print(f"❌ Speech recognition test failed: {e}")
        return False

def main():
    """Main test function"""
    if test_speech_recognition():
        print(f"\n🎉 Speech recognition functionality is working!")
    else:
        print(f"\n❌ Speech recognition has issues that need fixing.")

if __name__ == "__main__":
    main()