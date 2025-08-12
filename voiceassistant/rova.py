import streamlit as st
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
from pathlib import Path

# ====== SPEECH ENGINE FUNCTION ======
def speak(audio, selected_voice):
    """Speak the given text with selected voice."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[selected_voice].id)
    engine.say(audio)
    engine.runAndWait()

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

def tellDay(selected_voice):
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {
        1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
        4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'
    }
    speak(f"Today is {Day_dict.get(day)}", selected_voice)
    return f"Today is {Day_dict.get(day)}"

def tellTime(selected_voice):
    now = datetime.datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    speak(f"The time is {hour} hours and {minute} minutes", selected_voice)
    return f"The time is {hour}:{minute}"

def process_query(query, selected_voice):
    """Handle user commands and return output text."""
    if not query:
        return "No command received."

    query = query.lower()

    if "music" in query or "play some music" in query:
        speak("Playing music for you on YouTube", selected_voice)
        webbrowser.open("https://www.youtube.com/playlist?list=PLzAU9IV3j-jhG9RZrYJXglUnFSm1qPrJo")
        return "Playing music on YouTube"

    elif "youtube" in query:
        speak("Opening YouTube", selected_voice)
        webbrowser.open("https://www.youtube.com/")
        return "Opened YouTube"

    elif "google" in query:
        speak("Opening Google", selected_voice)
        webbrowser.open("https://www.google.com")
        return "Opened Google"

    elif "linkedin" in query:
        speak("Opening LinkedIn", selected_voice)
        webbrowser.open("https://www.linkedin.com/in/rohith-chelimilla-9b45922a7/")
        return "Opened LinkedIn"

    elif "github" in query:
        speak("Opening GitHub", selected_voice)
        webbrowser.open("https://github.com/chelimillarohith")
        return "Opened GitHub"

    elif "day" in query:
        return tellDay(selected_voice)

    elif "time" in query:
        return tellTime(selected_voice)

    elif "wikipedia" in query or "who is" in query:
        speak("Searching Wikipedia...", selected_voice)
        for word in ["wikipedia", "who is", "tell me about"]:
            query = query.replace(word, "")
        query = query.strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result, selected_voice)
            return result
        except:
            speak("Sorry, I couldn't find that on Wikipedia.", selected_voice)
            return "Wikipedia search failed."

    elif "your name" in query or "who are you" in query:
        speak("I am Rova, your desktop assistant.", selected_voice)
        return "I am Rova, your desktop assistant."

    elif any(word in query for word in ["bye", "exit", "stop"]):
        speak("Bye! Have a good day.", selected_voice)
        st.stop()
        return "Assistant stopped."

    else:
        speak("Sorry, I didn't understand that.", selected_voice)
        return "Command not recognized."


# ===== STREAMLIT FRONTEND =====
st.set_page_config(page_title="Rova - Desktop Assistant", page_icon="🎤", layout="centered")

st.markdown("<h1 style='text-align: center;'>🎤 Rova - Voice Assistant</h1>", unsafe_allow_html=True)

# ===== VOICE SELECTION =====
voice_choice = st.selectbox("Select Voice", ("Male Voice (voice[0])", "Female Voice (voice[1])"))
selected_voice_index = 0 if "Male" in voice_choice else 1

mic_icon = Path("mic.png")  # Place mic.png in same folder
if mic_icon.exists():
    st.image(str(mic_icon), width=150)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎙 Start Listening"):
        speak("Hello sir! I am Rova. How can I help you?", selected_voice_index)
        command = takeCommand()
        if command:
            result = process_query(command, selected_voice_index)
            st.write(f"**Response:** {result}")

with col2:
    if st.button("⏹ Stop Assistant"):
        speak("Assistant stopped.", selected_voice_index)
        st.stop()
        st.write("Assistant stopped.")
        
