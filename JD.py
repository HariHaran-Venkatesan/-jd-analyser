import anthropic

import os
from dotenv import load_dotenv
load_dotenv()
jd = input("Paste the job description: ")
prompt = f"""You are an expert technical recruiter. Analyze this job description and extract:

1. REQUIRED SKILLS (must-have)
2. NICE TO HAVE SKILLS (preferred)
3. EXPERIENCE LEVEL (junior/mid/senior + years)
4. SALARY RANGE (if mentioned, else say "Not disclosed")
5. RED FLAGS (anything unusual or concerning)
6. ESTIMATED INDIA SALARY RANGE: Based on the role, skills, and experience level, 
estimate realistic salary range for Hyderabad and Bangalore markets in LPA."

Job Description:
{jd}

Be specific and concise."""
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

messages = client.messages.create(
    model = "claude-haiku-4-5-20251001",
    max_tokens=512,
    messages= [{"role": "user", "content": prompt}])
print(messages.content[0].text)


