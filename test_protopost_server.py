from protopost import ProtoPost

def fail(data):
    raise ValueError("test failed successfully")


routes = {
    "get_precip": lambda city: "currently 30%",
    "get_temp": lambda city: "60 degrees F",
    "add": lambda data: data["a"] + data["b"],
    "fail": fail,
}

ProtoPost(routes).start(8125)
