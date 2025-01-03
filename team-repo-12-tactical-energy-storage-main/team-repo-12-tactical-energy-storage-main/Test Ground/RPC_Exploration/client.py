from rpc import RPCClient

client = RPCClient('127.0.0.1', 8080)
client.connect()

print(client.add(5, 6))
print(client.sub(5, 6))
print(client.mult(5, 6))
print(client.echo("LIGMA"))
client.disconnect()
