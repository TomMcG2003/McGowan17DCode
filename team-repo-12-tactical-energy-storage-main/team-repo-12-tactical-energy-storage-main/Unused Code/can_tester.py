import can

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

except:
    print("could not open a bus")

canID = 0x18EF00F9
# VE.Can VREG Request has a PGN of 0xEF00
# VE.Can proprietary requests are 0x18XXXXXX
# F9 is the address for Victron devices

data = [0xED, 0x8A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

msg = can.Message(
    arbitration_id=canID,
    data=data,
    is_extended_id=True
)

try:
    bus.send(msg)
    print("message was sent")
except can.CanError:
    print("Better luck next time")

response = bus.recv()

if response:
    soc_value = response.data[1]
    print(f"State of Charge: {soc_value}")
else:
    print("No response, looser")