import streamlit as st
import json
import requests

# ----------------- SETUP -----------------
st.set_page_config(page_title=" DSA Whisper for beginners", page_icon="🧠", layout="wide")
st.title("🧩 DSA Whisper: Master DSA Step-by-Step with AI")

# Load DSA topics
with open("topics.json", "r") as f:
    topics = json.load(f)

# Groq API Setup
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# ----------------- SIDEBAR -----------------
st.sidebar.header("📚 Choose a DSA Topic")
topic_choice = st.sidebar.selectbox("Select Topic", list(topics.keys()))

selected_topic = topics[topic_choice]
st.subheader(selected_topic["title"])
st.write(selected_topic["explanation"])
st.code(selected_topic["example"], language="python")

st.markdown("---")
# 1️⃣ Difficulty Level
st.sidebar.markdown("### 🎚 Difficulty Level")
difficulty = st.sidebar.radio(
    "Choose Level",
    ["Beginner", "Intermediate", "Advanced"]
)


# 3️⃣ Tip of the Day
st.sidebar.markdown("### 💡 Tip of the Day")
tips = [
    "Practice dry-run on paper before coding.",
    "Focus on understanding logic, not memorizing code.",
    "Learn time complexity early — it helps everywhere!",
    "Solve easier problems first, then increase difficulty.",
    "Practice 10–15 minutes daily instead of long breaks."
]
import random
st.sidebar.info(random.choice(tips))

# ----------------- AI Chat Section -----------------
st.subheader("💬 Chat with DSA Whisper")

user_question = st.text_area(
    "Ask your question here about DSA or Python...",
    placeholder="e.g., Explain time complexity of bubble sort"
)

if st.button("Ask DSA Whisper"):
    if user_question.strip():
        with st.spinner("DSA Whisper is thinking..."):
            payload = {
                "model": "llama-3.1-8b-instant",   # ✅ Groq-supported model
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an intelligent tutoring assistant that explains Data Structures and Algorithms "
                            "step-by-step with simple examples and Python code. Keep answers clear and short."
                        ),
                    },
                    {"role": "user", "content": user_question},
                ],
                "temperature": 0.7,
                "max_tokens": 512
            }

            try:
                response = requests.post(API_URL, headers=headers, json=payload)

                if response.status_code != 200:
                    st.error(f"❌ API request failed with status {response.status_code}")
                    try:
                        st.json(response.json())
                    except:
                        st.write(response.text)
                else:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                    st.success("🤖 Tutor's Response:")
                    st.write(answer)

            except Exception as e:
                st.error(f"🚫 API Error: {e}")
    else:
        st.warning("Please enter a question before submitting.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit + Groq API")
