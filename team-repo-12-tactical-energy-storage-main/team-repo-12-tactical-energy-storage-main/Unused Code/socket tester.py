import socket


# cerbo_gx_ip = "169.254.13.55"
# cerbo_gx_port = 51906


message_meanings = {"firmware version": [0x01, 0x02, False]}


def decode_can_frame(data):
    if len(data) < 4:
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


def receive_data_from_server(cerbo_gx_ip, cerbo_gx_port):
    # Create a TCP socket
    big_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # big_sock.settimeout(60)
    print(f"Connecting to {cerbo_gx_ip}:{cerbo_gx_port}")

    try:
        # Connect to the server (TCP connection)
        big_sock.connect((cerbo_gx_ip, cerbo_gx_port))
        print("Connected successfully!")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    while True:
        # Receive data in chunks of 4096 bytes
        try:
            print("grabbing data")
            data = big_sock.recv(4096)

        except Exception as err:
            print(f"Error receiving data: {err}")
            break

        # Check if the connection is closed by the server
        if not data:
            print("Connection closed by the server.")
            break

        print(f"Data received: {data.hex()}")  # Print the received data in hex format

        # Decode the CAN frame (if you have a decoding function)
        decoded_data = decode_can_frame(data) if data else None
        if decoded_data:
            print(f"Decoded data: {decoded_data}")

    # Close the socket once done
    big_sock.close()
    print("Socket closed.")


def generate_message(message_type):
    # [0x66, 0x99, regID.Low, regID.high, data, data, data, ...]
    message_meaning = message_meanings[message_type]
    if not message_meaning[2]:
        message = [0x00, 0x00, 0x00, 0x00]
    else:
        message = []
    message.append(message_meaning[1])
    message.append(message_meaning[0])
    message.append(0x99)
    message.append(0x66)
    message.reverse()
    print(message)
    return bytes(message)


def send_and_listen(ip, port):
    request_pgn_127506 = bytes([0x18, 0xEA, 0xFF, 0x00, 0x06, 0x00, 0xFA, 0x01])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"Connecting to {ip}:{port}")
        try:
            sock.connect((ip, port))
            print(f"We have connected to {ip}:{port}")
        except Exception as e:
            print(f"{e}")

        try:
            sock.sendall(request_pgn_127506)
        except Exception as e:
            print(f"Count not send data. {e}")

        try:
            response = sock.recv(4096)

            if response:
                print(f"We got a reply!")
                print(decode_can_frame(response))
                # print(decode_can_frame(response[4]))
                print(response)
                soc = response[4]
                print(f"The state of charge is {soc}")
            sock.close()

        except Exception as e:
            print(f"There was an error: {e}")


generate_message("firmware version")
# cerbo_gx_ip = "169.254.13.181"
cerbo_gx_ip = "169.254.1.45"
# cerbo_gx_ip = "169.254.1.55"
cerbo_gx_port = 139  # 23  # 139  # 51906
# receive_data_from_server(cerbo_gx_ip, cerbo_gx_port)
send_and_listen(cerbo_gx_ip, cerbo_gx_port)

