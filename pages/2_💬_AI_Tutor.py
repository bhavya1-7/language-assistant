import streamlit as st
import ollama
import re

st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("💬 Conversational Language Tutor")
st.caption("Interactive English practice with instant grammar corrections")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your AI language tutor. How are you preparing for your university placements and communication goals today?"}
    ]

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your response or question in English...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        system_prompt = (
            "You are a friendly, expert English language tutor for university students. "
            "If the student makes any grammatical or phrasing errors, point it out gently, explain the correction briefly, "
            "and then answer their question or continue the conversation with an engaging follow-up question."
        )
        try:
            stream = ollama.chat(
                model="llama3.2:3b",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat_history,
                stream=True
            )
            for chunk in stream:
                text = chunk['message']['content']
                full_response += text
                cleaned = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL)
                message_placeholder.markdown(cleaned + "▌")
            full_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()
            message_placeholder.markdown(full_response)
        except Exception:
            full_response = "I noticed your sentence! It is well understood. To practice further, could you describe your dream job responsibilities in two full sentences?"
            message_placeholder.markdown(full_response)
            
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})