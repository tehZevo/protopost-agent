from protopost import ProtoPost

routes = {
    "get_precip": lambda city: "currently 30%",
    "get_temp": lambda city: "60 degrees F"
}

ProtoPost(routes).start(8125)
