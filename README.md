                                            AI HIRING ASSISTANT CHATBOT

PROJECT OVERVIEW:
The AI Hiring Assistant is an intelligent recruitment chatbot built using Streamlit and Google Gemini API. It automates candidate screening by collecting applicant information, generating technical interview questions based on skills, performing sentiment analysis on responses, and securely storing candidate data in CSV and JSON formats.
KEY CAPABILITIES:
•	Collects candidate information like full name, Email address, location, year of experience, technical skills etc.
•	Generates skill based technical interview questions.
•	Performs sentiment analysis on response.
•	Stores candidate data in CSV and JSON formats.
•	Maintain conversation context.
•	Provides fallback handling and privacy notice.
INSTALLATION INSTRUCTIONS:
1.	Clone the repository from GitHub.
2.	Create and activate a virtual environment.
3.	Install required libraries.
4.	Configure Gemini API key securely using Streamlit secrets.
5.	Run the application using: streamlit run app.py
Usage Guide
1.	Click 'Start Interview'.
2.	Enter candidate details.
3.	Proceed to Technical Round.
4.	Answer generated technical questions.
5.	Submit interview to store responses.
6.	Data is automatically saved in CSV and JSON formats.
Technical Details
Frontend: Streamlit
Backend: Python
AI Model: Google Gemini (Flash models)
Data Handling: Pandas and JSON
State Management: Streamlit session_state
The architecture follows a step-based workflow: Greeting → Candidate Information → Technical Question Generation → Answer Collection → Sentiment Analysis → Data Storage → Completion.
Prompt Design
Prompts were carefully structured to control output quality and ensure relevance.
•	Technical Question Prompt Design:
• Role assignment: 'You are a professional technical interviewer.'
• Constraint enforcement: Exactly 5 technical questions.
• Output formatting: Numbered list only.
• Restricted from asking HR or behavioral questions.
•	Sentiment Analysis Prompt Design:
• Returns only one word: Positive, Neutral, or Negative.
• Avoids long explanations to reduce API token usage.
Challenges & Solutions
1. API Quota Limits (429 Error):
   Solution: Optimized API calls and implemented retry handling.
2. Streamlit Auto-Rerun Behavior:
   Solution: Controlled logic using session_state.
3. Secure API Key Handling:
   Solution: Used Streamlit secrets instead of hardcoding keys.
4. Maintaining Context:
   Solution: Implemented structured step transitions.
Future Improvements:
•	Resume PDF upload and parsing
•	Automatic candidate scoring system
•	Admin dashboard
•	Database integration (SQLite)
•	Cloud deployment
