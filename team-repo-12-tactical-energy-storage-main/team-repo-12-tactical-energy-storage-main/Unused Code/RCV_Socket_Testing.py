import socket
import os  # This might be replaced with the <logging> module
from threading import Timer
import logging as log


def decode_can_frame(data):
    """
    !!! This might be replaced with functions inside of the Message class !!!
    TODO: Ensure that this function actually works to decode the byte data
    :param data: The data pulled in from the TCP packet
    :return: Message ID, Data Length Code (DLC), and data Payload
    """

    # Yell if the data is incomplete
    if len(data) < 8:
        print("Incomplete frame")
        return

    # Assume first 4 bytes are the identifier (Message ID)
    message_id = int.from_bytes(data[:4], byteorder='big')

    # Next byte is the Data Length Code (DLC)
    dlc = data[4]

    # Following bytes are the actual data payload
    payload = data[5:5 + dlc]

    print(f"Message ID: {message_id}, DLC: {dlc}, Payload: {payload.hex()}")
    return message_id, dlc, payload


class Logger:
    def __init__(self, logger_code, logger_type, message):
        self.self = self
        self.logger_code = int(logger_code)
        self.logger_type = logger_type
        self.message = message

    def write_to_log(self):
        # TODO: Write the procedure that generates and writes the log to the correct logging level
        pass


class Message:
    def __init__(self, tcp_socket):
        self.self = self
        self.socket = tcp_socket
        self.data = None

    def encode_data(self):
        """
        This will take the data that the user gives and encode it to be sent over the socket
        :return: bytearray
        """
        # TODO: Write a procedure to encode the data
        # pass
        return bytearray("Hello world")  # This will have to change

    def decode_data(self):
        """
        This will decode the data.
        Primary use cases will be for debugging
        :return: utf-8 text
        """
        # TODO: Write a procedure to decode the data
        pass

    def create_message(self, data):
        # TODO: Find a procedure for creating message
        self.data = data
        self.data = self.encode_data()
        pass

    def send_message(self):
        # TODO: Add logging for error
        if self.data is None:
            print(f"Error, cannot send empty message")
        else:  # Message is not empty
            self.socket.send(self.data)

    def dump_message_data(self):
        if self.data is None:
            print(f"You have an empty message")
        return self.data

    def dump_decoded_message_data(self):
        if self.data is None:
            print(f"You have an empty message")
        return self.decode_data(self.data)


class Socket:

    def __init__(self, deviceIP, devicePort):
        self.self = self
        self.deviceIP = deviceIP  # IP of the Cerbo GX
        self.devicePort = devicePort  # Port number of the Cerbo GX
        self.decoded_data = {}  # Will hold decoded data, {key: data} ==
        self.message = None  # This will be filled my the user and this is the message that will be sent
        '''
        Here we are trying to open a socket with the given battery BMS controller. 
        If the connection is successful, then we save the socket as a class variable and connect to it.
        If the connection is not successful, then we collect the error message
        '''
        # TODO: Add logging for every socket connection
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.my_socket = my_socket
            my_socket.connect(self.deviceIP, self.devicePort)
            print("Socket created")
        # TODO: Add error logging for a failed socket connection
        except Exception as e:
            print(f"{e}: Error in making socket and connection")

    def timeout_exit(self):
        """
        This function will close the TCP socket and exit the program.
        :return: None
        """
        try:
            print(f"Closing the socket, socket {self.my_socket}")
            self.my_socket.close()
            exit(10)
            # TODO: Add logging for the timeout and closing of the socket

        # TODO: Add error logging
        except Exception as e:
            print(f"Failed to close socket {self.my_socket} after timeout: {e}")

    def get_messages(self):
        """
        TODO: Ensure that this method can actually capture the packets from the BMS
        :return: None
        """
        try:
            #  TODO: Add logging for message receipt
            while True:
                # Receive data in chunks of 1024 bytes
                data = self.socket.recv(1024)

                if not data:
                    pass

                else:
                    data = decode_can_frame(data)
                    message_id, dlc, payload = data
                    self.decoded_data[id] = [dlc, payload]

                # Print raw data (hexadecimal format)
                print(f"Received raw data: {data.hex()}")

                # Decode the received data as RV-C (if necessary)
                # decode_can_frame(data)
        # TODO: Add logging for error with reception of packet.
        # IDK what the errors we would get from this.
        except Exception as err:
            print(f"Error receiving data: {err}")

    def listener(self, timeout=False, timeout_duration=32000000):
        """
        This function will listen for any incoming packets coming into the TCP socket.
        :param timeout: Boolean. Default to false to listen indefinitely. True would have a timeout of one year by
                        default. Can change manually.
        :param timeout_duration: Int. Default to approx. one year. Can be changed manually.
        :return: None
        """
        if timeout:
            t = Timer(int(timeout_duration), self.timeout_exit)  #
            t.start()
            try:
                self.get_messages()
            # TODO: Add logging for this error
            except Exception as e:
                print(f"Here is your error... sorry for the lackluster message: {e}")

        try:
            while True:
                self.get_messages()
        # TODO: Add logging for this error
        except Exception as e:
            print(f"Here is your error... sorry for the lackluster message: {e}")

    def sendMessage(self, message):
        try:
            self.message = message
        # TODO: Add logging for this error
        except Exception as e:
            print(f"There was an error setting your socket's message.\nSocket: {self.my_socket}\nError: {e}")
        try:
            # Send the packet using the socket
            self.message.send_message()
            print(f"Sent message: {message.hex()}")
        # TODO: Add logging for this error
        except Exception as err:
            print(f"Error sending data: {err}")
