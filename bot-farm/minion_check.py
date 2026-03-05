import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# Load your secret key
load_dotenv()

# 1. Setup the GLM-5 Engine
# Note: api.z.ai uses the OpenAI-compatible format
zai_llm = LLM(
    model="openai/glm-4.7", 
    base_url="https://api.z.ai/api/paas/v4/", 
    api_key=os.getenv("ZAI_API_KEY")
)

# 2. Define your first Minion
scout = Agent(
    role='Lead Scout',
    goal='Verify the connection and report back your current system status.',
    backstory='You are a high-speed reconnaissance bot built by z.ai.',
    llm=zai_llm,
    verbose=True
)

# 3. Give them a simple task
test_task = Task(
    description='Tell me one interesting fact about the GLM-4.7 model you are running on.',
    expected_output='A single, fascinating sentence.',
    agent=scout
)

# 4. Kick it off
crew = Crew(agents=[scout], tasks=[test_task])
result = crew.kickoff()

print("\n--- MINION REPORT ---")
print(result)
