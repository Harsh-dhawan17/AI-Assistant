import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pyjokes
import os
import random
import tkinter as tk
from tkinter import scrolledtext
import wikipedia
import pywhatkit
import openai

# Set your OpenAI API key here
openai.api_key = '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'

  # Replace with your actual OpenAI API key
memory = {}

def remember_memory(key, value):
    """Remember something and store it in memory."""
    memory[key] = value
    speechtx(f"Okay, I will remember that {key} is {value}.")

def recall_memory(key):
    """Recall something from memory."""
    if key in memory:
        return f"You told me that {key} is {memory[key]}."
    else:
        return f"Sorry, I don't remember anything about {key}."

def forget_memory(key):
    """Forget a specific memory."""
    if key in memory:
        del memory[key]
        speechtx(f"I have forgotten about {key}.")
    else:
        speechtx(f"I don't remember anything about {key} to forget.")

def sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            data = recognizer.recognize_google(audio)
            print(f"You said: {data}")
            output_text.insert(tk.END, f"You: {data}\n")
            return data.lower().strip()
        except sr.UnknownValueError:
            error_msg = "Sorry, I didn't catch that."
            print(error_msg)
            output_text.insert(tk.END, f"Jarvis: {error_msg}\n")
            return ""
        except sr.RequestError:
            error_msg = "Sorry, my speech service is down."
            print(error_msg)
            output_text.insert(tk.END, f"Jarvis: {error_msg}\n")
            return ""

def get_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # or choose another GPT model
            prompt=prompt,
            max_tokens=500,  # Adjust based on how detailed you want the response
            n=1,
            stop=None,
            temperature=0.7  # Adjust for creativity
        )
       
        return response.choices[0].text.strip()
    except openai.error.AuthenticationError:
        print("Invalid API key or expired API key.")
        return "Sorry, there seems to be an issue with the API key."
    except openai.error.APIConnectionError:
        print("Failed to connect to OpenAI API.")
        return "Sorry, I'm having trouble connecting to the OpenAI service right now."
    except openai.error.RateLimitError:
        print("Rate limit exceeded.")
        return "I'm receiving too many requests at the moment. Please try again later."
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I'm having trouble connecting to the OpenAI service right now."

def speechtx(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Selecting female voice
    engine.setProperty('rate', 150)
    print(f"Jarvis: {text}")
    output_text.insert(tk.END, f"Jarvis: {text}\n")
    engine.say(text)
    engine.runAndWait()

def play_local_song(song_name):
    music_dir = r'C:\Users\DELL\Music'
    if os.path.exists(music_dir):
        songs = [f for f in os.listdir(music_dir) if os.path.isfile(os.path.join(music_dir, f))]
        
        if song_name == "random":
            selected_song = random.choice(songs)
            os.startfile(os.path.join(music_dir, selected_song))
            speechtx(f"Playing {selected_song} from your local library.")
        else:
            # Match song name with available songs
            best_match = None
            for song in songs:
                if song_name in song.lower():
                    best_match = song
                    break

            if best_match:
                os.startfile(os.path.join(music_dir, best_match))
                speechtx(f"Playing {best_match} from your local library.")
            else:
                speechtx("Sorry, I couldn't find that song in your local library.")
    else:
        speechtx("Music directory not found.")

def play_youtube_song(song_name):
    try:
        if song_name == "random":
            popular_songs = [
                "Blinding Lights by The Weeknd",
                "Shape of You by Ed Sheeran",
                "Dance Monkey by Tones and I",
                "Someone You Loved by Lewis Capaldi",
                "Senorita by Shawn Mendes and Camila Cabello",
                "Bad Guy by Billie Eilish",
                "Old Town Road by Lil Nas X",
                "Perfect by Ed Sheeran",
                "Havana by Camila Cabello",
                "Rockstar by Post Malone"
            ]
            selected_song = random.choice(popular_songs)
            speechtx(f"Playing {selected_song} from YouTube.")
            pywhatkit.playonyt(selected_song)
        else:
            speechtx(f"Searching for {song_name} on YouTube.")
            pywhatkit.playonyt(song_name)
            speechtx(f"Playing {song_name} from YouTube.")
    except Exception as e:
        print(f"Error: {e}")
        speechtx("Sorry, I couldn't play the song due to an error.")

def shut_down_system():
    speechtx("Shutting down the system. Goodbye!")
    os.system("shutdown /s /t 1")

def restart_system():
    speechtx("Restarting the system. See you soon!")
    os.system("shutdown /r /t 1")

def open_downloads_folder():
    downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    if os.path.exists(downloads_dir):
        os.startfile(downloads_dir)
        speechtx("Opening your Downloads folder.")
    else:
        speechtx("Downloads directory not found.")

def say_hi_to_friend():
    speechtx("What is your friend's name?")
    friend_name = sptext()
    if friend_name:
        speechtx(f"Hello {friend_name}, how are you?")
        friend_response = sptext()
        if "i am fine" in friend_response or "i'm fine" in friend_response:
            speechtx("I am glad to hear that.")
        else:
            speechtx("I hope you are doing well.")
    else:
        speechtx("I didn't catch your friend's name.")

def search_wikipedia(query):
    try:
        results = wikipedia.search(query)
        if results:
            first_result = results[0]
            summary = wikipedia.summary(first_result, sentences=2)
            return summary
        else:
            return "Sorry, I couldn't find any information on that topic."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"There are multiple results for {query}. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information on that topic."

def handle_openai_or_wikipedia(data):
    """Determine if the input is suitable for OpenAI or Wikipedia, then process it."""
    if any(keyword in data for keyword in ["who", "what", "where", "when", "why", "how"]):
        # Use Wikipedia for factual queries
        result = search_wikipedia(data)
        if "Sorry" in result:
            result = get_openai_response(data)  # Use OpenAI if Wikipedia fails
    else:
        # Use OpenAI for everything else
        result = get_openai_response(data)
    
    speechtx(result)
    

def main():
    speechtx("Hello, I am Jarvis A.I")
    while True:
        data = sptext()
        if data == "":
            continue
        elif "exit" in data or "quit" in data or "stop" in data:
            speechtx("Goodbye! Have a nice day.")
            break
        elif "hello jarvis" in data:
            speechtx("Hello! How can I assist you today?")
        elif "how are you jarvis" in data:
            speechtx("i am fine sir. how are you")
        elif "I am fine jarvis" in data:
            speechtx("Glad to hear that!.How can i assist you further")
        elif "What is your name" in data:
            speechtx("My name is Jarvis.")
        elif "who created you" in data or "who made you" in data:
            speechtx("I was created by a developer.")
        elif "how old are you" in data:
            speechtx("I was created in February 2020, so I'm four years old.")
        elif "open downloads" in data or "download" in data:
            open_downloads_folder()
        elif "remember" in data:
            speechtx("What would you like me to remember?")
            memory_key = sptext()
            speechtx(f"What should I remember about {memory_key}?")
            memory_value = sptext()
            remember_memory(memory_key, memory_value)
        elif "tell me a memory that i tell you  before" in data:
            memory_key = data.replace("tell me a memory that i tell you  before", "").strip()
            recall_response = recall_memory(memory_key)
            speechtx(recall_response)
        elif "forget" in data:
            memory_key = data.replace("forget", "").strip()
            forget_memory(memory_key)
        elif "time" in data:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speechtx(f"The current time is {current_time}.")
        elif "open youtube" in data or "youtube" in data:
            speechtx("Opening YouTube.")
            webbrowser.open("https://www.youtube.com/")
        elif "open chatgpt" in data or "chatgpt" in data:
            speechtx("Opening ChatGPT.")
            webbrowser.open("https://chat.openai.com/")
        elif "play song from youtube" in data or "play from youtube" in data:
            speechtx("Which song would you like to play from YouTube?")
            song_name = sptext()
            if song_name == "" or "any" in song_name or "random" in song_name:
                song_name = "random"
            play_youtube_song(song_name)
        elif "play music" in data or "play song" in data or "play a song" in data:
            speechtx("Which song would you like to play from your local library?")
            song_name = sptext()
            if song_name == "" or "any" in song_name or "random" in song_name:
                song_name = "random"
            play_local_song(song_name)
        elif "tell me a joke" in data or "joke" in data:
            joke = pyjokes.get_joke(language="en", category="neutral")
            speechtx(joke)
        elif "shut down" in data:
            shut_down_system()
        elif "restart" in data:
            restart_system()
        elif "say hi to my friend" in data or "say hello to my friend" in data:
            say_hi_to_friend()
        elif "i am bored" in data or "talk to me" in data:
            speechtx("Sure, let's chat! What would you like to talk about?")
            conversation_topic = sptext()
            if conversation_topic:
                handle_openai_or_wikipedia(conversation_topic)
            else:
                speechtx("I'm here to chat whenever you're ready.")
        else:
            speechtx("Let me check that for you.")
            handle_openai_or_wikipedia(data)

# GUI Setup
root = tk.Tk()
root.title("Jarvis Assistant")

# Creating text area for displaying output
output_text = scrolledtext.ScrolledText(root, width=60, height=20)
output_text.pack(pady=10)

# Creating buttons for each function
btn_start = tk.Button(root, text="Start Jarvis", command=main, width=20, bg='blue', fg='white')
btn_start.pack(pady=5)

btn_hi_friend = tk.Button(root, text="Say Hi to Friend", command=say_hi_to_friend, width=20, bg='green', fg='white')
btn_hi_friend.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=root.quit, width=20, bg='red', fg='white')
btn_exit.pack(pady=5)

root.mainloop()
