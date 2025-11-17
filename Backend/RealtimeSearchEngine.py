from googlesearch import search
from groq import Groq
from json import load, dump, JSONDecodeError
import datetime
from dotenv import dotenv_values
import os

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
        Answer = f"The search results for '{query}' are :\n[start]\n"

        for i in results:
            # Convert to string to avoid attribute access issues
            result_str = str(i)
            Answer += f"Result: {result_str}\n\n"

        Answer += "[end]"
        return Answer
    except Exception as e:
        # Fallback to simple search
        try:
            results = list(search(query, num_results=5))
            Answer = f"The search results for '{query}' are :\n[start]\n"
            
            for i in results:
                Answer += f"Result: {str(i)}\n\n"
                
            Answer += "[end]"
            return Answer
        except Exception as e2:
            # Return a fallback message if search fails
            return f"Unable to perform search for '{query}'. Error: {str(e2)}\n[start]\nNo search results available.\n[end]"

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
    
    # Check if client is available
    if client is None:
        return "Groq API key not available. Please check your .env file."

    with open(os.path.join("Data", "ChatLog.json"), "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

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
    messages.append({"role": "assistant", "content": Answer})

    with open(os.path.join("Data", "ChatLog.json"), "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Query: ")
        print(RealtimeSearchEngine(prompt))