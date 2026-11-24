
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from crewai import Agent, LLM


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env", override=True)

PROMPT_FILE = PROJECT_ROOT / "prompts" / "prompts.yaml"


def load_agent_prompt(agent_name):

    with open(PROMPT_FILE, "r", encoding="utf-8") as file:
        prompts = yaml.safe_load(file)

    return prompts[agent_name]


llm = LLM(
    model=os.getenv("GEMINI_MODEL"),
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4
)


def create_quiz_master():

    prompt = load_agent_prompt("quiz_master")

    quiz_master = Agent(
        role=prompt["role"],
        goal=prompt["goal"],
        backstory=prompt["backstory"],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    return quiz_master
