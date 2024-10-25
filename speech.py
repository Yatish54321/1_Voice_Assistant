import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit as kit
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
from google.auth.transport import requests
from requests import get
import random

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    """Speak the given audio string."""
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    """Wish the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Assistant Sir. Please tell me how may I help you")


def takeCommand():
    """Listen for a command from the user and return it as a string."""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"User said: {command}")
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return "none"
    except Exception as e:
        print(f"Error: {e}")
        speak("There was an issue with voice recognition.")
        return "none"


def sendEmail(to, content):   # improving
    """Send an email to the specified address with the given content."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry Sir, I am not able to send this email.")


def performWebOperations(query):
    """Handle web-related operations based on the user's command."""
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")

    elif 'open google' in query:
        speak("Sir, what should I search on Google?")
        cm = takeCommand()
        if cm != "none":
            webbrowser.open(f"https://www.google.com/search?q={cm}")

    elif 'open stack overflow' in query:
        print("Opening Stack Overflow...")
        webbrowser.open("https://stackoverflow.com/")


    elif 'open facebook' in query:
        webbrowser.open("www.facebook.com")

    elif 'open colab' in query:
        webbrowser.open("https://colab.research.google.com/")

    elif 'open github' in query:
        webbrowser.open("https://github.com/")

    elif "play songs on youtube" in query:
        kit.playonyt("Ordinary Person")


def playMusic():
    """Play a random song from the specified directory."""
    music_dir = 'C:\\Users\\yatis\\Downloads\\Flipkart_Grid6.0_Robotics_Solution_Video_Simulation.mp4'
    songs = os.listdir(music_dir)
    if songs:
        os.startfile(os.path.join(music_dir, random.choice(songs)))


def getIPAddress():
    """Fetch and speak the user's IP address."""
    try:
        # Make the GET request to the API
        ip = get('https://api.ipify.org').text
        speak(f"Your IP address is {ip}")
    except requests.ConnectionError:
        print("Connection error. Please check your internet connection.")
        speak("Unable to fetch IP address due to connection issues.")
    except requests.Timeout:
        print("The request timed out. Please try again.")
        speak("Unable to fetch IP address due to a timeout.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        speak("Unable to fetch IP address.")



def tellTime():
    """Speak the current time."""
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the time is {strTime}")


def tellJoke():
    """Fetch and speak a random joke."""
    joke = pyjokes.get_joke()
    speak(joke)


if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()

        if query == "none":
            continue  # Retry listening if no valid command

        print(f"Command received: {query}")

        if 'play music' in query:
            print("Playing music...")
            playMusic()
        elif 'time' in query:
            print("Telling the time...")
            tellTime()
        elif 'joke' in query:
            print("Telling a joke...")
            tellJoke()
        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                if content != "none":
                    to = "yatish54321@example.com"
                    sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry Sir, I am not able to send this email")
        elif 'shutdown' in query:
            print("Shutting down the system...")
            os.system("shutdown /s /t 5")
        elif 'restart' in query:
            print("Restarting the system...")
            os.system("shutdown /r /t 5")
        elif 'sleep' in query:
            print("Putting the system to sleep...")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif 'no thanks' in query or 'you can sleep' in query:
            print("Assistant is signing off...")
            speak("Thanks for using me Sir, have a good day.")
            break
        else:
            print("Performing web operations...")
            performWebOperations(query)
