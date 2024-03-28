import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from mock_ATS import calculate_ats_percentage
from components.consts import ml_job_description, web_dev_job_description
import json
from langchain_openai import ChatOpenAI
import time

import logging
logging.basicConfig(level=logging.DEBUG)

start_time = time.time()

with open('data/resume_data.json', 'r') as f:
     resume_data = json.load(f)

def format_resume_from_json(resume_data):
    # Personal Information
    personal_info = resume_data.get("personal_info", {})
    personal_info_text = f"Name: {personal_info.get('name', '')}\n" \
                         f"Email: {personal_info.get('email', '')}\n" \
                         f"Phone: {personal_info.get('phone', '')}\n" \
                         f"LinkedIn: {personal_info.get('linkedin', '')}\n"

    # Education
    education_text = "Education:\n"
    for edu in resume_data.get("education", []):
        education_text += f" - {edu.get('school', '')}, {edu.get('degree', '')}, {edu.get('dates', '')}, GPA: {edu.get('GPA', '')}\n"

    # Experiences
    experiences_text = "Experiences:\n"
    for exp in resume_data.get("experiences", []):
        experiences_text += f" - {exp.get('company', '')}, {exp.get('title', '')}, {exp.get('dates', '')}\n" \
                            f"   {exp.get('details', '').replace('\\n', '\n   ')}\n"

    # Certifications
    certifications_text = "Certifications:\n"
    for cert in resume_data.get("certifications", []):
        certifications_text += f" - {cert.get('name', '')}, {cert.get('date', '')}\n   {cert.get('url', '')}\n"

    # Skills
    skills_text = "Skills:\n - " + ", ".join(resume_data.get("skills", [])) + "\n"

    # Combine all sections
    resume_text = personal_info_text + "\n" + education_text + "\n" + experiences_text + "\n" + certifications_text + "\n" + skills_text

    return resume_text

# Assuming resume_data is your loaded JSON object
resume_text = format_resume_from_json(resume_data)


load_dotenv(dotenv_path='.env.local')
OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ["OPENAI_API_KEY"] = OPEN_AI_API_KEY
os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key

# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

ats_tool = calculate_ats_percentage

# Define your agents with roles and goals
ats_scanner = Agent(
  role='ATS Scanner',
  goal='Scan resumes for ATS compatibility',
  backstory="""You are an ATS Scanner AI designed to evaluate resumes for their compatibility with Applicant Tracking Systems (ATS).""",
  verbose=True,
  allow_delegation=False,
  tools=[ats_tool],
  llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
)
resume_writer = Agent(
  role='Resume Writer',
  goal='Craft compelling resumes',
  backstory="""You are a Resume Writer AI designed to create compelling resumes that resonate with hiring managers and ATS systems.""",
  verbose=True,
  allow_delegation=True,
  llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
)

# Create tasks for your agents
task1 = Task(
  description=f"""Based on the following job description ({web_dev_job_description}), generate a resume that is well-aligned with the job requirements by selecting relevant experiences, certifications, and skills from the provided resume data ({resume_text}).""",
  expected_output="A well structured resume that is well-aligned with the job description",
  agent=resume_writer
)

task2 = Task(
  description="""Based on the generated resume, calculate the ATS compatibility percentage with the job description.""",
  expected_output="A percentage indicating the ATS compatibility of the resume with the job description",
  agent=ats_scanner
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[resume_writer, ats_scanner],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)

end_time = time.time()

total_time = end_time - start_time
print(f"Total time taken: {total_time} seconds")