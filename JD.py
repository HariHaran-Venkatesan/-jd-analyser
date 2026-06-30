import anthropic
import json
import os
from dotenv import load_dotenv
load_dotenv()
while True:
    jd = input("\nPaste job description (or type 'exit' to quit): ")
    if jd.lower() == "exit":
        break
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
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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
