import streamlit as st
from streamlit import session_state
import json
import os
import whisper
from st_audiorec import st_audiorec
import difflib
import speech_recognition as sr
from deep_translator import GoogleTranslator
session_state = st.session_state
if "user_index" not in st.session_state:
    st.session_state["user_index"] = 0
    
def transcribe_audio_from_data(file_data):
    with open("temp.mp3", "wb") as f:
        f.write(file_data)
    model = whisper.load_model("base")
    result = model.transcribe("temp.mp3",language="en")
    os.remove("temp.mp3")
    return result["text"]


# def check_mapping(transcription):
#     dictionary = {
#     ' கொள்ளும்பம்': 'FAMILY',
#     ' பிரியா விடை' : 'GOOD BYE',
#     ' வானக்கம்.' : 'HELLO' ,
#     ' வீட்டு' : 'HOUSE',
#     ' நான் உன்னைக் காதலிக்கிறேன்.': 'I LOVE YOU',
#     ' நான் உங்களைக்கு வெளக்குகிறேன்.' : 'I-WILL-EXPLAIN-IT',
#     ' காதல' : 'LOVE',
#     ' இல்லை.':'NO',
#     ' தாய்வை செய்து.': 'PLEASE',
#     ' மன்னிக்கவும்':'SORRY',
#     ' நண்டி':'THANK YOU',
#     ' அம்ம்.':'YES',
#     ' நீங்கள் வாழ வேறுக்கு படுகிறீர்கள்': 'YOU ARE WELCOME',
#     ' பயன': 'BOY',
#     ' கரினம':'DIFFICULT',
#     ' பியிலிமே?':'EASY',
#     ' மிகமுயில்லையில்லையும் அம்மா.': 'EXTREMELY TALL',
#     ' உன்னவு?':'FOOD',
#     ' பின்':'GIRL',
#     ' மடிய வானக்கம்': 'GOOD AFTERNOON',
#     ' மாலிய் வனக்கம்.':'GOOD EVENING',
#     ' காலையிவனக்கம்':'GOOD MORNING',
#     ' இனியையிரவு':'GOOD NIGHT',
#     ' அவன் மகுழ்ச்சியாகத் தயிருக்கிறான்.':'HE IS HAPPY',
#     ' தयpel':'HEAR',
#     ' யானக்கு தெரியாது.':'I DONT KNOW',
#     ' எனக்குப் புரிய விலி.':'I DONT UNDERSTAND',
#     ' உங்களை சந்தித்ததில் மகிழ்ச்சி':'NICE TO MEET YOU',
#     ' வலவானே': 'STRONG',
#     ' நீ என்ன செய்து கொண்டிருக்கிறாய்':'WHAT ARE YOU DOING',
#     ' மீங்கள் எடுக்கிறாய்?':'WHERE ARE YOU'
#     }
#     dict_1={
#     'FAMILY' : ' குடும்பம்',
#     'GOOD BYE':' பிரியா விடை',
#     'HELLO': ' வணக்கம்.',
#     'HOUSE':' வீடு.',
#     'I LOVE YOU':' நான் உன்னைக் காதலிக்கிறேன்.',
#     'I-WILL-EXPLAIN-IT':' நான் உங்களுக்கு விளக்குகிறேன்.',
#     'LOVE':' காதல்',
#     'NO':' இல்லை.',
#     'PLEASE':' தயவு செய்து.',
#     'SORRY':' மன்னிக்கவும்',
#     'THANK YOU':' நன்றி',
#     'YES':' ஆம்.',
#     'YOU ARE WELCOME':' நீங்கள் வரவேற்கப்படுகிறீர்கள்.',
#     'BOY':'பையன்',
#     'DIFFICULT':'கடினமான',
#     'EASY':'எளிமை',
#     'EXTREMELY TALL':'மிக உயரமான',
#     'FOOD':'உணவு',
#     'GIRL':'பெண்',
#     'GOOD AFTERNOON':'மதிய வணக்கம்',
#     'GOOD EVENING':'மாலை வணக்கம்',
#     'GOOD MORNING':'காலை வணக்கம்',
#     'GOOD NIGHT':'இனிய இரவு',
#     'HE IS HAPPY':'அவனஂ மகிழஂசஂசியாக இருகஂகிறானஂ',
#     'HEAR':'கேள்',
#     'I DONT KNOW':'எனக்கு தெரியாது',
#     'I DONT UNDERSTAND':'எனக்கு புரியவில்லை',
#     'NICE TO MEET YOU':'உங்களை சந்தித்ததில் மகிழ்ச்சி',
#     'STRONG':'வலுவான',
#     'WHAT ARE YOU DOING':'நீ என்ன செய்து கொண்டு இருக்கிறாய்?',
#     'WHERE ARE YOU':'நீ எங்கே இருக்கிறாய்?'
#     }
#     if transcription in dictionary :
#         t = dictionary[transcription]
#         return dictionary[transcription] , dict_1[t]
    
#     else: 
#         return 'Cant Understand the audio','Try Again'

def signup(json_file_path="data.json"):
    st.title("Signup Page")
    with st.form("signup_form"):
        st.write("Fill in the details below to create an account:")
        name = st.text_input("Name:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=120)
        sex = st.radio("Sex:", ("Male", "Female", "Other"))
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")
        
        if st.form_submit_button("Signup"):
            if password == confirm_password:
                user = create_account(
                    name,
                    email,
                    age,
                    sex,
                    password,
                    json_file_path,
                )
                session_state["logged_in"] = True
                session_state["user_info"] = user
            else:
                st.error("Passwords do not match. Please try again.")


def check_login(username, password, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        for user in data["users"]:
            if user["email"] == username and user["password"] == password:
                session_state["logged_in"] = True
                session_state["user_info"] = user
                st.success("Login successful!")
                return user
        return None
    except Exception as e:
        st.error(f"Error checking login: {e}")
        return None


def initialize_database(json_file_path="data.json"):
    try:
        if not os.path.exists(json_file_path):
            data = {"users": []}
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file)
    except Exception as e:
        print(f"Error initializing database: {e}")


def create_account(
    name,
    email,
    age,
    sex,
    password,
    json_file_path="data.json",
):
    try:

        if not os.path.exists(json_file_path) or os.stat(json_file_path).st_size == 0:
            data = {"users": []}
        else:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

        # Append new user data to the JSON structure
        user_info = {
            "name": name,
            "email": email,
            "age": age,
            "sex": sex,
            "password": password,
        }
        data["users"].append(user_info)

        # Save the updated data to JSON
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        st.success("Account created successfully! You can now login.")
        return user_info
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return None


def login(json_file_path="data.json"):
    st.title("Login Page")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    login_button = st.button("Login")

    if login_button:
        user = check_login(username, password, json_file_path)
        if user is not None:
            session_state["logged_in"] = True
            session_state["user_info"] = user
        else:
            st.error("Invalid credentials. Please try again.")


def get_user_info(email, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for user in data["users"]:
                if user["email"] == email:
                    return user
        return None
    except Exception as e:
        st.error(f"Error getting user information: {e}")
        return None

def render_dashboard(user_info, json_file_path="data.json"):
    try:
        st.title(f"Welcome to the Dashboard, {user_info['name']}!")
        
        st.subheader("User Information:")
        st.write(f"Name: {user_info['name']}")
        st.write(f"Sex: {user_info['sex']}")
        st.write(f"Age: {user_info['age']}")
        st.image("image.jpeg", caption="Bridging Communication Gaps", use_column_width=True)
        
    except Exception as e:
        st.error(f"Error rendering dashboard: {e}")


def main(json_file_path="data.json"):

    st.sidebar.title("Bridging Communication Gaps")
    page = st.sidebar.radio(
        "Go to",
        (
            "Signup/Login",
            "Dashboard",
            "Bridge Communication Gaps",
        ),
        key="Bridging Communication Gaps",
    )

    if page == "Signup/Login":
        st.title("Signup/Login Page")
        login_or_signup = st.radio(
            "Select an option", ("Login", "Signup"), key="login_signup"
        )
        if login_or_signup == "Login":
            login(json_file_path)
        else:
            signup(json_file_path)

    elif page == "Dashboard":
        if session_state.get("logged_in"):
            render_dashboard(session_state["user_info"])
        else:
            st.warning("Please login/signup to view the dashboard.")
            
            
    elif page == "Bridge Communication Gaps":
        if session_state.get("logged_in"):
            user_info = session_state["user_info"]
            st.title("Bridge Communication Gaps")
            st.write("Record or upload an audio file to get the sign")
            paths = {}            
            signs = []
            for video in os.listdir("videos"):
                path = "videos//"+video
                sign = video.split(".")[0]
                paths[sign] = path
                signs.append(sign)
            options = ["Record", "Upload"]
            choice = st.radio("Choose an option", options)
            if choice == "Record":
                # st.write("Click the button below to start recording:")
                # audio = st_audiorec()
                # if audio is not None:
                #     transcription = transcribe_audio_from_data(audio).upper()
                recognizer = sr.Recognizer()
                microphone = sr.Microphone()
                if st.button("START RECORDING"):
                    with microphone as source:
                        st.info("Listening...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)   
                        try:
                            voice_command = recognizer.recognize_google(audio, language="en")
                            print(voice_command)
                        except sr.UnknownValueError:
                            st.write("Could not understand the audio. Please try again.")
                            # st.rerun()
                            return
                            
                        except sr.RequestError as e:
                            st.write("Could not understand the audio. Please try again.")
                            # st.rerun()
                            return
                    if voice_command:
                        # trans,tamil_trans= check_mapping(voice_command_tamil.upper())
                        # st.write('English:',trans)
                        # st.write('Tamil:',tamil_trans)
                        
                        st.write('English:',voice_command.upper())
                       
                        words = difflib.get_close_matches(voice_command.upper(),signs,cutoff=0.2)
                        
                        print(words)
                        # st.write(trans)
                        word = "HELLO"
                        if len(words)>0:
                            word = words[0]
                        st.image(paths[word], caption=word, use_column_width=True)
            elif choice == "Upload":
                st.write("Upload an audio file:")
                audio = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])
                if audio is not None:
                    st.audio(audio, format="audio/wav")
                    transcription = transcribe_audio_from_data(audio.read()).upper()
                    if transcription:
                    
                        st.write('English:',transcription)

                       
                        words = difflib.get_close_matches(transcription,signs,cutoff=0.2)
                        # st.write(words)
                        if len(words)>0:
                            word = words[0]
                        st.image(paths[word], caption=word, use_column_width=True)

        else:
            st.warning("Please login/signup to bridge communication gaps.")
if __name__ == "__main__":
    initialize_database()
    main()
