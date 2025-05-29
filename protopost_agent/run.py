import os
import yaml
import itertools
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from protopost import ProtoPost

from .templates import default_template
from .utils import toolify

#TODO: config port
#TODO: approval/feedback
#TODO: cli args for config file and debug/verbose flag
#TODO: system prompt?
#TODO: log for every step/tool call?
#TODO: other prompt templates/agents?
#TODO: chat history/sessions?
#TODO: allow calling tools with some context?
#TODO: handle tool failures (see https://python.langchain.com/docs/how_to/tools_error/)

class DebugCallbacks(BaseCallbackHandler):
    def __init__(self):
        super().__init__()
        #TODO: assumes only one tool can be called at a time
        self.last_tool = None

    def on_tool_start(self, tool, args, **kwargs):
        self.last_tool = tool["name"]
        print(f"Tool '{self.last_tool}' called with: {args}")

    def on_tool_end(self, output, **kwargs):
        print(f"Tool '{self.last_tool}' succeeded with: {output}")

    def on_tool_error(self, error, **kwargs):
        print(f"Tool '{self.last_tool}' errored with: {error}")

    def on_llm_end(self, response, **kwargs):
        gens = [g.message.content for g in itertools.chain(*response.generations)]
        print("LLM:", gens)

def main():
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

    debug_callbacks = DebugCallbacks()

    def run(prompt):
        res = agent_executor.invoke({"input": prompt}, {"callbacks": [debug_callbacks]})
        return res["output"]

    ProtoPost({"": run}).start(8123)

if __name__ == "__main__":
    main()