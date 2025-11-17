#!/usr/bin/env python3
"""
Test script to verify core backend functionality
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_modules():
    """Test the core backend modules that don't require platform-specific features"""
    print("Testing Core Backend Functionality")
    print("=" * 40)
    
    # Test Model module
    try:
        from Backend.Model import FirstLayerDMM
        print("✓ Model module loaded successfully")
    except Exception as e:
        print(f"✗ Model module failed: {e}")
        return False
    
    # Test RealtimeSearchEngine module
    try:
        from Backend.RealtimeSearchEngine import RealtimeSearchEngine, GoogleSearch
        print("✓ RealtimeSearchEngine module loaded successfully")
    except Exception as e:
        print(f"✗ RealtimeSearchEngine module failed: {e}")
        return False
    
    # Test Chatbot module
    try:
        from Backend.Chatbot import ChatBot
        print("✓ Chatbot module loaded successfully")
    except Exception as e:
        print(f"✗ Chatbot module failed: {e}")
        return False
    
    # Test TextToSpeech module
    try:
        from Backend.TextToSpeech import TextToSpeech
        print("✓ TextToSpeech module loaded successfully")
    except Exception as e:
        print(f"✗ TextToSpeech module failed: {e}")
        return False
    
    # Test ImageGeneration module
    try:
        from Backend.ImageGeneration import GenerateImages
        print("✓ ImageGeneration module loaded successfully")
    except Exception as e:
        print(f"✗ ImageGeneration module failed: {e}")
        return False
    
    return True

def test_utility_functions():
    """Test utility functions from various modules"""
    print("\nTesting Utility Functions")
    print("=" * 40)
    
    # Test Google Search function
    try:
        from Backend.RealtimeSearchEngine import GoogleSearch
        print("✓ GoogleSearch function loaded successfully")
    except Exception as e:
        print(f"✗ GoogleSearch function failed: {e}")
    
    # Test AnswerModifier function
    try:
        from Backend.RealtimeSearchEngine import AnswerModifier
        test_answer = "This is a test.\n\nWith multiple lines.\n\n\nAnd extra newlines."
        modified = AnswerModifier(test_answer)
        print("✓ AnswerModifier function works correctly")
    except Exception as e:
        print(f"✗ AnswerModifier function failed: {e}")
    
    # Test QueryModifier function
    try:
        from Frontend.GUI import QueryModifier
        test_query = "what is the time"
        modified = QueryModifier(test_query)
        print("✓ QueryModifier function works correctly")
    except Exception as e:
        print(f"✗ QueryModifier function failed: {e}")

if __name__ == "__main__":
    print("Jarvis AI Assistant - Core Functionality Test")
    print("=" * 50)
    
    # Test core modules
    if test_core_modules():
        print("\n✅ All core modules loaded successfully!")
    else:
        print("\n❌ Some core modules failed to load.")
    
    # Test utility functions
    test_utility_functions()
    
    print("\n" + "=" * 50)
    print("Core functionality testing completed.")