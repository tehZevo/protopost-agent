import os
import yaml
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from protopost import ProtoPost

from templates import default_template
from utils import toolify

#TODO: goal:
#- chat/session history (langchain?)
#TODO:  system prompt?
#TODO: log for every step/tool call?
#TODO: other prompt templates/agents?
#TODO: chat history/sessions?
#TODO: allow calling with some context?

with open("config.yml", "r") as f:
  config = yaml.safe_load(f)

OLLAMA_MODEL = config["ollama"]["model"]
OLLAMA_HOST = config["ollama"]["api_url"]
os.environ["OLLAMA_HOST"] = OLLAMA_HOST

model = ChatOllama(model=OLLAMA_MODEL)
prompt = PromptTemplate.from_template(default_template)
tools = [toolify(route) for route in config["routes"]]
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

def run(prompt):
    res = agent_executor.invoke({"input": prompt})
    return res["output"]

ProtoPost({"": run}).start(8123)