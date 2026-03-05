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

file_reader = FileReadTool(file_path='../requirements.txt') 
file_writer = FileWriterTool() 

scout = Agent(
    role='Lead Scout',
    goal='Read the provided file and extract the raw data.',
    backstory='You are a highly precise reconnaissance bot.',
    llm=groq_llm,
    tools=[file_reader], 
    verbose=True
)

scribe = Agent(
    role='Technical Scribe',
    goal='Format data into a beautiful Markdown report and save it to the disk.',
    backstory='You are an expert technical writer who formats data and writes files locally.',
    llm=groq_llm,
    tools=[file_writer],
    verbose=True
)

read_task = Task(
    description='Use your tool to read the file and extract the list of libraries.',
    expected_output='A raw list of libraries.',
    agent=scout
)

write_task = Task(
    description='Take the list from the Scout. Use your FileWriterTool to write this list into a new file named "dependencies_report.md" inside the current directory. Format the text as a Markdown bulleted list.',
    expected_output='Confirmation that the file was successfully written.',
    agent=scribe
)

# --- THE UPGRADED CREW ---
crew = Crew(
    agents=[scout, scribe], 
    tasks=[read_task, write_task], 
    verbose=True,
    memory=True, # 1. Turn on the memory systems
    embedder={   # 2. Force it to use the free local HuggingFace model
        "provider": "huggingface",
        "config": {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "api_key": "not-needed" # This tricks the validator to stop asking for a real key            
        }
    }
) 

result = crew.kickoff()

print("\n--- MASTER CONTROL REPORT ---")
print(result)