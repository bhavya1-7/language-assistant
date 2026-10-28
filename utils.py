import sqlite3
import re
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    conn = sqlite3.connect("data/app.db")
    students = pd.read_sql_query("SELECT * FROM students", conn)
    lessons = pd.read_sql_query("SELECT * FROM lessons", conn)
    conn.close()
    return students, lessons

def call_ollama(prompt, model="llama3.2:3b", system="You are an expert educational AI assistant."):
    try:
        import ollama
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        )
        raw_text = response['message']['content']
        # Strip DeepSeek or Llama think blocks if present
        clean_text = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
        return clean_text
    except Exception as e:
        return (
            "*(Local Ollama offline: Displaying pre-computed fallback response)*\n\n"
            "• **Key Focus Area:** Vocabulary and speaking skills show the highest variance across technical departments.\n"
            "• **Action Plan:** Prioritize short 15-minute daily active listening and presentation drills.\n"
            "• **Target:** Consistent practice to raise overall proficiency toward the 75+ Advanced threshold."
        )