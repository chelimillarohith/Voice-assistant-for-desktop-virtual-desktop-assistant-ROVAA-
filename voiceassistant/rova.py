import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
from pathlib import Path
import os

# ====== SPEECH ENGINE FUNCTION ======
def speak(audio, lang="en"):
    """Generate and play speech using gTTS."""
    tts = gTTS(text=audio, lang=lang)
    filename = "voice.mp3"
    tts.save(filename)
    st.audio(filename, format="audio/mp3")
    try:
        os.remove(filename)
    except:
        pass

def takeCommand():
    """Listen for a voice command and convert it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            st.info("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            st.success(f"✅ You said: {query}")
            return query
        except Exception:
            st.error("❌ Could not understand. Please try again.")
            return None

def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {
        1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
        4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'
    }
    speak(f"Today is {Day_dict.get(day)}")
    return f"Today is {Day_dict.get(day)}"

def tellTime():
    now = datetime.datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    speak(f"The time is {hour} hours and {minute} minutes")
    return f"The time is {hour}:{minute}"

def process_query(query):
    """Handle user commands and return output text."""
    if not query:
        return "No command received."

    query = query.lower()

    if "music" in query or "play some music" in query:
        speak("Playing music for you on YouTube")
        webbrowser.open("https://www.youtube.com/playlist?list=PLzAU9IV3j-jhG9RZrYJXglUnFSm1qPrJo")
        return "Playing music on YouTube"

    elif "youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")
        return "Opened YouTube"

    elif "google" in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        return "Opened Google"

    elif "linkedin" in query:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com/in/rohith-chelimilla-9b45922a7/")
        return "Opened LinkedIn"

    elif "github" in query:
        speak("Opening GitHub")
        webbrowser.open("https://github.com/chelimillarohith")
        return "Opened GitHub"

    elif "day" in query:
        return tellDay()

    elif "time" in query:
        return tellTime()

    elif "wikipedia" in query or "who is" in query:
        speak("Searching Wikipedia...")
        for word in ["wikipedia", "who is", "tell me about"]:
            query = query.replace(word, "")
        query = query.strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
            return result
        except:
            speak("Sorry, I couldn't find that on Wikipedia.")
            return "Wikipedia search failed."

    elif "your name" in query or "who are you" in query:
        speak("I am Rova, your desktop assistant.")
        return "I am Rova, your desktop assistant."

    elif any(word in query for word in ["bye", "exit", "stop"]):
        speak("Bye! Have a good day.")
        st.stop()
        return "Assistant stopped."

    else:
        speak("Sorry, I didn't understand that.")
        return "Command not recognized."


# ===== STREAMLIT FRONTEND =====
st.set_page_config(page_title="Rova - Desktop Assistant", page_icon="🎤", layout="centered")

st.markdown("<h1 style='text-align: center;'>🎤 Rova - Voice Assistant</h1>", unsafe_allow_html=True)

mic_icon = Path("mic.png")  # Place mic.png in same folder
if mic_icon.exists():
    st.image(str(mic_icon), width=150)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎙 Start Listening"):
        speak("Hello sir! I am Rova. How can I help you?")
        command = takeCommand()
        if command:
            result = process_query(command)
            st.write(f"**Response:** {result}")

with col2:
    if st.button("⏹ Stop Assistant"):
        speak("Assistant stopped.")
        st.stop()
        st.write("Assistant stopped.")
