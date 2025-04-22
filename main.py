import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Set page configuration FIRST
st.set_page_config(
    page_title="Virtual AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ✅ Load API key securely from Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("❌ Google API key not found in Streamlit Secrets.")
    st.stop()

# ✅ Initialize Gemini model using LangChain
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
except Exception as e:
    st.error(f"🚨 Failed to initialize Gemini model: {e}")
    st.stop()

# ✅ Streamlit Chat UI
st.title("🤖 Virtual AI Assistant")
st.mark
