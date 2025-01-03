import json
import socket
import inspect
from threading import Thread

global SIZE
SIZE = 1024


class RPCServer:
    def __init__(self, host="0.0.0.0", port=8080):
        self.host = host
        self.port = port
        self.address = (host, port)
        self._methods = {}

    def registerMethod(self, function):
        try:
            self._methods.update({function.__name__: function})
            # Here the dictionary key is the name of the function and the value is the function object.
        except:
            raise Exception("Nope")

    def registerInstance(self, instance=None) -> None:
        try:
            # Registering the instance's methods
            for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
                if not functionName.startswith('__'):
                    self._methods.update({functionName: function})
        except:
            raise Exception('A non class object has been passed into RPCServer.registerInstance(self, instance)')

    def __handle__(self, client, address):
        while True:
            try:
                functionName, args, kwargs = json.loads(client.recv(SIZE).decode())
            except:
                print(f"! client {address} disconnected")
                break

            try:
                response = self._methods[functionName](*args, **kwargs)
            except Exception as e:
                client.sendall(json.dumps(str(e)).encode())
            else:
                client.sendall(json.dumps(response).encode())
        print(f"Completed requests from address {address}")
        client.close()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()
            print(f"+server {self.address} running")
            while True:
                try:
                    client, address = sock.accept()
                    Thread(target=self.__handle__, args=[client, address]).start()
                except KeyboardInterrupt:
                    print(f"- Server {self.address} interrupted")
                    break


class RPCClient:
    def __init__(self, host: str = 'localhost', port: int = 8080) -> None:
        self.__sock = None
        self.__address = (host, port)

    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect(self.__address)
        except EOFError as e:
            print(e)
            raise Exception("Couldn't connect")

    def disconnect(self):
        try:
            self.__sock.close()
        except:
            pass

    def __getattr__(self, __name):
        def execute(*args, **kwargs):
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())
            response = json.loads(self.__sock.recv(SIZE).decode())

            return response

        return execute
