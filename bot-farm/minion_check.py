import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool, FileWriterTool

# Load your secret key
load_dotenv()

# 1. Setup the GLM-5 Engine
# Note: api.z.ai uses the OpenAI-compatible format
zai_llm = LLM(
    model="openai/glm-4.7", 
    base_url="https://api.z.ai/api/paas/v4/", 
    api_key=os.getenv("ZAI_API_KEY")
)

groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile", 
    api_key=os.getenv("GROQ_API_KEY")
)

# 2. Initialize the Tool
#file_tool = FileReadTool() 

# Instead of a blank tool, point it exactly where it needs to go.
# Since the script runs in bot-farm/, we tell it to look one level up (../)
file_reader = FileReadTool(file_path='../requirements.txt')
file_writer = FileWriterTool() # Can write to any path it is told to

# --- AGENT 1: The Scout ---
scout = Agent(
    role='Lead Scout',
    goal='Read the provided file and extract the raw data.',
    backstory='You are a highly precise reconnaissance bot.',
    llm=groq_llm,
    tools=[file_reader], 
    verbose=True
)

# --- AGENT 2: The Scribe ---
scribe = Agent(
    role='Technical Scribe',
    goal='Format data into a beautiful Markdown report and save it to the disk.',
    backstory='You are an expert technical writer who formats data and writes files locally.',
    llm=groq_llm,
    tools=[file_writer],
    verbose=True
)

# --- TASKS ---
read_task = Task(
    description='Use your tool to read the file and extract the list of libraries.',
    expected_output='A raw list of libraries.',
    agent=scout
)

write_task = Task(
    description='Take the list from the Scout. Use your FileWriterTool to write this list into a new file named "dependencies_report.md" inside the current directory. Format the text as a Markdown bulleted list.',
    expected_output='Confirmation that the dependencies_report.md file was successfully written.',
    agent=scribe
)

# --- THE CREW ---
# Notice how we pass both agents and both tasks in order!
crew = Crew(agents=[scout, scribe], tasks=[read_task, write_task], verbose=True) 
result = crew.kickoff()

print("\n--- MINION REPORT ---")
print(result)
