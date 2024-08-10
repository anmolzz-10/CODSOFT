import tkinter as tk
from tkinter import scrolledtext
import requests
import random
import math
from datetime import datetime
from bs4 import BeautifulSoup

# Global list to manage tasks
tasks = []

# Function to get weather information
def get_weather(city):
    api_key = "API KEY"  # Your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] == "404":
        return "City not found. Please check the city name."
    else:
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temp = main['temp'] - 273.15  # Convert from Kelvin to Celsius
        return f"The weather in {city} is {weather_desc} with a temperature of {temp:.2f}°C."

# Function to perform basic and advanced arithmetic calculations
def calculate(expression):
    try:
        # Convert the expression to a valid Python expression
        expression = expression.replace('^', '**')  # Handle exponentiation
        result = eval(expression, {"__builtins__": None}, {"sin": math.sin, "cos": math.cos, "tan": math.tan, 
                                                           "sqrt": math.sqrt, "log": math.log, "exp": math.exp, 
                                                           "pi": math.pi, "e": math.e, "pow": math.pow})
        return str(result)
    except Exception as e:
        return f"There was an error with your calculation: {e}"

# Function to manage a to-do list
def manage_tasks(command):
    if "add" in command:
        task = command.replace("add", "").strip()
        tasks.append(task)
        return f"Task '{task}' added to your to-do list."
    elif "show" in command:
        if tasks:
            return "Your tasks are: " + ", ".join(tasks)
        else:
            return "Your to-do list is empty."
    elif "remove" in command:
        task = command.replace("remove", "").strip()
        if task in tasks:
            tasks.remove(task)
            return f"Task '{task}' removed from your to-do list."
        else:
            return f"Task '{task}' not found in your to-do list."
    else:
        return "I can only add, show, or remove tasks."

# Function to fetch the latest news headlines for today with category filtering
def get_news(category=None):
    api_key = "API KEY"  # Your NewsAPI key
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'us',
        'apiKey': api_key,
        'sortBy': 'publishedAt'  # Sort by publication date
    }
    if category:
        params['category'] = category
    
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'ok':
        headlines = [article['title'] for article in data['articles'][:5]]  # Get top 5 headlines
        if headlines:
            return "Here are today's top news headlines:\n" + "\n".join(headlines)
        else:
            return "No news articles found for today."
    else:
        return "Failed to fetch news."

# Function to gather information from the web
def gather_info(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('h3')  # Assuming we're interested in heading tags for search results
    return "\n".join([result.get_text() for result in results[:5]])  # Get top 5 results

# Function to tell a joke or a fun fact
def get_joke_or_fact():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you get if you cross a cat with a dark horse? Kitty Perry.",
        "Why don't programmers like nature? It has too many bugs."
    ]
    facts = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
        "A single strand of spaghetti is called a 'spaghetto'.",
        "There are more stars in the universe than grains of sand on all the Earth’s beaches."
    ]
    return random.choice(jokes + facts)

# Main chatbot function to handle responses
def chatbot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Debugging: Print the user input to see what's being processed
    print(f"User input: {user_input}")

    # Weather
    if "weather" in user_input and "in" in user_input:
        city = user_input.split("in")[-1].strip()
        return get_weather(city)
    
    # Calculation
    elif "calculate" in user_input:
        expression = user_input.replace("calculate", "").strip()
        return calculate(expression)
    
    # Task management
    elif "task" in user_input:
        return manage_tasks(user_input)
    
    # News with category
    elif "news" in user_input:
        if "sports" in user_input:
            return get_news("sports")
        elif "technology" in user_input:
            return get_news("technology")
        elif "business" in user_input:
            return get_news("business")
        else:
            return get_news()
    
    # Gather information
    elif "search" in user_input or "info" in user_input:
        query = user_input.replace("search", "").replace("info", "").strip()
        return gather_info(query)
    
    # Joke or Fact
    elif "joke" in user_input or "fact" in user_input:
        return get_joke_or_fact()
    
    # Greetings and small talk
    elif "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "how are you" in user_input:
        return "I'm here to help with whatever you need!"
    elif "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! Have a great day!"
    
    # Default response
    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"

# Function to send user input to the chatbot and display the response
def send():
    user_input = entry.get()
    if user_input.lower() in ["bye", "goodbye"]:
        chat_area.insert(tk.END, "You: " + user_input + "\n")
        chat_area.insert(tk.END, "Chatbot: Goodbye! Have a great day!\n")
        root.quit()
    else:
        chat_area.insert(tk.END, "You: " + user_input + "\n")
        response = chatbot_response(user_input)
        chat_area.insert(tk.END, "Chatbot: " + response + "\n")
    entry.delete(0, tk.END)

# Creating the GUI interface
root = tk.Tk()
root.title("Utility Chatbot")

# Chat display area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
chat_area.pack(pady=10)

# User input area
entry = tk.Entry(root, width=40, font=("Arial", 14))
entry.pack(pady=10)
entry.bind("<Return>", lambda event: send())  # Bind Enter key to send function

# Send button
send_button = tk.Button(root, text="Send", command=send, font=("Arial", 12))
send_button.pack(pady=10)

# Initial greeting
chat_area.insert(tk.END, "Chatbot: Hello! I'm your utility chatbot. How can I assist you today?\n")

# Run the GUI loop
root.mainloop()
