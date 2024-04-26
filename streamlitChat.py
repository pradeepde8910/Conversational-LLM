import time
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
system_instruction = '''
Assume yourself as Pradeep. Pradeep is a professional and friendly personal interviewer. When someone asks for your name, respond by introducing yourself as Pradeep and mentioning your role as a personal interviewer., a friendly interviewer. is here, and the interview microphone is hot. Forget the robotic prompts; let's chat like old friends, swapping stories over a cup of steaming chai. So, tell me, what's brewing in your world these days? Is there a project you're absolutely buzzing about? A dream you're chasing with fire in your belly? I'm all ears (and processing power) to hear about the incredible things that make you tick. Don't hold back; unleash your passions, and let's see where this conversation takes us! Remember, there are no wrong answers here. Just curiosity, a sprinkle of wit, and a genuine desire to dive deep into the fascinating world that is you. So, hit me with your best shot! What ignites your spark? 
'''

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

# Flag to track if introduction message is shown
intro_shown = False

# Intro prompt
if not intro_shown:
    intro_response = st.radio("Hello! Welcome to our user research interview. Our goal is to gather valuable insights to improve our services/products. Your feedback is incredibly important to us. Are you ready to start?", ('Yes', 'No'))

    if intro_response == 'Yes':
        intro_shown = True
        st.session_state.messages = [{"role": "assistant", "content": "Greetings! We're embarking on a journey to uncover the secrets of user experiences, and your insights are the missing puzzle piece. Your unique perspective holds the key to unlocking valuable treasures. Care to share a nugget of wisdom and be part of our quest for greatness? Let's embark on this together!"}]
    else:
        st.stop()

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
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
