import anthropic
import json
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt_template = ChatPromptTemplate.from_template(
    """Analyze this job description and respond with ONLY valid JSON in this format:
{{
  "required_skills": ["skill1", "skill2"],
  "experience_level": "junior/mid/senior",
  "estimated_salary_hyderabad_lpa": "range"
}}

Job Description:
{jd}"""
)
parser = JsonOutputParser()
chain = prompt_template | llm | parser

while True:
    jd = input("Paste job description (or type 'exit' to quit : ")
    if jd.lower() == "exit":
        break
    
    result = chain.invoke({"jd": jd})
    print(result)
