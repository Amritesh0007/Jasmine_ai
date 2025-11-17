import google.generativeai as genai
import os
from dotenv import dotenv_values
from typing import Optional, List, Dict, Any
import PIL.Image
import base64
import io

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
env_vars = dotenv_values(env_path)
GEMINI_API_KEY = env_vars.get("GEMINI_API_KEY")

# Configure the API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiAPI:
    """A class to interact with Google's Gemini API for various AI capabilities."""
    
    def __init__(self):
        """Initialize the Gemini API client."""
        self.model = None
        if GEMINI_API_KEY:
            # Use the correct model names
            self.model = genai.GenerativeModel('models/gemini-flash-latest')
            self.vision_model = genai.GenerativeModel('models/gemini-flash-latest')
    
    def generate_text(self, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """
        Generate text based on a prompt.
        
        Args:
            prompt (str): The input prompt for text generation
            temperature (float): Controls randomness in generation (0.0 to 1.0)
            
        Returns:
            Optional[str]: Generated text or None if failed
        """
        try:
            if not self.model:
                raise ValueError("Gemini API not configured. Check your API key.")
                
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return None
    
    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Optional[str]:
        """
        Generate a chat completion based on conversation history.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'
            temperature (float): Controls randomness in generation
            
        Returns:
            Optional[str]: Generated response or None if failed
        """
        try:
            if not self.model:
                raise ValueError("Gemini API not configured. Check your API key.")
            
            # Convert messages to Gemini format
            chat_history = []
            for msg in messages:
                if msg['role'] == 'user':
                    chat_history.append({'role': 'user', 'parts': [msg['content']]})
                elif msg['role'] == 'assistant':
                    chat_history.append({'role': 'model', 'parts': [msg['content']]})
            
            # Start chat and send message
            chat = self.model.start_chat(history=chat_history[:-1])
            response = chat.send_message(chat_history[-1]['parts'][0])
            return response.text
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return None
    
    def analyze_image(self, image_path: str, prompt: str = "Describe this image") -> Optional[str]:
        """
        Analyze an image using Gemini's vision capabilities.
        
        Args:
            image_path (str): Path to the image file
            prompt (str): Prompt for image analysis
            
        Returns:
            Optional[str]: Analysis result or None if failed
        """
        try:
            if not self.vision_model:
                raise ValueError("Gemini Vision model not available.")
            
            # Load and process image
            img = PIL.Image.open(image_path)
            
            # Generate content
            response = self.vision_model.generate_content([prompt, img])
            return response.text
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return None
    
    def solve_math_problem(self, problem: str) -> Optional[str]:
        """
        Solve mathematical problems using Gemini.
        
        Args:
            problem (str): Mathematical problem to solve
            
        Returns:
            Optional[str]: Solution or None if failed
        """
        try:
            prompt = f"Solve this mathematical problem step by step: {problem}"
            return self.generate_text(prompt)
        except Exception as e:
            print(f"Error solving math problem: {e}")
            return None
    
    def explain_code(self, code: str, language: str = "Python") -> Optional[str]:
        """
        Explain code functionality.
        
        Args:
            code (str): Code to explain
            language (str): Programming language of the code
            
        Returns:
            Optional[str]: Explanation or None if failed
        """
        try:
            prompt = f"Explain the following {language} code in detail:\n\n{code}"
            return self.generate_text(prompt)
        except Exception as e:
            print(f"Error explaining code: {e}")
            return None
    
    def debug_code(self, code: str, error: str = "", language: str = "Python") -> Optional[str]:
        """
        Help debug code issues.
        
        Args:
            code (str): Code to debug
            error (str): Error message if any
            language (str): Programming language of the code
            
        Returns:
            Optional[str]: Debugging suggestions or None if failed
        """
        try:
            if error:
                prompt = f"Debug the following {language} code. The error is: {error}\n\nCode:\n{code}"
            else:
                prompt = f"Debug the following {language} code and identify potential issues:\n\n{code}"
            return self.generate_text(prompt)
        except Exception as e:
            print(f"Error debugging code: {e}")
            return None

# Global instance for easy access
gemini_api = GeminiAPI()

# Convenience functions for direct access
def generate_text(prompt: str, temperature: float = 0.7) -> Optional[str]:
    """Generate text using Gemini."""
    return gemini_api.generate_text(prompt, temperature)

def chat_completion(messages: List[Dict[str, str]], temperature: float = 0.7) -> Optional[str]:
    """Get chat completion from Gemini."""
    return gemini_api.chat_completion(messages, temperature)

def analyze_image(image_path: str, prompt: str = "Describe this image") -> Optional[str]:
    """Analyze an image using Gemini Vision."""
    return gemini_api.analyze_image(image_path, prompt)

def solve_math_problem(problem: str) -> Optional[str]:
    """Solve a math problem using Gemini."""
    return gemini_api.solve_math_problem(problem)

def explain_code(code: str, language: str = "Python") -> Optional[str]:
    """Explain code using Gemini."""
    return gemini_api.explain_code(code, language)

def debug_code(code: str, error: str = "", language: str = "Python") -> Optional[str]:
    """Debug code using Gemini."""
    return gemini_api.debug_code(code, error, language)