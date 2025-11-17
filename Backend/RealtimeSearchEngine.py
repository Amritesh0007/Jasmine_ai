from googlesearch import search
from groq import Groq
from json import load, dump, JSONDecodeError
import datetime
from dotenv import dotenv_values
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Backend.GeminiAPI import gemini_api, chat_completion

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Clean up the API key if it exists
if GroqAPIKey:
    GroqAPIKey = GroqAPIKey.strip().strip('"').strip("'")

# Initialize client only if API key is available
client = Groq(api_key=GroqAPIKey) if GroqAPIKey else None

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

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, Sir, how can I help you?"}
]

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
    global SystemChatBot, messages
    
    with open(os.path.join("Data", "ChatLog.json"), "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    search_results = GoogleSearch(prompt)
    
    # Try using Gemini API first
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
        # Fallback to Groq if Gemini is not available
        if client is None:
            return f"I found the following search results for '{prompt}': {search_results}"

        SystemChatBot.append({"role": "system", "content": search_results})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated to a currently available model
            messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.strip().replace("</s>", "")
        SystemChatBot.pop()

    messages.append({"role": "assistant", "content": Answer})

    with open(os.path.join("Data", "ChatLog.json"), "w") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Query: ")
        print(RealtimeSearchEngine(prompt))