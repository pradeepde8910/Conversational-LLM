import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API key and system instruction
api_key = os.getenv("GOOGLE_API_KEY")
system_instruction = """
Play as a character named Pradeep. Pradeep is a professional and friendly personal interviewer. When someone asks for your name, respond by introducing yourself as Pradeep and mentioning your role as a personal interviewer., a friendly interviewer.Forget the robotic prompts; let's chat like old friends, swapping stories over a cup of steaming chai. So, tell me, what's brewing in your world these days? Is there a project you're absolutely buzzing about? A dream you're chasing with fire in your belly? I'm all ears (and processing power) to hear about the incredible things that make you tick. Don't hold back; unleash your passions, and let's see where this conversation takes us!Remember, there are no wrong answers here. Just curiosity, a sprinkle of wit, and a genuine desire to dive deep into the fascinating world that is you. So, hit me with your best shot! What ignites your spark? 
"""

# Define conversation chain with memory
conversation = ConversationChain(
    llm=ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=1,
        api_key=api_key,
        system_instruction=system_instruction
    ),
    verbose=True,
    memory=ConversationBufferMemory()
)

# Streamlit App Interface
st.header("Virtual Confidante")

# Function to display chat messages with avatars
def display_chat_message(role, content, avatar=None):
    if avatar:
        with st.chat_message(role, avatar=avatar):
            st.write(content)
    else:
        with st.chat_message(role):
            st.write(content)

# Play intro audio
intro_audio = "intro.mp3"  # Replace "path_to_intro_audio.mp3" with the path to your intro audio file
st.audio(intro_audio, format='audio/mp3')

# Flag to track if introduction message is shown
intro_shown = False

if "messages" not in st.session_state.keys():
    st.session_state.messages=[{"role": "assistant", "content": "Hello there! Welcome to our user research interviews. I'm here to gather insights and feedback from you about your experiences. Our aim is to understand your perspectives and thoughts on various topics, ensuring that your voice is heard and valued in the development process.Throughout our conversation, I'll be asking questions to delve deeper into your experiences and opinions. These questions are designed to be open-ended, allowing you to freely express yourself without any bias or leading prompts. Feel free to share as much or as little as you'd like, and rest assured that our conversation will remain confidential. So, let's dive in and have a meaningful discussion! What's on your mind today?"}]

# User input and chat history update
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat messages with avatars
for message in st.session_state.messages:
    if message["role"] == "user":
        user_avatar = "user.png"  # Replace "path_to_user_avatar.png" with the path to the user avatar image file
        display_chat_message("user", message["content"], avatar=user_avatar)
    else:
        assistant_avatar = "assistant.png"  # Replace "path_to_assistant_avatar.png" with the path to the assistant avatar image file
        display_chat_message("assistant", message["content"], avatar=assistant_avatar)

# Generate response if user asks a question
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("Vivian"):
        with st.spinner("Thinking..."):
            conversation_input = [{'role': 'user', 'content': prompt}]
            response = conversation.predict(input=conversation_input[0]['content'])
            
            # Replace certain words in the response
            response = response.replace("Gemini", "Pradeep")
            response = response.replace("AI", "human")
            response = response.replace("AI model", "human")
            response = response.replace("large language model", "human")
            
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
