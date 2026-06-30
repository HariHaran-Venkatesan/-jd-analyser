import anthropic
import json
import os
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

import datetime

def save_result(data, jd_text):
    record = {
        "timestamp": str(datetime.datetime.now()),
        "jd_snippet": jd_text[:100],
        "analysis": data
    }
    
    try:
        with open("jd_history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    
    history.append(record)
    
    with open("jd_history.json", "w") as f:
        json.dump(history, f, indent=2)


def analyse_jd(jd_text, client):
    prompt = f"""Analyze this job description and respond with ONLY valid JSON (no markdown, no explanation) in this exact format:

{{
  "required_skills": ["skill1", "skill2"],
  "nice_to_have_skills": ["skill1", "skill2"],
  "experience_level": "junior/mid/senior",
  "experience_years": "estimated range",
  "salary_disclosed": true/false,
  "estimated_salary_hyderabad_lpa": "range",
  "estimated_salary_bangalore_lpa": "range",
  "red_flags": ["flag1", "flag2"]
}}

Job Description:
{jd}"""

    
    messages = client.messages.create(
        model = "claude-haiku-4-5-20251001",
        max_tokens=512,
        messages= [{"role": "user", "content": prompt}])

    response_text = messages.content[0].text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    data = json.loads(response_text)

    print("Required Skills:", data["required_skills"])
    print("Experience Level:", data["experience_level"])
    print("Hyderabad Salary:", data["estimated_salary_hyderabad_lpa"])
    my_estimate = input("Based on your experience, what's the real Hyderabad salary range? (or press Enter to skip): ")
    data["my_salary_estimate"] = my_estimate
    return data

def load_resume():
    with open("resume.txt", "r", encoding="utf-8") as f:
        return f.read()
     
def fit_score(jd_text, resume_text, client):
    prompt = f"""You are an expert technical recruiter. Compare this resume against this job description.

Respond with ONLY valid JSON in this format:
{{
  "fit_score": "0-100",
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "verdict": "one sentence honest verdict",
  "what_to_add_to_resume": ["suggestion1", "suggestion2"]
}}

RESUME:
{resume_text}
JOB DESCRIPTION:
{jd_text}"""
    messages = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    response_text = messages.content[0].text.strip()
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()
    return json.loads(response_text)


while True:
    jd = input("Paste job description (or type 'exit' to quit : ")
    if jd.lower() == "exit":
        break
    data = analyse_jd(jd, client)
    fit = fit_score(jd, load_resume(), client)
    data["fit_analysis"] = fit
    save_result(data, jd)
    print("\nFit Score:", fit["fit_score"])
    print("Missing Skills:", fit["missing_skills"])
    print("Verdict:", fit["verdict"])
    
