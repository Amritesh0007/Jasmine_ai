from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import speech_recognition as sr
import os
import platform
from dotenv import dotenv_values
from googletrans import Translator
try:
    import pyaudio
    import wave
    import threading
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False
    print("PyAudio not available. Audio recording functionality will be limited.")
import time
from Backend.GeminiAPI import speech_to_text

# Load environment variables with absolute path
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
env_vars = dotenv_values(env_path)

InputLanguage = env_vars.get("InputLanguage", "en")

mt = Translator()

# HTML content with speech recognition
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Inject Input Language
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Save HTML to file
os.makedirs("Data", exist_ok=True)
with open("Data/Voice.html", "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Construct local file URL
current_dir = os.getcwd()
Link = f"{current_dir}/Data/Voice.html"

# Set Chrome options
chrome_options = Options()
# Use default Chrome instead of hardcoded Chrome Beta path
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")  # Modern headless mode
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36")

# Platform-specific Chrome executable path
system = platform.system().lower()
if system == "darwin":  # macOS
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif system == "windows":
    # Common Windows Chrome paths
    possible_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            chrome_options.binary_location = path
            break

# Initialize driver with the installed ChromeDriver
driver = None
try:
    # Use the installed ChromeDriver
    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("ChromeDriver successfully initialized")
except Exception as e:
    print(f"Error initializing ChromeDriver: {e}")
    print("Trying to use ChromeDriver from PATH...")
    
    # Try without specifying path (assumes chromedriver is in PATH)
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("ChromeDriver successfully initialized from PATH")
    except Exception as e2:
        print(f"Error initializing ChromeDriver from PATH: {e2}")
        print("Speech recognition may not work. Please ensure Chrome is installed.")
        # Create a dummy driver object that will show an error message
        driver = None

# Setup temp status path
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation

def SpeechRecognition():
    # Check if driver is available
    if driver is None:
        print("Error: ChromeDriver not available. Speech recognition disabled.")
        return "Speech recognition not available. Please install ChromeDriver."
    
    driver.get("file:///" + Link)
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text:
                driver.find_element(By.ID, "end").click()
                if InputLanguage and (InputLanguage.lower() == "en" or "en" in InputLanguage.lower()):
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            pass

# Gemini ASR Implementation

def GeminiSpeechRecognition(audio_file_path=None):
    """Speech recognition using Google Gemini API"""
    if audio_file_path:
        # Use provided audio file
        try:
            transcribed_text = speech_to_text(audio_file_path)
            if transcribed_text:
                print(f"Transcribed text: {transcribed_text}")
                return QueryModifier(transcribed_text)
            else:
                print("Failed to transcribe audio")
                return ""
        except Exception as e:
            print(f"Error in Gemini ASR: {e}")
            return ""
    else:
        # Try to record audio if PyAudio is available
        try:
            import pyaudio
            import wave
            import threading
            
            print("Audio recording functionality is available but not implemented in this simplified version.")
            print("Please provide an audio file for transcription.")
            return ""
        except ImportError:
            print("Audio recording not available. Please provide an audio file for transcription.")
            return ""

# Run the assistant
if __name__ == "__main__":
    while True:
        # You can switch between the two implementations
        print("Choose ASR method:")
        print("1. Web Speech Recognition (default)")
        print("2. Gemini ASR")
        choice = input("Enter choice (1 or 2): ")
        
        if choice == "2":
            # For demo, we'll use a placeholder
            Text = GeminiSpeechRecognition("Data/sample_audio.wav")
        else:
            Text = SpeechRecognition()
        print(Text)