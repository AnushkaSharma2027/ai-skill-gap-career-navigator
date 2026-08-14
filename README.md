# AI Skill-Gap Career Navigator

Analyzes your current skills against a target job role using the Gemini API, and generates a personalized, week-by-week learning roadmap.

## Setup (VS Code)

### 1. Create project folder and open in VS Code

```bash
mkdir ai-skill-gap-career-navigator
cd ai-skill-gap-career-navigator
code .
```

Copy all the project files into this folder.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it (Windows):

```bash
venv\Scripts\activate
```

Activate it (Mac/Linux):

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a free Gemini API key

Go to aistudio.google.com/app/apikey, sign in with your Google account, click Create API Key, and copy it.

### 5. Set up your API key

Copy .env.example to a new file named .env, then paste your key: