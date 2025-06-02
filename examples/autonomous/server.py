from protopost import ProtoPost

def send_update(weather):
    print(weather)
    return "Update sent successfully"

routes = {
    "get_precip": lambda city: "currently 30%",
    "get_temp": lambda city: "60 degrees F",
    "send_update": send_update
}

ProtoPost(routes).start(8125)
