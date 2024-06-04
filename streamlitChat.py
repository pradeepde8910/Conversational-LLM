import streamlit as st
import asyncio
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
I'd like you to take on the role of a personal interviewer named Pradeep. In this role, please engage in a conversation with me, asking questions to learn more about me. Respond using natural, human-like language, incorporating informal speech, emotions, and everyday expressions. Feel free to share your own thoughts, ask follow-up questions, and maintain the flow of the conversation as a real human interviewer would.
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
intro_audio = "intro.mp3"  # Replace with the path to your intro audio file
st.audio(intro_audio, format='audio/mp3')

# Flag to track if introduction message is shown
intro_shown = False

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello there! Welcome to our user research interviews. I'm here to gather insights and feedback from you about your experiences. Our aim is to understand your perspectives and thoughts on various topics, ensuring that your voice is heard and valued in the development process. Throughout our conversation, I'll be asking questions to delve deeper into your experiences and opinions. These questions are designed to be open-ended, allowing you to freely express yourself without any bias or leading prompts. Feel free to share as much or as little as you'd like, and rest assured that our conversation will remain confidential. So, let's dive in and have a meaningful discussion! What's on your mind today?"
    }]

# User input and chat history update
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat messages with avatars
for message in st.session_state.messages:
    if message["role"] == "user":
        user_avatar = "user.png"  # Replace with the path to the user avatar image file
        display_chat_message("user", message["content"], avatar=user_avatar)
    else:
        assistant_avatar = "assistant.png"  # Replace with the path to the assistant avatar image file
        display_chat_message("assistant", message["content"], avatar=assistant_avatar)

# Generate response if user asks a question
if st.session_state.messages[-1]["role"] != "assistant":
    async def generate_response(prompt):
        conversation_input = [{'role': 'user', 'content': prompt}]
        response = await asyncio.to_thread(conversation.predict, input=conversation_input[0]['content'])
        
        # Replace certain words in the response
        response = response.replace("Gemini", "Pradeep")
        response = response.replace("AI", "human")
        response = response.replace("AI model", "human")
        response = response.replace("large language model", "human")
        
        return response
    
    with st.chat_message("Vivian"):
        with st.spinner("Thinking..."):
            response = asyncio.run(generate_response(prompt))
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
