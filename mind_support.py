import streamlit as st
import ollama
import base64

# Page config
st.set_page_config(page_title="Mental Health Chatbot")

# === Constants ===
MODEL_NAME = "llama3:8b"
BACKGROUND_IMAGE = "background.png"

# === Background Setup ===
def get_base64(background_path):
    try:
        with open(background_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Background image not found at '{background_path}'. Make sure it exists.")
        return None

bin_str = get_base64(BACKGROUND_IMAGE)
if bin_str:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# === Session State ===
st.session_state.setdefault('conversation_history', [])

# === Response Generation Functions ===
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    try:
        response = ollama.chat(model=MODEL_NAME, messages=st.session_state['conversation_history'])
        ai_response = response['message']['content']
        st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
        return ai_response
    except Exception as e:
        st.error(f"Error from Ollama: {e}")
        return "Sorry, I had an issue responding."

@st.cache_data(show_spinner=False)
def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        st.error(f"Affirmation error: {e}")
        return "Sorry, couldn't generate an affirmation now."

@st.cache_data(show_spinner=False)
def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        st.error(f"Meditation guide error: {e}")
        return "Sorry, couldn't generate a meditation guide right now."

# === UI ===
st.title("🧠 Mental Health Support Agent")

# Display past conversation
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# === User Input ===
user_message = st.text_input("How can I help you today?", key="user_input")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# === Buttons ===
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive Affirmation"):
        with st.spinner("Generating affirmation..."):
            affirmation = generate_affirmation()
            st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        with st.spinner("Generating meditation..."):
            meditation = generate_meditation_guide()
            st.markdown(f"**Guided Meditation:** {meditation}")
