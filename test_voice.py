#!/usr/bin/env python3
"""
Simple test script to verify voice recognition is working
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_voice_recognition():
    """Test voice recognition functionality"""
    print("🎙️  Testing Voice Recognition")
    print("=" * 30)
    
    try:
        # Test importing the speech recognition module
        from Backend.SpeechToText import SpeechRecognition
        print("✅ Speech recognition module imported successfully")
        
        print("\n💡 Instructions:")
        print("   1. Speak clearly into your microphone")
        print("   2. Say something like 'Hello' or 'How are you?'")
        print("   3. The recognized text will appear below")
        print("   4. Press Ctrl+C to stop the test")
        print("\n📝 Listening for speech input...")
        
        # Try to recognize speech (this will open Chrome)
        recognized_text = SpeechRecognition()
        print(f"✅ Recognized text: {recognized_text}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⏹️  Test stopped by user")
        return True
    except Exception as e:
        print(f"❌ Voice recognition test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Jarvis AI Assistant - Voice Recognition Test")
    print("=" * 50)
    
    if test_voice_recognition():
        print(f"\n🎉 Voice recognition test completed!")
    else:
        print(f"\n❌ Voice recognition test failed!")

if __name__ == "__main__":
    main()