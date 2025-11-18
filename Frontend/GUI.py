# GUI.py - Frontend for Jarvis AI Assistant
"""
GUI Module for Jarvis AI Assistant
Handles the graphical user interface with fallback mechanisms
"""

from dotenv import dotenv_values
import sys
import os

# Load environment variables
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
old_chat_message = ""

# Directory paths - use absolute path based on script location
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
GraphicsDirPath = os.path.join(base_dir, "Frontend", "Graphics")
TempDirPath = os.path.join(base_dir, "Frontend", "Files")

# Utility functions
def AnswerModifier(Answer):
    """Clean up answer text by removing extra newlines"""
    lines = Answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    """Format query with proper punctuation and capitalization"""
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ['how','what','who','where','when','why','which','whom','can you',"what's", "where's","how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + '.'
        else:
            new_query += '.'

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    """Set microphone status in data file"""
    try:
        with open(os.path.join(TempDirPath, 'Mic.data'), 'w', encoding='utf-8') as file:
            file.write(Command)
    except Exception as e:
        print(f"Error setting microphone status: {e}")

def GetMicrophoneStatus():
    """Get microphone status from data file"""
    try:
        with open(os.path.join(TempDirPath, 'Mic.data'), 'r', encoding='utf-8') as file:
            Status = file.read().strip()
        return Status
    except FileNotFoundError:
        return "False"

def SetAsssistantStatus(Status):
    """Set assistant status in data file"""
    try:
        with open(os.path.join(TempDirPath, 'Status.data'), 'w', encoding='utf-8') as file:
            file.write(Status)
    except Exception as e:
        print(f"Error setting assistant status: {e}")

def GetAssistantStatus():
    """Get assistant status from data file"""
    try:
        with open(os.path.join(TempDirPath, 'Status.data'), 'r', encoding='utf-8') as file:
            Status = file.read()
        return Status
    except FileNotFoundError:
        return "Available..."

def MicButtonInitiated():
    """Set microphone to initiated state"""
    SetMicrophoneStatus("False")

def MicButtonClosed():
    """Set microphone to closed state"""
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    """Get full path to graphics file"""
    return os.path.join(GraphicsDirPath, Filename)

def TempDirectoryPath(Filename):
    """Get full path to temp file"""
    return os.path.join(TempDirPath, Filename)

def ShowTextToScreen(Text):
    """Show text on screen by writing to responses file"""
    try:
        with open(os.path.join(TempDirPath, 'Responses.data'), 'w', encoding='utf-8') as file:
            file.write(Text)
    except Exception as e:
        print(f"Error showing text to screen: {e}")

def GraphicalUserInterface():
    """
    Main GUI function that creates and runs the application window
    Returns False if GUI is not available
    """
    # Try to import PyQt6 (better ARM64 support)
    try:
        from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QPushButton
        from PyQt6.QtGui import QFont, QMovie
        from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal, QEasingCurve, QPropertyAnimation
        from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
        from PyQt6.QtMultimediaWidgets import QVideoWidget
        
        print("Starting Jasmine AI Assistant GUI with PyQt6...")
        
        # Create the application
        app = QApplication([])
        
        # Create a main window with futuristic styling
        window = QWidget()
        window.setWindowTitle("JASMINE AI ASSISTANT")
        window.setGeometry(50, 50, 900, 700)  # Adjusted size to fit better on screen
        
        # Futuristic gradient background
        window.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #000428,
                stop: 0.5 #004e92,
                stop: 1 #000428
            );
            color: #00ffcc;
        """)
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section with animated elements
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            background-color: rgba(0, 15, 35, 200);
            border: 2px solid qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #00ffcc,
                stop: 0.5 #ff00ff,
                stop: 1 #00ffcc
            );
            border-radius: 20px;
            padding: 20px;
        """)
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(15)
        
        # Animated title with gradient text effect and pulsing animation
        title = QLabel("JASMINE AI ASSISTANT")
        title.setStyleSheet("""
            font-size: 32px; 
            font-weight: 900; 
            color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #00ffcc,
                stop: 0.5 #ff00ff,
                stop: 1 #00ffcc
            );
            text-align: center;
            background-color: transparent;
            letter-spacing: 2px;
            font-family: 'Arial Black', sans-serif;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add animation to title
        try:
            title_animation = QPropertyAnimation(title, b"styleSheet")
            title_animation.setDuration(2000)
            title_animation.setStartValue("""
            font-size: 32px; 
            font-weight: 900; 
            color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #00ffcc,
                stop: 0.5 #ff00ff,
                stop: 1 #00ffcc
            );
            text-align: center;
            background-color: transparent;
            letter-spacing: 2px;
            font-family: 'Arial Black', sans-serif;
        """)
            title_animation.setEndValue("""
            font-size: 32px; 
            font-weight: 900; 
            color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #ff00ff,
                stop: 0.5 #00ffcc,
                stop: 1 #ff00ff
            );
            text-align: center;
            background-color: transparent;
            letter-spacing: 2px;
            font-family: 'Arial Black', sans-serif;
        """)
            title_animation.setLoopCount(-1)
            title_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            title_animation.start()
        except Exception as e:
            print(f"Title animation error: {e}")
        
        header_layout.addWidget(title)
        
        # Subtitle with futuristic font and animated effect
        subtitle = QLabel("ADVANCED NEURAL PROCESSING SYSTEM")
        subtitle.setStyleSheet("""
            font-size: 16px; 
            color: #74ee15;
            text-align: center;
            background-color: transparent;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            letter-spacing: 1px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add animation to subtitle
        try:
            subtitle_animation = QPropertyAnimation(subtitle, b"styleSheet")
            subtitle_animation.setDuration(1500)
            subtitle_animation.setStartValue("""
            font-size: 16px; 
            color: #74ee15;
            text-align: center;
            background-color: transparent;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            letter-spacing: 1px;
        """)
            subtitle_animation.setEndValue("""
            font-size: 16px; 
            color: #00ffff;
            text-align: center;
            background-color: transparent;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            letter-spacing: 1px;
        """)
            subtitle_animation.setLoopCount(-1)
            subtitle_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            subtitle_animation.start()
        except Exception as e:
            print(f"Subtitle animation error: {e}")
        
        header_layout.addWidget(subtitle)
        
        # Animated status indicators with pulsing effect
        status_layout = QHBoxLayout()
        status_layout.setSpacing(20)
        
        # Custom animated label class
        class AnimatedLabel(QLabel):
            def __init__(self, text, color, parent=None):
                super().__init__(text, parent)
                self.color = color
                try:
                    self.animation = QPropertyAnimation(self, b"styleSheet")
                    self.animation.setDuration(1000)
                    self.animation.setStartValue(f"""
                    font-size: 14px;
                    color: {color};
                    font-weight: bold;
                    background-color: transparent;
                    padding: 8px;
                    border-radius: 8px;
                """)
                    self.animation.setEndValue(f"""
                    font-size: 14px;
                    color: #ffffff;
                    font-weight: bold;
                    background-color: {color};
                    padding: 8px;
                    border-radius: 8px;
                """)
                    self.animation.setLoopCount(-1)
                    self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
                    self.setStyleSheet(f"""
                    font-size: 14px;
                    color: {color};
                    font-weight: bold;
                    background-color: transparent;
                    padding: 8px;
                    border-radius: 8px;
                """)
                    self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.animation.start()
                except Exception as e:
                    print(f"Indicator animation error: {e}")
                    self.setStyleSheet(f"""
                    font-size: 14px;
                    color: {color};
                    font-weight: bold;
                    background-color: transparent;
                    padding: 8px;
                    border-radius: 8px;
                """)
                    self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create animated status indicators
        indicators = [
            ("● ONLINE", "#00ff00"),
            ("● VOICE ACTIVE", "#ffcc00"),
            ("● NEURAL NET", "#ff00ff"),
            ("● SECURITY", "#00ffff")
        ]
        
        for text, color in indicators:
            indicator = AnimatedLabel(text, color)
            status_layout.addWidget(indicator)
        
        header_layout.addLayout(status_layout)
        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)
        
        # Create media frame with enhanced futuristic design
        media_frame = QFrame()
        media_frame.setStyleSheet("""
            background-color: rgba(0, 5, 20, 200);
            border: 2px solid qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #00ffff,
                stop: 0.5 #ff00ff,
                stop: 1 #00ffff
            );
            border-radius: 25px;
            padding: 25px;
        """)
        media_layout = QVBoxLayout()
        media_layout.setContentsMargins(15, 15, 15, 15)
        
        # Try to use video player, fallback to GIF if it fails
        try:
            # Video player for MP4 with enhanced styling
            video_widget = QVideoWidget()
            video_widget.setStyleSheet("""
                background-color: rgba(0, 0, 0, 100);
                border: 2px solid #00ffff;
                border-radius: 20px;
                min-height: 250px;
                min-width: 250px;
            """)
            
            media_player = QMediaPlayer()
            audio_output = QAudioOutput()
            media_player.setAudioOutput(audio_output)
            media_player.setVideoOutput(video_widget)
            
            mp4_path = GraphicsDirectoryPath("jasmine.mp4")
            print(f"Loading MP4 from: {mp4_path}")
            print(f"MP4 file exists: {os.path.exists(mp4_path)}")
            
            if os.path.exists(mp4_path):
                # Set the video source using QUrl
                media_player.setSource(QUrl.fromLocalFile(mp4_path))
                # Set to loop playback
                media_player.setLoops(-1)  # Infinite loops
                # Start playing
                media_player.play()
                print("MP4 video loaded and playing successfully")
                media_layout.addWidget(video_widget)
            else:
                print("MP4 file not found!")
                # Fallback to a label if video file is missing
                fallback_label = QLabel("JASMINE AI\n[VIDEO FILE MISSING]")
                fallback_label.setStyleSheet("""
                    font-size: 24px;
                    color: #ff3300;
                    background-color: rgba(0, 0, 0, 180);
                    border: 2px dashed #ff3300;
                    border-radius: 20px;
                    padding: 60px;
                    font-weight: 900;
                    font-family: 'Courier New', monospace;
                """)
                fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                media_layout.addWidget(fallback_label)
                
        except Exception as e:
            print(f"Error initializing video player, falling back to GIF: {e}")
            # Fallback to GIF with enhanced styling
            gif_label = QLabel()
            gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            gif_label.setStyleSheet("""
                background-color: rgba(0, 0, 0, 100);
                border: 2px solid #00ffff;
                border-radius: 20px;
                min-height: 250px;
                min-width: 250px;
            """)
            
            gif_path = GraphicsDirectoryPath("Jarvis.gif")
            print(f"Loading GIF from: {gif_path}")
            print(f"GIF file exists: {os.path.exists(gif_path)}")
            
            if os.path.exists(gif_path):
                gif_movie = QMovie(gif_path)
                if gif_movie.isValid():
                    print("GIF movie loaded successfully")
                    gif_label.setMovie(gif_movie)
                    gif_movie.start()
                else:
                    print(f"GIF movie is not valid. Error: {gif_movie.lastError()}")
                    # Fallback text if GIF fails to load
                    gif_label.setText("JASMINE AI\n[ANIMATION LOADING...]")
                    gif_label.setStyleSheet("""
                        font-size: 24px;
                        color: #00ffcc;
                        background-color: rgba(0, 0, 0, 180);
                        border: 2px dashed #00ffcc;
                        border-radius: 20px;
                        padding: 60px;
                        font-weight: 900;
                        font-family: 'Courier New', monospace;
                    """)
            else:
                print("GIF file not found!")
                # Fallback text if GIF file is missing
                gif_label.setText("JASMINE AI\n[GIF FILE MISSING]")
                gif_label.setStyleSheet("""
                    font-size: 24px;
                    color: #ff3300;
                    background-color: rgba(0, 0, 0, 180);
                    border: 2px dashed #ff3300;
                    border-radius: 20px;
                    padding: 60px;
                    font-weight: 900;
                    font-family: 'Courier New', monospace;
                """)
                
            media_layout.addWidget(gif_label)
        
        media_frame.setLayout(media_layout)
        main_layout.addWidget(media_frame)
        
        # Create animated buttons with futuristic design
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Custom button class for animated effects
        class FuturisticButton(QPushButton):
            def __init__(self, text, parent=None):
                super().__init__(text, parent)
                self.setStyleSheet("""
                    QPushButton {
                        background-color: qlineargradient(
                            x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 #001f3f,
                            stop: 1 #0074D9
                        );
                        color: #00ffcc;
                        border: 2px solid #00ffff;
                        border-radius: 15px;
                        padding: 12px 20px;
                        font-size: 16px;
                        font-weight: bold;
                        font-family: 'Courier New', monospace;
                    }
                    QPushButton:hover {
                        background-color: qlineargradient(
                            x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 #00ffff,
                            stop: 1 #0074D9
                        );
                        border: 2px solid #ff00ff;
                        color: #ffffff;
                    }
                    QPushButton:pressed {
                        background-color: qlineargradient(
                            x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 #ff00ff,
                            stop: 1 #001f3f
                        );
                        border: 2px solid #00ffcc;
                        color: #ffffff;
                    }
                """)
        
        # Create buttons
        mic_button = FuturisticButton("🎤 TOGGLE MIC")
        gemini_asr_button = FuturisticButton("🎙️ GEMINI ASR")
        settings_button = FuturisticButton("⚙️ SETTINGS")
        exit_button = FuturisticButton("❌ EXIT")
        
        button_layout.addWidget(mic_button)
        button_layout.addWidget(gemini_asr_button)
        button_layout.addWidget(settings_button)
        button_layout.addWidget(exit_button)
        
        main_layout.addLayout(button_layout)
        
        # Create instructions frame with animated elements
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("""
            background-color: rgba(0, 15, 35, 200);
            border: 2px solid qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #ff00ff,
                stop: 0.5 #00ffff,
                stop: 1 #ff00ff
            );
            border-radius: 20px;
            padding: 20px;
        """)
        instructions_layout = QVBoxLayout()
        instructions_layout.setSpacing(15)
        
        # Instructions title
        instructions_title = QLabel("SYSTEM COMMANDS")
        instructions_title.setStyleSheet("""
            font-size: 20px;
            color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #ff00ff,
                stop: 0.5 #00ffff,
                stop: 1 #ff00ff
            );
            font-weight: 900;
            text-align: center;
            background-color: transparent;
            font-family: 'Courier New', monospace;
            letter-spacing: 1px;
        """)
        instructions_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_layout.addWidget(instructions_title)
        
        # Instructions with futuristic styling
        instructions = QLabel(
            "🎙️  SPEAK: 'Open Chrome' or 'Play music'\n" +
            "🔊  AUDIO: Real-time neural voice processing\n" +
            "⚡  SPEED: Quantum response in milliseconds\n" +
            "🔒  SECURITY: AES-256 encrypted\n" +
            "🌐  CONNECT: Internet connectivity\n\n" +
            "Close window to terminate assistant"
        )
        instructions.setStyleSheet("""
            font-size: 14px; 
            line-height: 1.6;
            color: #00ccff;
            background-color: transparent;
            font-family: 'Courier New', monospace;
            letter-spacing: 0.5px;
        """)
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        instructions_layout.addWidget(instructions)
        
        instructions_frame.setLayout(instructions_layout)
        main_layout.addWidget(instructions_frame)
        
        # Create system info frame with enhanced design
        system_frame = QFrame()
        system_frame.setStyleSheet("""
            background-color: rgba(0, 5, 20, 200);
            border: 2px solid qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #74ee15,
                stop: 0.5 #00ffcc,
                stop: 1 #74ee15
            );
            border-radius: 15px;
            padding: 15px;
        """)
        system_layout = QVBoxLayout()
        system_layout.setSpacing(10)
        
        # System info with enhanced styling
        system_info = QLabel(
            f"👤 USER: {Assistantname or 'USER'} | " +
            f"💻 PLATFORM: {sys.platform.upper()} | " +
            "🔧 FRAMEWORK: PyQt6 | " +
            "📡 STATUS: ACTIVE"
        )
        system_info.setStyleSheet("""
            font-size: 12px;
            color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #74ee15,
                stop: 0.5 #00ffcc,
                stop: 1 #74ee15
            );
            background-color: transparent;
            text-align: center;
            font-family: 'Courier New', monospace;
            letter-spacing: 0.5px;
        """)
        system_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        system_layout.addWidget(system_info)
        
        system_frame.setLayout(system_layout)
        main_layout.addWidget(system_frame)
        
        window.setLayout(main_layout)
        window.show()
        
        # Function to handle Gemini ASR button click
        def start_gemini_asr():
            print("Starting Gemini ASR...")
            try:
                # Import and call the actual Gemini ASR function
                from Backend.SpeechToText import GeminiSpeechRecognition
                result = GeminiSpeechRecognition()
                
                # Show the result in a message box
                from PyQt6.QtWidgets import QMessageBox
                msg = QMessageBox()
                msg.setWindowTitle("Gemini ASR Result")
                if result:
                    msg.setText(f"Transcribed text:\n{result}")
                else:
                    msg.setText("Failed to transcribe audio or no speech detected.")
                msg.setStyleSheet("""
                    background-color: #001f3f;
                    color: #00ffcc;
                    font-family: 'Courier New', monospace;
                """)
                msg.exec()
            except Exception as e:
                print(f"Error in Gemini ASR: {e}")
                from PyQt6.QtWidgets import QMessageBox
                msg = QMessageBox()
                msg.setWindowTitle("Gemini ASR Error")
                msg.setText(f"Error occurred during speech recognition:\n{str(e)}")
                msg.setStyleSheet("""
                    background-color: #001f3f;
                    color: #00ffcc;
                    font-family: 'Courier New', monospace;
                """)
                msg.exec()
        
        # Connect button signals
        exit_button.clicked.connect(app.quit)
        gemini_asr_button.clicked.connect(start_gemini_asr)
        
        print("GUI started successfully.")
        print("The application is now running. Close the GUI window to exit.")
        
        # Run the application
        return app.exec()
        
    except ImportError as e:
        # Try PyQt5 as fallback
        try:
            from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QPushButton
            from PyQt5.QtGui import QMovie, QPixmap, QFont
            from PyQt5.QtCore import Qt, QTimer, QUrl
            print("Starting Jasmine AI Assistant GUI with PyQt5...")
            
            # Create the application
            app = QApplication(sys.argv)
            
            # Create a main window
            window = QWidget()
            window.setWindowTitle("JASMINE AI ASSISTANT")
            window.setGeometry(50, 50, 900, 700)  # Adjusted size to fit better on screen
            window.setStyleSheet("""
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #000428,
                    stop: 0.5 #004e92,
                    stop: 1 #000428
                );
                color: #00ffcc;
            """)
            
            # Create main layout
            main_layout = QVBoxLayout()
            main_layout.setSpacing(20)
            main_layout.setContentsMargins(30, 30, 30, 30)
            
            # Header section with futuristic design
            header_frame = QFrame()
            header_frame.setStyleSheet("""
                background-color: rgba(0, 15, 35, 200);
                border: 2px solid qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #00ffcc,
                    stop: 0.5 #ff00ff,
                    stop: 1 #00ffcc
                );
                border-radius: 20px;
                padding: 20px;
            """)
            
            header_layout = QVBoxLayout()
            header_layout.setSpacing(15)
            
            # Futuristic title
            title = QLabel("JASMINE AI ASSISTANT")
            title.setStyleSheet("""
                font-size: 32px; 
                font-weight: 900; 
                color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00ffcc,
                    stop: 0.5 #ff00ff,
                    stop: 1 #00ffcc
                );
                text-align: center;
                background-color: transparent;
                letter-spacing: 2px;
                font-family: 'Arial Black', sans-serif;
            """)
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(title)
            
            # Subtitle
            subtitle = QLabel("ADVANCED NEURAL PROCESSING SYSTEM")
            subtitle.setStyleSheet("""
                font-size: 16px; 
                color: #74ee15;
                text-align: center;
                background-color: transparent;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                letter-spacing: 1px;
            """)
            subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(subtitle)
            
            header_frame.setLayout(header_layout)
            main_layout.addWidget(header_frame)
            
            # Create media frame
            media_frame = QFrame()
            media_frame.setStyleSheet("""
                background-color: rgba(0, 5, 20, 200);
                border: 2px solid qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #00ffff,
                    stop: 0.5 #ff00ff,
                    stop: 1 #00ffff
                );
                border-radius: 25px;
                padding: 25px;
            """)
            media_layout = QVBoxLayout()
            media_layout.setContentsMargins(15, 15, 15, 15)
            
            # Fallback to GIF for PyQt5
            gif_label = QLabel()
            gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            gif_label.setStyleSheet("""
                background-color: rgba(0, 0, 0, 100);
                border: 2px solid #00ffff;
                border-radius: 20px;
                min-height: 250px;
                min-width: 250px;
            """)
            
            gif_path = GraphicsDirectoryPath("Jarvis.gif")
            print(f"Loading GIF from: {gif_path}")
            print(f"GIF file exists: {os.path.exists(gif_path)}")
            
            if os.path.exists(gif_path):
                gif_movie = QMovie(gif_path)
                if gif_movie.isValid():
                    print("GIF movie loaded successfully")
                    gif_label.setMovie(gif_movie)
                    gif_movie.start()
                else:
                    print(f"GIF movie is not valid. Error: {gif_movie.lastError()}")
                    # Fallback text if GIF fails to load
                    gif_label.setText("JASMINE AI\n[ANIMATION LOADING...]")
                    gif_label.setStyleSheet("""
                        font-size: 24px;
                        color: #00ffcc;
                        background-color: rgba(0, 0, 0, 180);
                        border: 2px dashed #00ffcc;
                        border-radius: 20px;
                        padding: 60px;
                        font-weight: 900;
                        font-family: 'Courier New', monospace;
                    """)
            else:
                print("GIF file not found!")
                # Fallback text if GIF file is missing
                gif_label.setText("JASMINE AI\n[GIF FILE MISSING]")
                gif_label.setStyleSheet("""
                    font-size: 24px;
                    color: #ff3300;
                    background-color: rgba(0, 0, 0, 180);
                    border: 2px dashed #ff3300;
                    border-radius: 20px;
                    padding: 60px;
                    font-weight: 900;
                    font-family: 'Courier New', monospace;
                """)
                
            media_layout.addWidget(gif_label)
            media_frame.setLayout(media_layout)
            main_layout.addWidget(media_frame)
            
            # Create buttons
            button_layout = QHBoxLayout()
            button_layout.setSpacing(15)
            
            mic_button = QPushButton("🎤 TOGGLE MIC")
            mic_button.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #001f3f,
                        stop: 1 #0074D9
                    );
                    color: #00ffcc;
                    border: 2px solid #00ffff;
                    border-radius: 15px;
                    padding: 12px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    font-family: 'Courier New', monospace;
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #00ffff,
                        stop: 1 #0074D9
                    );
                    border: 2px solid #ff00ff;
                    color: #ffffff;
                }
            """)
            
            settings_button = QPushButton("⚙️ SETTINGS")
            settings_button.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #001f3f,
                        stop: 1 #0074D9
                    );
                    color: #00ffcc;
                    border: 2px solid #00ffff;
                    border-radius: 15px;
                    padding: 12px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    font-family: 'Courier New', monospace;
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #00ffff,
                        stop: 1 #0074D9
                    );
                    border: 2px solid #ff00ff;
                    color: #ffffff;
                }
            """)
            
            gemini_asr_button = QPushButton("🎙️ GEMINI ASR")
            gemini_asr_button.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #001f3f,
                        stop: 1 #0074D9
                    );
                    color: #00ffcc;
                    border: 2px solid #00ffff;
                    border-radius: 15px;
                    padding: 12px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    font-family: 'Courier New', monospace;
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #00ffff,
                        stop: 1 #0074D9
                    );
                    border: 2px solid #ff00ff;
                    color: #ffffff;
                }
            """)
            
            exit_button = QPushButton("❌ EXIT")
            exit_button.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #8B0000,
                        stop: 1 #FF0000
                    );
                    color: #ffffff;
                    border: 2px solid #ff0000;
                    border-radius: 15px;
                    padding: 12px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    font-family: 'Courier New', monospace;
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #ff0000,
                        stop: 1 #8B0000
                    );
                    border: 2px solid #ffffff;
                    color: #ffffff;
                }
            """)
            
            button_layout.addWidget(mic_button)
            button_layout.addWidget(gemini_asr_button)
            button_layout.addWidget(settings_button)
            button_layout.addWidget(exit_button)
            
            main_layout.addLayout(button_layout)
            
            # Create instructions frame
            instructions_frame = QFrame()
            instructions_frame.setStyleSheet("""
                background-color: rgba(0, 15, 35, 200);
                border: 2px solid qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #ff00ff,
                    stop: 0.5 #00ffff,
                    stop: 1 #ff00ff
                );
                border-radius: 20px;
                padding: 20px;
            """)
            instructions_layout = QVBoxLayout()
            instructions_layout.setSpacing(15)
            
            # Instructions title
            instructions_title = QLabel("SYSTEM COMMANDS")
            instructions_title.setStyleSheet("""
                font-size: 20px;
                color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff00ff,
                    stop: 0.5 #00ffff,
                    stop: 1 #ff00ff
                );
                font-weight: 900;
                text-align: center;
                background-color: transparent;
                font-family: 'Courier New', monospace;
                letter-spacing: 1px;
            """)
            instructions_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            instructions_layout.addWidget(instructions_title)
            
            # Instructions
            instructions = QLabel(
                "🎙️  SPEAK: 'Open Chrome' or 'Play music'\n" +
                "🔊  AUDIO: Real-time neural voice processing\n" +
                "⚡  SPEED: Quantum response in milliseconds\n" +
                "🔒  SECURITY: AES-256 encrypted\n" +
                "🌐  CONNECT: Internet connectivity\n\n" +
                "Close window to terminate assistant"
            )
            instructions.setStyleSheet("""
                font-size: 14px; 
                line-height: 1.6;
                color: #00ccff;
                background-color: transparent;
                font-family: 'Courier New', monospace;
                letter-spacing: 0.5px;
            """)
            instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
            instructions.setWordWrap(True)
            instructions_layout.addWidget(instructions)
            
            instructions_frame.setLayout(instructions_layout)
            main_layout.addWidget(instructions_frame)
            
            # Create system info frame
            system_frame = QFrame()
            system_frame.setStyleSheet("""
                background-color: rgba(0, 5, 20, 200);
                border: 2px solid qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #74ee15,
                    stop: 0.5 #00ffcc,
                    stop: 1 #74ee15
                );
                border-radius: 15px;
                padding: 15px;
            """)
            system_layout = QVBoxLayout()
            system_layout.setSpacing(10)
            
            # System info
            system_info = QLabel(
                f"👤 USER: {Assistantname or 'USER'} | " +
                f"💻 PLATFORM: {sys.platform.upper()} | " +
                "🔧 FRAMEWORK: PyQt5 | " +
                "📡 STATUS: ACTIVE"
            )
            system_info.setStyleSheet("""
                font-size: 12px;
                color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #74ee15,
                    stop: 0.5 #00ffcc,
                    stop: 1 #74ee15
                );
                background-color: transparent;
                text-align: center;
                font-family: 'Courier New', monospace;
                letter-spacing: 0.5px;
            """)
            system_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            system_layout.addWidget(system_info)
            
            system_frame.setLayout(system_layout)
            main_layout.addWidget(system_frame)
            
            window.setLayout(main_layout)
            window.show()
            
            # Function to handle Gemini ASR button click
            def start_gemini_asr():
                print("Starting Gemini ASR...")
                try:
                    # Import and call the actual Gemini ASR function
                    from Backend.SpeechToText import GeminiSpeechRecognition
                    result = GeminiSpeechRecognition()
                    
                    # Show the result in a message box
                    from PyQt5.QtWidgets import QMessageBox
                    msg = QMessageBox()
                    msg.setWindowTitle("Gemini ASR Result")
                    if result:
                        msg.setText(f"Transcribed text:\n{result}")
                    else:
                        msg.setText("Failed to transcribe audio or no speech detected.")
                    msg.setStyleSheet("""
                        background-color: #001f3f;
                        color: #00ffcc;
                        font-family: 'Courier New', monospace;
                    """)
                    msg.exec_()
                except Exception as e:
                    print(f"Error in Gemini ASR: {e}")
                    from PyQt5.QtWidgets import QMessageBox
                    msg = QMessageBox()
                    msg.setWindowTitle("Gemini ASR Error")
                    msg.setText(f"Error occurred during speech recognition:\n{str(e)}")
                    msg.setStyleSheet("""
                        background-color: #001f3f;
                        color: #00ffcc;
                        font-family: 'Courier New', monospace;
                    """)
                    msg.exec_()
            
            # Connect button signals
            exit_button.clicked.connect(app.quit)
            gemini_asr_button.clicked.connect(start_gemini_asr)
            
            print("GUI started successfully.")
            print("The application is now running. Close the GUI window to exit.")
            
            # Run the application
            return app.exec()
            
        except ImportError as e2:
            print(f"GUI Error: Neither PyQt6 nor PyQt5 is available. {e2}")
            return False
        except Exception as e2:
            print(f"GUI Error with PyQt5: {e2}")
            return False
            
    except Exception as e:
        print(f"GUI Error with PyQt6: {e}")
        return False

# Main execution
if __name__ == "__main__":
    result = GraphicalUserInterface()
    if result is False:
        sys.exit(1)
    else:
        sys.exit(result)