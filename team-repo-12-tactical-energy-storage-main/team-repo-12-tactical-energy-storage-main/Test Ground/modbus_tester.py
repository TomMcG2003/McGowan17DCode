import asyncio
import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)

SYSTEMSLAVE = 100


async def run_async_simple_client(comm, IP, port, framer=FramerType.SOCKET):
    """Run async client."""
    # activate debugging
    pymodbus_apply_logging_config("DEBUG")

    print("get client")
    client = ModbusClient.AsyncModbusTcpClient(
        host=IP,
        port=port,
        # framer=framer,
        # timeout=10,
        # retries=3,
        # source_address=("localhost", 0),
    )

    print("connecting to server")
    await client.connect()
    # test client is connected
    assert client.connected
    print("Connected to the server")
    print("get and verify data")
    try:
        # See all calls in client_calls.py
        # rr = await client.read_coils(1, 1, slave=100)  # Changed slave ID from 1 to 100
        rr = await client.read_holding_registers(address=843, count=1, slave=100, no_response_expected=False)
        registers = rr.registers
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
        return
    print(f"Here is the output: {rr}")
    print(f"Here are the registers: {registers}")
    print("close connection")
    client.close()


async def test_function(IP, port, framer=FramerType.SOCKET):
    register_data = {}
    client = ModbusClient.AsyncModbusTcpClient(
        host=IP,
        port=port,
        framer=framer,
        # timeout=10,
        # retries=3,
        # source_address=("localhost", 0),
    )
    await client.connect()
    # test client is connected
    assert client.connected
    try:
        # See all calls in client_calls.py
        for i in range(840, 847):
            rr = await client.read_holding_registers(address=i, count=1, slave=100)
            register_data[i] = rr.registers[0]
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
        return
    print(f"Here is the output: {rr}")
    print(f"Here are the registers: {register_data}")
    print("close connection")
    client.close()


async def test_one_register(IP, port, register, slave=100, framer=FramerType.SOCKET):
    register_data = {}
    # print("get client")
    client = ModbusClient.AsyncModbusTcpClient(
        host=IP,
        port=port,
        framer=framer,
        # timeout=10,
        # retries=3,
        # source_address=("localhost", 0),
    )
    await client.connect()
    # test client is connected
    assert client.connected
    try:
        # See all calls in client_calls.py
        rr = await client.read_holding_registers(address=register, count=1, slave=slave)
        print(rr)
        # register_data[register] = rr.registers[0]
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
        return

    print(f"Here is the output: {rr}")
    print(f"Here are the registers: {register_data}")
    print("close connection")
    client.close()


async def test_read_coils(IP, port, register, framer=FramerType.SOCKET):
    register_data = {}
    client = ModbusClient.AsyncModbusTcpClient(
        host=IP,
        port=port,
        framer=framer,
        # timeout=10,
        # retries=3,
        # source_address=("localhost", 0),
    )
    await client.connect()
    # test client is connected
    assert client.connected

    try:
        # See all calls in client_calls.py
        rr = await client.read_coils(address=register, count=1, slave=100)
        # register_data[register] = rr.registers[0]
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
        return
    print(f"Here is the output: {rr}")
    print(f"Here are the registers: {register_data}")
    print("close connection")
    client.close()


async def what_registers_can_we_read_from(IP, port, framer=FramerType.SOCKET):
    registers = []
    client = ModbusClient.AsyncModbusTcpClient(
        host=IP,
        port=port,
        framer=framer,
        # timeout=10,
        # retries=3,
        # source_address=("localhost", 0),
    )
    await client.connect()
    # test client is connected
    assert client.connected
    with open("readable_registers.txt", "w") as f:
        for i in range(0, 4924):
            try:
                rr = await client.read_holding_registers(address=i, count=1, slave=100)
                if not isinstance(rr, ExceptionResponse):
                    registers.append(i)
                    f.write(f"{i}\n")
            except Exception as e:
                pass
    f.close()
    print(registers)
    client.close()


async def test_write_to_2710(IP, port, framer=FramerType.SOCKET):
    client = ModbusClient.AsyncModbusTcpClient(
        host=IP,
        port=port,
        framer=framer,
        # timeout=10,
        # retries=3,
        # source_address=("localhost", 0),
    )
    await client.connect()
    # test client is connected
    assert client.connected
    try:
        rr = await client.write_register(address=2710, value=28, slave=100)
    except ModbusException as e:
        print(f"ERROR! {e}")
        return
    print(rr)
    client.close()


async def storage_update(IP, port, slaveID, framer=FramerType.SOCKET):
    client = ModbusClient.AsyncModbusTcpClient(
        host=IP,
        port=port,
        framer=framer,
        # timeout=10,
        # retries=3,
        # source_address=("localhost", 0),
    )
    await client.connect()
    assert client.connected
    register_values = {
        "deviceID": [slaveID, SYSTEMSLAVE]
    }

    try:

        register_values["deviceID"] = [slaveID, SYSTEMSLAVE]
        internalVoltage = await client.read_holding_registers(address=840, count=1, slave=SYSTEMSLAVE)
        stateOfCharge = await client.read_holding_registers(address=843, count=1, slave=SYSTEMSLAVE)
        availableEnergy = await client.read_holding_registers(address=309, count=1, slave=slaveID)
        # holdTime = ??? --> float32
        # chargeTime = ??? --> Curve2D
        # dischargeTime = ??? --> Curve2D
        # maxChargeTime = ??? --> Curve2D
        # maxDischargeTime = ??? --> Curve2D
        # maxChargeRate = ??? --> float32
        # maxDischargeRate = ??? --> float32

        register_values["internalVoltage"] = internalVoltage.registers[0] / 10
        register_values["stateOfCharge"] = stateOfCharge.registers[0] / 100
        register_values["availableEnergy"] = availableEnergy.registers[0]
        # register_values["holdTime"] = holdTime.registers[0]
        # register_values["chargeTime"] = ???
        # register_values["dischargeTime"] = ???
        # register_values["maxChargeTime"] = ???
        # register_values["maxDischargeTime"] = ???
        # register_values["maxChargeRate"] = maxChargeRate.registers[0]
        # register_values["maxDischargeRate"] = maxDischargeRate.registers[0]

    except Exception as e:
        print(f"Error! {e}")
    print(register_values)
    client.close()


# 840
if __name__ == "__main__":
    cerbo_IP = "192.168.50.16"
    cerbo_port = 502
    # asyncio.run(run_async_simple_client("tcp", "192.168.50.16", 502), debug=True)  # Changed the port from 81 to 502
    # asyncio.run(test_function(cerbo_IP, cerbo_port))
    asyncio.run(test_one_register(cerbo_IP, cerbo_port, 3127, slave=100))
    # asyncio.run(test_read_coils(cerbo_IP, cerbo_port, 806))
    # asyncio.run(what_registers_can_we_read_from(cerbo_IP, cerbo_port))
    # asyncio.run(test_write_to_2710(cerbo_IP, cerbo_port))
    # asyncio.run(storage_update(cerbo_IP, cerbo_port, slaveID=1))
