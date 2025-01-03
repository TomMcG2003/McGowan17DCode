import socket


def decode_can_frame(data):
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


def receive_rvc_packets(sock):
    """Receive RV-C packets from the Cerbo GX."""
    data = None
    try:
        # sock.listen(1)  # This is the issue
        while True:
            # Receive data in chunks of 4096 bytes
            try:
                data = sock.recv(4096)
            except Exception as err:
                print(f"{err}")
            print(data)
            # decoded_data = None
            if not data:
                pass
            else:
                decoded_data = decode_can_frame(data)

            # Print raw data (hexadecimal format)
            # print(f"Received raw data: {data.hex()}")

            # Decode the received data as RV-C (if necessary)
            # decode_can_frame(data)

    except Exception as err:
        print(f"Error receiving data: {err}")


def send_rvc_packet(sock, message):
    """Send an RV-C packet to the Cerbo GX."""
    try:
        # Send the packet using the socket
        sock.send(message)
        print(f"Sent message: {message.hex()}")

    except Exception as err:
        print(f"Error sending data: {err}")


def connectSocket(my_socket, socketIP, socketPort):
    my_socket.connect((socketIP, socketPort))


if __name__ == "__main__":
    # The IP and Port of the Cerbo GX
    cerbo_gx_ip = "169.254.13.55"  # Replace with the actual Cerbo GX IP
    cerbo_gx_port = 51906  # 81  # Either this or 34461
    # ports = [51883, 51884, 51896, 51898, 51899, 51900, 51901, 51902, 51906]
    try:
        # Create a TCP socket
        big_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {cerbo_gx_ip}:{cerbo_gx_port}")
        try:
            big_sock.connect((cerbo_gx_ip, cerbo_gx_port))
        except Exception as e:
            pass

        print("Connected to Cerbo GX. Listening and ready to send RV-C packets...")

        # Example: Create a sample CAN-like RV-C packet to send
        # sample_rvc_packet = bytes.fromhex('1234567812345678')  # Replace with actual RV-C message

        # Send a packet to the Cerbo GX
        # send_rvc_packet(big_sock, sample_rvc_packet)

        # Receive and print RV-C packets from Cerbo GX
        receive_rvc_packets(big_sock)
        print("Done listening")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Closing connection")
        big_sock.close()
