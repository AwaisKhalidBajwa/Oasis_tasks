import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the user's voice and return the command as text"""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            speak("Sorry, I'm unable to reach the speech recognition service.")
            return None

def process_command():
    """Process the command from the user"""
    command = listen()
    if command is None:
        return
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%H:%M:%S')}.")
    elif "date" in command:
        today = datetime.date.today()
        speak(f"Today's date is {today.strftime('%B %d, %Y')}.")
    elif "calculate" in command:
        try:
            # Simple arithmetic evaluation
            result = eval(command.replace("calculate", "").strip())
            speak(f"The result is {result}.")
        except Exception as e:
            speak("Sorry, I couldn't perform the calculation. Please check your command.")
    elif "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query} on the web.")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "introduction" in command:
        speak("I am your voice assistant. I can help with the time, date, weather, perform calculations, and search the web.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        root.destroy()
    else:
        speak("I'm sorry, I don't understand that command.")

# Create the main window
root = tk.Tk()
root.title("Voice Assistant")

# Create a label
label = tk.Label(root, text="Click the button and speak your command", padx=20, pady=20)
label.pack()

# Create a button to activate the voice assistant
button = tk.Button(root, text="Speak", command=process_command, padx=20, pady=10)
button.pack()

# Run the application
root.mainloop()
