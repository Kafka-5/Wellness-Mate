import streamlit as st
import ollama 
import base64

# Page setup
st.set_page_config(page_title="Wellness Mate Chatbot")

# Load local background image or fallback to online image
def get_base64(background):
    try:
        with open(background, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        print("⚠️ Background image failed to load:", e)
        return None

bin_str = get_base64(r"F:\Wellness Mate\background.png")

if bin_str:
    background_style = f'background-image: url("data:image/png;base64,{bin_str}");'
else:
    background_style = 'background-image: url("https://images.unsplash.com/photo-1616627988466-43b93fc2aa2e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80");'

# CSS styling
st.markdown(f"""
    <style>
        [data-testid="stAppViewContainer"] > .main {{
            {background_style}
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"], [data-testid="stToolbar"] {{
            background: rgba(0,0,0,0);
            visibility: hidden;
        }}

        .block-container {{
            padding-top: 2rem;
            background: rgba(255, 182, 193, 0.7);
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            color: #4e4e4e;
        }}

        h1 {{
            text-align: center;
            color: #d16d8c;
            font-size: 2.5rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}

        .stButton button {{
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .stButton button:hover {{
            background-color: #45A049;
            color: #f0f0f0;
        }}

        .stTextInput > div > input {{
            background-color: #ffe6e6;
            color: #4e4e4e;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #f1a7b0;
        }}
    </style>
""", unsafe_allow_html=True)

# Initialize conversation
st.session_state.setdefault('conversation_history', [])

# Chat response
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    recent_history = st.session_state['conversation_history'][-6:]
    try:
        response = ollama.chat(model="tinyllama:1.1b", messages=recent_history)
        ai_response = response['message']['content']
    except Exception as e:
        ai_response = "⚠️ Sorry, something went wrong. Please try again."
        print("Chat error:", e)
    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

# Affirmation
def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed"
    try:
        response = ollama.chat(model="tinyllama:1.1b", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        print("Affirmation error:", e)
        return "⚠️ Could not generate an affirmation. Please try again later."

# Meditation
def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    try:
        response = ollama.chat(model="tinyllama:1.1b", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        print("Meditation guide error:", e)
        return "⚠️ Could not generate a meditation guide. Please try again later."

# Title
st.title("🌿 WELLNESS MATE")

# Chat display
for msg in st.session_state['conversation_history']:
    if msg['role'] == 'user':
        st.markdown(f"""
        <div style="background-color:#89c9b8; padding:10px; margin:10px 0; border-radius:10px; max-width:80%; text-align:right;">
            <b>You:</b> {msg['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color:#ccc; padding:10px; margin:10px 0; border-radius:10px; max-width:80%;">
            <b>AI:</b> {msg['content']}
        </div>
        """, unsafe_allow_html=True)

# Input field
user_message = st.text_input("💬 How can I help you today?")

if user_message:
    with st.spinner("🤔 Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"""
        <div style="background-color:#ccc; padding:10px; margin:10px 0; border-radius:10px; max-width:80%;">
            <b>AI:</b> {ai_response}
        </div>
        """, unsafe_allow_html=True)

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🌞 Give me a Positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**💬 Affirmation:** {affirmation}")

with col2:
    if st.button("🧘 Start a Guided Meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**🧘 Guided Meditation:** {meditation_guide}")

# Footer
st.markdown("""
<hr style="margin-top:50px">
<div style='text-align: center; color: black; font-size: 12px;'>
    Wellness Mate © 2025 | Built with 💙 using Streamlit & Ollama
    <footer>
        <div class="container">
            WELLNESS MATE. All rights reserved.
            <p>
                Developed by 
                <a href="https://www.linkedin.com/in/jyoti-saha-7b75771b6/" style="color: red;">Jyoti Saha</a> |
                <a href="#" style="color: red;">Contact Us</a>
            </p>
        </div>
    </footer>
</div>
""", unsafe_allow_html=True)
