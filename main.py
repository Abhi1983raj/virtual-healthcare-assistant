import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Secure API Key Access ---
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "YOUR_ACTUAL_API_KEY_HERE")

if os.environ["GOOGLE_API_KEY"] == "YOUR_ACTUAL_API_KEY_HERE":
    st.warning("⚠️ Please set your GOOGLE_API_KEY as a Streamlit Secret for better security!")

# --- Initialize LLM ---
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
except Exception as e:
    st.error(f"❌ Error initializing Gemini Pro:\n\n`{e}`")
    st.stop()

# --- Streamlit App UI ---
st.set_page_config(page_title="Virtual AI Assistant", page_icon="🤖")
st.title("🤖 Virtual AI Assistant")
st.markdown("Welcome! Ask me anything and I'll do my best to assist you.")

# --- Chat State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! 👋 How can I assist you today?"}
    ]

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input Handling ---
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = llm.invoke(prompt)

            # Optional: fix bullets for markdown rendering
            content = response.content.replace("* ", "- ")

            # Handle line-by-line display for better formatting
            for line in content.splitlines():
                full_response += line + "\n"
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_message = f"❗ Sorry, I encountered an error:\n\n`{e}`"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            message_placeholder.markdown(error_message)
