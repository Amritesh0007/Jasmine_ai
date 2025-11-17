# Jasmine AI Assistant

Welcome to your personal AI assistant! This application provides voice and text-based interaction with advanced AI capabilities.

## Current Status

✅ **Application Running Successfully**
- GUI interface is active
- Text-based interaction works
- Voice recognition is now working!
- Application automation (open/close apps, YouTube search) functional
- AI chat and real-time search working

## How to Use

### Method 1: Voice Interface (Recommended)
1. Run the main application:
   ```bash
   python3 Main.py
   ```
2. Activate microphone:
   ```bash
   python3 toggle_microphone.py true
   ```
3. Speak clearly into your microphone when the Chrome window opens

### Method 2: Text Interface
```bash
cd /Users/amriteshkumar/Jarvis/jarvis-ai-assistant
python3 text_interface.py
```

Examples of what you can do:
- "Hello, how are you?" (General conversation)
- "Open notepad" (Opens TextEdit on macOS)
- "Play some music" (Opens YouTube search)
- "What's the weather like today?" (Real-time search)
- "Write an application for sick leave" (Content generation)

## Features

### 🤖 AI Capabilities
- General conversation with AI chatbot
- Real-time information search
- Content generation (letters, applications, etc.)

### ⚙️ Automation
- Open/close applications
- Play music on YouTube
- Search Google
- System controls (Windows only)

### 🎵 Supported Commands
- "Open [app name]" (notepad, chrome, calculator, etc.)
- "Close [app name]"
- "Play [music/query]"
- "Search for [topic]"
- "Write [content type]"

## Troubleshooting

### Voice Recognition Issues
If voice recognition stops working:
1. Check that the microphone is activated:
   ```bash
   cat Frontend/Files/Mic.data
   ```
   Should show "True"

2. Restart the application if needed

### Application Opening Issues
If apps don't open, try using more specific names:
- "Open TextEdit" instead of "Open notepad"
- "Open Google Chrome" instead of "Open chrome"

## File Structure
- `Main.py` - Main application entry point
- `text_interface.py` - Text-based interface
- `toggle_microphone.py` - Control voice recognition
- `Backend/` - AI and automation modules
- `Frontend/` - GUI interface
- `Data/` - Chat logs and temporary files

## Exiting the Application
- For GUI: Close the application window
- For text interface: Type 'exit' or press Ctrl+C

## Need Help?
Check `USAGE_INSTRUCTIONS.md` for detailed usage information.
