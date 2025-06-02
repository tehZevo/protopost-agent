import json

from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate
from protopost import protopost_client as ppcl

def toolify(data):
  #TODO: puts example usage in the description rather than making a json schema
  desc = data["description"]
  desc += "\nExample usage:" + data["usage"]

  def func(json_string: str):
    #handle cases where llm passes us "double encoded" json
    try:
      parsed = json.loads(json_string)
    except json.JSONDecodeError:
      parsed = json_string

    return ppcl(data["route"], parsed)
  
  func.__doc__ = desc
  func.__name__ = data["name"]
  
  return tool()(func)

def make_prompt(system_prompt, has_user_message, has_chat_history):
    messages = []
    if system_prompt is not None:
        messages.append(("system", system_prompt))
    if has_user_message:
        messages.append(("user", "{user_message}"))
    if has_chat_history:
        messages.append(MessagesPlaceholder("chat_history", optional=True))
    messages.append(("placeholder", "{agent_scratchpad}"))
    
    prompt = ChatPromptTemplate.from_messages(messages)

    return prompt