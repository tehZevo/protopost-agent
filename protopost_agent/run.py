import os
import yaml
import time
import argparse
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from protopost import ProtoPost

from .utils import toolify, make_prompt

#TODO: retry N times on output parsing failure
#TODO: approval/feedback
#TODO: cli args for config file and debug/verbose flag
#TODO: system prompt?
#TODO: log for every step/tool call?
#TODO: other prompt templates/agents?
#TODO: chat history/sessions?
#TODO: allow calling tools with some context?
#TODO: handle tool failures (see https://python.langchain.com/docs/how_to/tools_error/)
#TODO: add a sleep tool with config flag
#TODO: prototools: @prototool annotation that can be used as a protopost route list available tools
#TODO: trim think

parser = argparse.ArgumentParser()
group = parser.add_argument_group("mode")
#TODO: descriptions ("description")
group.add_argument("-s", "--service", action="store_const", dest="mode", const="service")
group.add_argument("-a", "--autonomous", action="store_const", dest="mode", const="autonomous")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-i", "--max-iterations", type=int, default=10)
parser.add_argument("-p", "--port", type=int, default="8123")
parser.add_argument("-l", "--loop", action="store_true")
parser.add_argument("-d", "--delay", type=float, default=3)
parser.add_argument("-n", "--niceness", type=float, default=1)
args, MESSAGE = parser.parse_known_args()

if len(MESSAGE) > 0:
    MESSAGE = " ".join(MESSAGE)
else:
    MESSAGE = None

PORT = args.port
CONFIG_PATH = "config.yml" #TODO: argparse me
VERBOSE = args.verbose
MAX_ITERATIONS = args.max_iterations
MODE = args.mode if args.mode is not None else "interactive"
DELAY = args.delay
NICENESS = args.niceness
LOOP = args.loop

#TODO: run interactive with user message if provided as argv 2
def interactive_runner(model, tools, system_prompt, message):
    #TODO: chat history ConversationBufferWindowMemorys
    #TODO: show loading indicator? #TODO: stream output?

    prompt = make_prompt(system_prompt, True, False)
    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=MAX_ITERATIONS, verbose=VERBOSE)
    
    if message is not None:
        res = agent_executor.invoke({"user_message": message})
        print(res["output"])
        exit(0)
        
    while True:
        message = input("> ")
        if message == "/bye":
            exit(0)
        
        res = agent_executor.invoke({"user_message": message})
        print(res["output"])

def service_runner(model, tools, system_prompt):
    #TODO: chat history with sessions(?)
    prompt = make_prompt(system_prompt, True, False)
    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=MAX_ITERATIONS, verbose=VERBOSE)
    
    def run(message):
        res = agent_executor.invoke({"user_message": message})
        return res["output"]

    ProtoPost({"": run}).start(PORT)

def autonomous_runner(model, tools, system_prompt):
    prompt = make_prompt(system_prompt, False, False)
    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=MAX_ITERATIONS, verbose=VERBOSE)

    while True:
        t = time.time()
        agent_executor.invoke({})
        dt = time.time() - t
        if not LOOP:
            return
        
        time.sleep(DELAY + dt * NICENESS)


def main():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    OLLAMA_MODEL = config["ollama"]["model"]
    OLLAMA_HOST = config["ollama"]["api_url"]
    SYSTEM_PROMPT = config.get("system_prompt")
    os.environ["OLLAMA_HOST"] = OLLAMA_HOST

    model = ChatOllama(model=OLLAMA_MODEL)
    tools = [toolify(route) for route in config["tools"]]

    if MODE == "service":
        service_runner(model, tools, SYSTEM_PROMPT)
    elif MODE == "autonomous":
        autonomous_runner(model, tools, SYSTEM_PROMPT)
    else:
        interactive_runner(model, tools, SYSTEM_PROMPT, MESSAGE)

if __name__ == "__main__":
    main()