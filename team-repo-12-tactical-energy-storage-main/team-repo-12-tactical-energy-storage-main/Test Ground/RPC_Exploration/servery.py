from rpc import RPCServer


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def echo(string):
    return string


def mult(a, b):
    return a*b


server = RPCServer()
# We pass these functions in. They are passed in as function objects and not as strings. This is why we have to do
# certain comprehensions on the other end.
server.registerMethod(add)
server.registerMethod(sub)
server.registerMethod(mult)
server.registerMethod(echo)

server.run()
