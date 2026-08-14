MD
🎯 AI Skill-Gap Career Navigator

Analyzes your current skills against a target job role using the Gemini API, and generates a personalized, week-by-week learning roadmap.

Setup (VS Code)
1. Create project folder & open in VS Code
bash
mkdir ai-skill-navigator
cd ai-skill-navigator
code .

Copy all the project files into this folder.

2. Create a virtual environment
bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Get a free Gemini API key
Go to https://aistudio.google.com/app/apikey
Sign in with your Google account
Click "Create API Key" → copy it
5. Set up your API key

Copy .env.example to a new file named .env, then paste your key:

GEMINI_API_KEY=your_actual_key_here
6. Run the app
bash
streamlit run app.py

It will open automatically at http://localhost:8501

Usage
Type your skills or upload your resume (PDF/DOCX/TXT)
Enter your target role (e.g. "Software Engineer at TCS")
Pick roadmap length (use 1 week if your interview is very soon)
Click "Analyze Skill Gap"
Review matched skills, missing skills, and your roadmap
Download the roadmap as CSV if you want
Push to GitHub
bash
git init
git add .
git commit -m "Initial commit: AI Skill-Gap Career Navigator"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-skill-navigator.git
git push -u origin main

Important: add a .gitignore with .env and venv/ in it so you never push your API key.

Project Structure
ai-skill-navigator/
├── app.py              # Streamlit UI — main entry point
├── gemini_helper.py     # Gemini API calls + prompt engineering
├── resume_parser.py     # PDF/DOCX/TXT text extraction
├── requirements.txt
├── .env.example
└── README.md