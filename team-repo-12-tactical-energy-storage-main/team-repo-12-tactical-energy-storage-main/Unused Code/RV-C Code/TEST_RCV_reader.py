import can
from can import message as m

testMessage = can.Message(data=[1])
m1 = m.Message(data=[0x64, 0x65, 0x61, 0x64, 0x62, 0x65, 0x65, 0x66, 0x21])
# What these two lines show is that we can generate simple messages using bytecode
print(testMessage.data)
print(m1.data)
# These print out the data we have
testString = "Hello, world!"
testEncoding = testString.encode("utf-8")
m2 = m.Message(data=testEncoding)
# These lines show that we can encode a normal string and put it into a message
print(m2.data.decode("utf-8"))
print(m2.data)
# This is us decoding the message to show that it keeps the data
print("===================================")
# Here we are trying to open a bus and print out the messages that we receive
with can.Bus(interface="socketcan") as bus:
#with can.Bus() as bus:
    try:
        while True:
            message = bus.recv()
            if message is not None:
                print(f"Message received: {message}")
                print(f"ID: {message.arbitration_id}, Date: {message.data}")
    except KeyboardInterrupt:
        print("Quiting...")
    finally:
        bus.shutdown()

    # for msg in bus:
    #    print(msg.data)
