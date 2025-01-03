import can

'''
with can.Bus(interface="socketcan") as bus:  # Is the channel, bustype, bitrate required?
    try:
        while True:
            message = bus.recv()
            if message is not None:
                print(f"Message: {message}")
                print(f"ID: {message.arbitration_id}, Data: {message.data}")
    except KeyboardInterrupt:
        print("Quiting...")

    finally:
        bus.shutdown()
'''
IP = "169.254.13.55"


def receive_can_messages(ip_address=IP, port=81, bitrate=250000):
    # Set up the CAN interface using the IP address and port for Ethernet
    #bus = can.interface.Bus(interface='socketcan', channel=f"{ip_address}:{port}")
    #bus = can.interface.Bus(bustype='socketcan', channel=f"{ip_address}:{port}", bitrate=bitrate)
    bus = can.interface.Bus(bustype='kvaser', channel=0, bitrate=bitrate)
    #bus = can.interface.Bus(interface='kvaser', channel=0, bitrate=bitrate)

    '''print("Listening for CAN messages over Ethernet...")

    try:
        while True:
            message = bus.recv()  # Receive a message
            if message is not None:
                print(f"Message received: {message}")
                print(f"ID: {hex(message.arbitration_id)}, Data: {message.data}")

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        bus.shutdown()
    '''


if __name__ == "__main__":
    receive_can_messages()
