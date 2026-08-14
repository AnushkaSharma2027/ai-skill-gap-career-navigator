"""
gemini_helper.py
Handles all communication with the Gemini API.
Core idea: send one carefully engineered prompt that forces the model to
return STRICT JSON, so the Streamlit UI can render it reliably instead of
trying to parse loose free-text.
"""
 
import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
 
load_dotenv()
 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
 
MODEL_NAME = "gemini-3.6-flash"
 
 
def _configure():
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found. Create a .env file (see .env.example) "
            "and paste your key from https://aistudio.google.com/app/apikey"
        )
    genai.configure(api_key=GEMINI_API_KEY)
 
 
def _build_prompt(current_skills: str, target_role: str, roadmap_weeks: int) -> str:
    """
    The prompt is the 'brain' of this app. It:
    1. Gives the model a persona (career coach / technical recruiter)
    2. Gives explicit steps to reason through
    3. Forces a strict JSON schema so the output is parseable
    """
    return f"""
You are an expert technical career coach and recruiter who has hired for
hundreds of tech roles in India (including companies like TCS, Infosys,
Wipro, and product startups). You are precise, honest, and never pad your
answers with fluff.
 
TASK:
A candidate wants to work as a: "{target_role}"
 
Their current skills / background (may be raw resume text or a typed list):
---
{current_skills}
---
 
Do the following, reasoning step by step internally, but only output the
final JSON described below:
 
1. Determine the realistic, typical skill requirements for "{target_role}"
   in the current Indian tech job market — split into "must_have" and
   "good_to_have" skills.
2. Compare those requirements against the candidate's listed
   skills/background and infer which skills they already have (even if
   phrased differently, e.g. "REST APIs" counts as "API development").
3. Identify the SPECIFIC missing skills (the real gap) — must_have gaps
   and good_to_have gaps separately.
4. Generate a prioritized, week-by-week learning roadmap spanning
   {roadmap_weeks} weeks that closes the MUST-HAVE gaps first. Each week
   should have a clear focus, 2-4 concrete learning tasks, and 1-3 named
   learning resources (real, well-known resources: official docs,
   well-known free courses, YouTube channels, or practice platforms like
   LeetCode/HackerRank — do not invent fake URLs).
5. Add 3-5 likely technical interview topics/questions for this role given
   the candidate's current gap, so they can prioritize last-minute prep.
 
OUTPUT FORMAT:
Return ONLY valid JSON, no markdown code fences, no commentary, matching
EXACTLY this schema:
 
{{
  "target_role": "string",
  "matched_skills": ["skill the candidate already has", "..."],
  "missing_must_have": ["skill", "..."],
  "missing_good_to_have": ["skill", "..."],
  "roadmap": [
    {{
      "week": 1,
      "focus": "short title of the week's theme",
      "tasks": ["task 1", "task 2"],
      "resources": ["resource 1", "resource 2"]
    }}
  ],
  "likely_interview_topics": ["topic/question", "..."],
  "summary": "2-3 sentence honest overall assessment of how ready this candidate is right now"
}}
 
Return ONLY the JSON object, nothing else.
"""
 
 
def _extract_json(raw_text: str) -> dict:
    """
    Gemini sometimes wraps JSON in ```json ... ``` fences despite instructions.
    This strips those and parses safely.
    """
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned.strip(), flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned.strip()).strip()
 
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Last resort: grab the widest {...} block in the text
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Could not parse a valid JSON response from Gemini.")
 
 
def analyze_skill_gap(current_skills: str, target_role: str, roadmap_weeks: int = 4) -> dict:
    """
    Main function called by the Streamlit app.
    Sends the prompt to Gemini and returns a parsed dict.
    """
    _configure()
    model = genai.GenerativeModel(MODEL_NAME)
 
    prompt = _build_prompt(current_skills, target_role, roadmap_weeks)
 
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.4,  # lower = more consistent/structured output
            max_output_tokens=4096,
        ),
    )
 
    if not response.text:
        raise ValueError("Gemini returned an empty response. Try again.")
 
    return _extract_json(response.text)