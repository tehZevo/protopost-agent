import json

from langchain.agents import tool
from protopost import protopost_client as ppcl

def toolify(data):
  #TODO: puts example usage in the description rather than making a json schema
  desc = data["description"]
  desc += "\nExample usage:" + data["usage"]

  print("making func with", data)
  def func(json_string: str):
    try:
      parsed = json.loads(json_string)
      print("data was json string lol")
    except json.JSONDecodeError:
      parsed = json_string

    #TODO: parse json
    return ppcl(data["route"], parsed)
  
  func.__doc__ = desc
  func.__name__ = data["name"]
  
  return tool()(func)