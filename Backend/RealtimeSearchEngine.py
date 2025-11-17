from googlesearch import search
from json import load, dump, JSONDecodeError
import datetime
from dotenv import dotenv_values
import os
import sys
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backend.GeminiAPI import gemini_api, chat_completion

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Ensure Data directory exists
data_dir = "Data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

try:
    with open(os.path.join("Data", "ChatLog.json"), "r") as f:
        messages = load(f)
except FileNotFoundError:
    # Create the file with an empty list if it doesn't exist
    with open(os.path.join("Data", "ChatLog.json"), "w") as f:
        dump([], f)
    messages = []
except JSONDecodeError:
    print("ChatLog.json is empty or corrupted. Initializing with an empty list.")
    with open(os.path.join("Data", "ChatLog.json"), "w") as f:
        dump([], f)
    messages = []

def GoogleSearch(query):
    try:
        # Try advanced search first
        results = list(search(query, advanced=True, num_results=5))
        
        # If advanced search returns no results, try simple search
        if not results:
            results = list(search(query, num_results=5))
            
        if results:
            Answer = f"The search results for '{query}' are :\n[start]\n"

            for i in results:
                # Convert to string to avoid attribute access issues
                result_str = str(i)
                Answer += f"Result: {result_str}\n\n"

            Answer += "[end]"
            return Answer
        else:
            # Return a fallback message if no results found
            return f"No search results found for '{query}'.\n[start]\nNo search results available.\n[end]"
    except Exception as e:
        # Return a fallback message if search fails
        return f"Unable to perform search for '{query}'. Error: {str(e)}\n[start]\nNo search results available.\n[end]"

def get_weather_info(location):
    """Get weather information for a specific location using Open-Meteo API"""
    try:
        # First, we need to get the coordinates for the location
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_response = requests.get(geocoding_url, timeout=10)
        geo_data = geo_response.json()
        
        if 'results' not in geo_data or not geo_data['results']:
            return f"Sorry, I couldn't find weather information for {location}."
        
        # Get coordinates
        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']
        resolved_location = geo_data['results'][0]['name']
        
        # Get current weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
        weather_response = requests.get(weather_url, timeout=10)
        weather_data = weather_response.json()
        
        if 'current_weather' not in weather_data:
            return f"Sorry, I couldn't retrieve weather data for {resolved_location}."
        
        # Extract weather information
        current = weather_data['current_weather']
        temperature = current['temperature']
        windspeed = current['windspeed']
        weather_code = current['weathercode']
        
        # Simple weather code interpretation
        weather_descriptions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle",
            55: "dense drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            71: "slight snow fall",
            73: "moderate snow fall",
            75: "heavy snow fall",
            95: "thunderstorm",
        }
        
        weather_description = weather_descriptions.get(weather_code, "unknown weather condition")
        
        return f"The current weather in {resolved_location} is {temperature}°C with {weather_description} and wind speed of {windspeed} km/h."
        
    except Exception as e:
        return f"Sorry, I couldn't retrieve weather information for {location}. Error: {str(e)}"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# SystemChatBot is no longer needed since we're using Gemini API exclusively
# SystemChatBot = [
#     {"role": "system", "content": System},
#     {"role": "user", "content": "Hi"},
#     {"role": "assistant", "content": "Hello, Sir, how can I help you?"}
# ]

def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours: {minute} minutes: {second} seconds.\n"
    return data

def RealtimeSearchEngine(prompt):
    global messages
    
    with open(os.path.join("Data", "ChatLog.json"), "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    # Check if this is a weather query
    weather_keywords = ["weather", "temperature", "forecast", "climate", "rain", "snow", "sunny", "cloudy", "windy"]
    is_weather_query = any(keyword in prompt.lower() for keyword in weather_keywords)
    
    if is_weather_query:
        # Extract location from the prompt
        # Simple approach: assume the location is after "in" or "at"
        location = ""
        if " in " in prompt.lower():
            location = prompt.lower().split(" in ", 1)[1].strip("?")
        elif " at " in prompt.lower():
            location = prompt.lower().split(" at ", 1)[1].strip("?")
        else:
            # If no specific location mentioned, try to extract a proper noun
            words = prompt.split()
            # Simple heuristic: assume capitalized words after weather keywords are locations
            for i, word in enumerate(words):
                if word.lower() in weather_keywords and i + 1 < len(words):
                    location = words[i + 1]
                    break
        
        if location:
            # Get weather information directly
            weather_info = get_weather_info(location)
            Answer = weather_info
        else:
            # Fall back to search if we can't determine location
            search_results = GoogleSearch(prompt)
            Answer = f"I found the following search results for '{prompt}': {search_results}"
    else:
        # Regular search for non-weather queries
        search_results = GoogleSearch(prompt)
        
        # Use Gemini API for processing search results
        if gemini_api.model:
            # Prepare conversation history for context-aware responses
            conversation_history = [
                {"role": "user", "content": System},
                {"role": "assistant", "content": "Understood. I'm ready to help with search results."}
            ]
            
            # Add recent chat history for context (last 3 exchanges for faster processing)
            recent_chats = messages[-3:] if len(messages) > 3 else messages
            for entry in recent_chats:
                conversation_history.append({
                    "role": entry["role"], 
                    "content": entry["content"]
                })
            
            # Check if search results are available
            if "No search results available" not in search_results:
                # Add search results and current query
                conversation_history.append({
                    "role": "user", 
                    "content": f"Here are the search results for '{prompt}': {search_results}"
                })
                conversation_history.append({
                    "role": "user", 
                    "content": f"Use the search results to provide an accurate answer to: {prompt}. Include real-time information if needed: {Information()}"
                })
            else:
                # No search results, ask Gemini to provide general knowledge
                conversation_history.append({
                    "role": "user", 
                    "content": f"No search results were found for '{prompt}'. Please provide an answer based on your general knowledge. Include real-time information if needed: {Information()}"
                })
            
            # Get response from Gemini with optimized parameters for speed
            Answer = chat_completion(conversation_history, temperature=0.5, max_tokens=512)
            
            # Fallback if Gemini fails
            if not Answer:
                Answer = f"I found the following search results for '{prompt}': {search_results}"
        else:
            # If Gemini is not available, return search results directly
            Answer = f"I found the following search results for '{prompt}': {search_results}"

    messages.append({"role": "assistant", "content": Answer})

    with open(os.path.join("Data", "ChatLog.json"), "w") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Query: ")
        print(RealtimeSearchEngine(prompt))