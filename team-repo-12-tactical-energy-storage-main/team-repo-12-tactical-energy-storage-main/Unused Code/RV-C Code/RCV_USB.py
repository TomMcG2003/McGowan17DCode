import can

with can.Bus(interface= 'pcan') as bus:  # is channel and bitrate required?
    try:
        while True:
            message = bus.recv()
            if message is not None:
                print(f"message: {message}")
                print(f"ID: {message.arbitration_id}, Data: {message.data}")
    except KeyboardInterrupt:
        print("Quiting...")
    finally:
        bus.shutdown()

"""def receive_can_messages(bitrate=250000):
    # Set up the CAN interface for a USB-based PCAN device
    bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=bitrate)

    print("Listening for CAN messages over USB...")

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


if __name__ == "__main__":
    receive_can_messages()
"""