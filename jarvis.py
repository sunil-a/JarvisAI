import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
from datetime import datetime

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)

# Initialize speech recognizer
recognizer = sr.Recognizer()


def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source, timeout=5, phrase_time_limit=8
            )
            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            speak("Speech recognition requires an internet connection.")
            return ""


def execute_command(command):

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web.")

    elif "open notepad" in command:
        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad.")

    elif "open calculator" in command:
        subprocess.Popen(["calc.exe"])
        speak("Opening Calculator.")

    elif "what time" in command or "current time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif "search for" in command:
        query = command.replace("search for", "", 1).strip()

        if query:
            webbrowser.open(
                "https://www.google.com/search?q=" +
                __import__("urllib.parse", fromlist=["quote"]).quote(query)
            )
            speak(f"Searching for {query}.")

    elif "stop jarvis" in command or "exit jarvis" in command:
        speak("Goodbye! JARVIS shutting down.")
        return False

    else:
        speak("Sorry, I do not know that command yet.")

    return True


def main():
    speak("Hello! I am JARVIS, your personal voice assistant.")
    speak("How can I help you?")

    running = True

    while running:
        command = listen()

        if command:
            running = execute_command(command)


if __name__ == "__main__":
    main()
