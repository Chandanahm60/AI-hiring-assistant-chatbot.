import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os
import time
from datetime import datetime
from google.api_core.exceptions import ResourceExhausted

# =========================================
# CONFIGURE GEMINI (SECURE)
# =========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def load_model():
    return genai.GenerativeModel("models/gemini-2.5-flash")

model = load_model()

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(page_title="AI Hiring Assistant", page_icon="🤖")
st.title("🤖 AI Hiring Assistant")
st.caption("AI-Based Smart Technical Recruitment System")

# =========================================
# SESSION STATE
# =========================================
if "step" not in st.session_state:
    st.session_state.step = 0

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}

if "questions" not in st.session_state:
    st.session_state.questions = []

EXIT_WORDS = ["exit", "quit", "bye", "stop"]

# =========================================
# SAFE GEMINI CALL FUNCTION
# =========================================
def safe_generate(prompt):
    while True:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except ResourceExhausted:
            st.warning("⚠ API limit reached. Waiting 60 seconds...")
            time.sleep(60)

# =========================================
# GENERATE TECHNICAL QUESTIONS (1 API CALL)
# =========================================
def generate_questions(skills):

    prompt = f"""
    You are a professional technical interviewer.

    Generate exactly 5 technical interview questions 
    for a candidate skilled in: {skills}.

    Rules:
    - Only technical questions
    - No HR questions
    - Numbered list only
    """

    response_text = safe_generate(prompt)
    questions = response_text.split("\n")
    return [q for q in questions if q.strip()][:5]

# =========================================
# EVALUATE CANDIDATE (1 API CALL)
# =========================================
def evaluate_candidate(questions, answers):

    combined = ""
    for i in range(len(questions)):
        combined += f"""
        Question {i+1}: {questions[i]}
        Answer {i+1}: {answers[i]}
        """

    prompt = f"""
    You are a senior technical interviewer.

    Evaluate the candidate based on the following Q&A.

    Provide:
    1. Overall Sentiment (Positive / Neutral / Negative)
    2. Technical Level (Beginner / Intermediate / Advanced)
    3. Hiring Recommendation (Yes / No)
    4. Short Justification (2-3 lines)

    {combined}
    """

    return safe_generate(prompt)

# =========================================
# SAVE TO CSV
# =========================================
def save_to_csv(data):
    file = "candidates_data.csv"
    df = pd.DataFrame([data])

    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False, index=False)
    else:
        df.to_csv(file, index=False)

# =========================================
# SAVE TO JSON
# =========================================
def save_to_json(data):
    file = "candidates_data.json"

    if os.path.exists(file):
        with open(file, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(data)

    with open(file, "w") as f:
        json.dump(existing_data, f, indent=4)

# =========================================
# STEP 0 — GREETING
# =========================================
if st.session_state.step == 0:

    st.info("""
    👋 Welcome to the AI Hiring Assistant!

    🎯 Purpose:
    This chatbot collects candidate details and conducts
    a technical interview based on your skills.

    🔒 Privacy Notice:
    All candidate data is securely stored locally
    and used only for recruitment evaluation.
    """)

    if st.button("Start Interview"):
        st.session_state.step = 1
        st.rerun()

# =========================================
# STEP 1 — COLLECT DETAILS
# =========================================
elif st.session_state.step == 1:

    st.subheader("📋 Candidate Information")

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
    position = st.text_input("Desired Position")
    location = st.text_input("Current Location")
    skills = st.text_input("Technical Skills (comma separated)")

    if st.button("Proceed to Technical Round"):

        if name.lower() in EXIT_WORDS:
            st.success("Conversation Ended. Thank you!")
            st.stop()

        if name and email and phone and position and location and skills:

            candidate_id = f"CAND_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            st.session_state.candidate_data = {
                "Candidate_ID": candidate_id,
                "Full_Name": name,
                "Email_Address": email,
                "Phone_Number": phone,
                "Years_of_Experience": experience,
                "Desired_Position": position,
                "Current_Location": location,
                "Technical_Skills": skills,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            st.session_state.questions = generate_questions(skills)
            st.session_state.step = 2
            st.rerun()

        else:
            st.warning("⚠ Please fill all required fields.")

# =========================================
# STEP 2 — TECHNICAL ROUND
# =========================================
elif st.session_state.step == 2:

    st.subheader("💻 Technical Interview Round")

    answers = []

    for i, question in enumerate(st.session_state.questions):
        answer = st.text_area(question, key=f"answer_{i}")
        answers.append(answer)

    if st.button("Submit Interview"):

        if all(ans.strip() != "" for ans in answers):

            evaluation = evaluate_candidate(
                st.session_state.questions,
                answers
            )

            for i, ans in enumerate(answers):
                st.session_state.candidate_data[f"Technical_Answer_{i+1}"] = ans

            st.session_state.candidate_data["AI_Evaluation"] = evaluation

            save_to_csv(st.session_state.candidate_data)
            save_to_json(st.session_state.candidate_data)

            st.success("✅ Interview Completed Successfully!")
            st.session_state.step = 3
            st.rerun()

        else:
            st.warning("⚠ Please answer all questions.")

# =========================================
# STEP 3 — END MESSAGE
# =========================================
elif st.session_state.step == 3:

    st.balloons()
    st.success("🎉 Thank you for attending the AI Interview!")
    st.write("Our recruitment team will contact you soon.")