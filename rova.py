#pip install pyttsx3 SpeechRecognition wikipedia pyaudio

import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia

# Initialize the speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 = Male, 1 = Female

def speak(audio):
    """Speak the given text."""
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Listen for a voice command and convert it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
        except Exception as e:
            print("Could not understand. Please say that again.")
            return "None"
    return query

def tellDay():
    """Tell the current day of the week."""
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {
        1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
        4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'
    }
    day_of_the_week = Day_dict.get(day, "Unknown day")
    speak(f"Today is {day_of_the_week}")
    print(f"Day: {day_of_the_week}")

def tellTime():
    """Tell the current time."""
    now = datetime.datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    speak(f"The time is {hour} hours and {minute} minutes")
    print(f"Time: {hour}:{minute}")

def Hello():
    """Initial greeting."""
    speak("Hello sirr. I am Rovaa. your desktop assistant, Tell me how may I help you?")

def Take_query():
    """Main loop to take user commands and respond."""
    Hello()

    while True:
        query = takeCommand().lower()

        if "play some music" in query or "music" in query:
            speak("Opening gana")
            webbrowser.open("https://gaana.com/")
        
        elif "open youtube" in query or "youtube" in query:
            speak("Opening youtube")
            webbrowser.open("https://www.youtube.com/")
            
        elif "open google" in query or "google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
            
        elif "open linkedin" in query or "linkedin" in query:
            speak("Opening linkedin")
            webbrowser.open("https://www.linkedin.com/in/rohith-chelimilla-9b45922a7/")
        
        elif "open github" in query or "github" in query:
            speak("Opening github")
            webbrowser.open("https://github.com/chelimillarohith")

        elif "which day is it" in query or "day" in query:
            tellDay()

        elif "tell me the time" in query or "time" in query:
            tellTime()

        elif "from wikipedia" in query or "who is" in query:
            speak("Searching Wikipedia...")
            query = query.replace("from wikipedia", "").strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't find that on Wikipedia.")
                print("Wikipedia Error:", e)

        elif "tell me your name" in query or "what is your name" in query or "who are you" in query:
            speak("I am Rova, your desktop assistant.")

        elif "bye" in query or "exit" in query or "stop" in query:
            speak("Bye!, have a good day.")
            print("Assistant stopped.")
            break

        else:
            speak("Sorry, I didn't understand that. Please try again.")

# Entry point
if __name__ == '__main__':
    Take_query()
