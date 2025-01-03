import asyncio
import math
import sys
import csv
import XMLTranslator as xml
from pymodbus.client import AsyncModbusTcpClient
import time  # For testing/timing purposes
import numpy as np
import pymodbus.client as ModbusClient
from pymodbus import (
    FramerType,
    ModbusException
    # ExceptionResponse,
    # pymodbus_apply_logging_config
)
import time
import datetime
import tracemalloc
import EnumClasses as eC
import StructClasses as sC
import rticonnextdds_connector as rti
from BatteryCalls import Battery

# import XMLTranslator as xmlt
# -----

ppath = r"C:\Users\thomas.mcgowan\XE4012\team-repo-12-tactical-energy-storage\Capstone\xml\tmg_xml_24_mar.xml"
"""
The 5 curves below are test curves. These can be used to test functions for TMS messages that 
"""

# -----
tracemalloc.start()
MAXCHARGE = 5  # Units are KWH
SYSTEMSLAVE = 100
BATTERYSLAVE = 225
VEBUSSLAVE = 227
cerbo_IP = "192.168.50.16"
cerbo_port = 502
tempCurve = {
    "points": [
        {"x": 1.0, "y": 2.0},
        {"x": 3.5, "y": 4.5},
        {"x": 5.0, "y": 6.0},
        # Add more points as needed, up to 21
    ]
}

tempCurvechargeTime = {
    'chargeTime': {
        "points": [
            {"x": 1.0, "y": 2.0},
            {"x": 3.5, "y": 4.5},
            {"x": 5.0, "y": 6.0},
            # Add more points as needed, up to 21
        ]
    }
}

tempCurvedischargeTime = {
    'dischargeTime': {
        "points": [
            {"x": 1.0, "y": 2.0},
            {"x": 3.5, "y": 4.5},
            {"x": 5.0, "y": 6.0},
            # Add more points as needed, up to 21
        ]
    }
}

tempCurvemaxChargeTime = {
    'maxChargeTime': {
        "points": [
            {"x": 1.0, "y": 2.0},
            {"x": 3.5, "y": 4.5},
            {"x": 5.0, "y": 6.0},
            # Add more points as needed, up to 21
        ]
    }
}

tempCurvemaxDischargeTime = {
    'maxDischargeTime': {
        "points": [
            {"x": 1.0, "y": 2.0},
            {"x": 3.5, "y": 4.5},
            {"x": 5.0, "y": 6.0},
            # Add more points as needed, up to 21
        ]
    }
}


class TMSReply:
    def __init__(self, deviceID: str, targetDeviceID: str, config: eC.ConfigID, portNumber: tuple,
                 requestSequenceID: int,
                 status: eC.ReplyStatus):
        self.self = self
        self.deviceID = deviceID
        self.targetDeviceID = targetDeviceID
        self.config = config
        self.portNumber = portNumber
        self.requestSequenceID = requestSequenceID
        self.status = status

    def reply_as_dict(self):
        return {
            "deviceID": self.deviceID,
            "targetDeviceID": self.targetDeviceID,
            "config": self.config,
            "portNumber": self.portNumber,
            "requestSequenceID": self.requestSequenceID,
            "status": self.status
        }

    def reply_as_list(self):
        return [self.deviceID, self.targetDeviceID, self.config, self.portNumber, self.requestSequenceID, self.status]

    def reply_as_string(self):
        return str(self.reply_as_dict())


# ----
class Demonstration:
    def __init__(self):
        self.self = self
        self.bigValues = []

    def generateKey(self, line):
        keys = {}
        counter = 0
        for thing in line:
            keys[thing] = counter
            counter += 1
        return keys

    async def test_storage_update(self):
        path = "TEST_storage_update_data.csv"
        curCount = 0
        with open(path, 'r') as f:
            file = csv.reader(f)
            for line in file:
                register_values = {}
                if curCount == 0:
                    keys = self.generateKey(line)
                    curCount += 1
                else:
                    curCount += 1
                    register_values["deviceId"] = line[0]
                    register_values["internalVoltage"] = float(line[1])
                    register_values["soc"] = float(line[2])
                    register_values["availableEnergy"] = float(line[3])
                    register_values["holdTime"] = float(line[4])
                    register_values["chargeTime"] = tempCurvechargeTime
                    register_values["dischargeTime"] = tempCurvedischargeTime
                    register_values["maxChargeTime"] = tempCurvemaxChargeTime
                    register_values["maxDischargeTime"] = tempCurvemaxDischargeTime
                    register_values["maxChargeRate"] = float(line[9])
                    register_values["maxDischargeRate"] = float(line[10])
                    self.bigValues.append(register_values)
        f.close()
        return self.bigValues

    async def test_heartbeat(self, heartbeatID):
        return {"deviceId": "cadet-battery", "heartbeat": heartbeatID}

    async def heartbeatdemo(self):
        """
        To make this work, we need to ensure that we can connect to the router and that the router can talk to the battery
        One thing we can do is upload this to GitHub, pull it onto the Raspberry Pi, SSH into the Raspberry Pi, and share
        the Raspberry Pi's SSH interface on the screen via our laptop.
        :return: None
        """
        with rti.open_connector(
                config_name="TmsParticipantLibrary::TmsParticipant",
                url=ppath) as device:
            for i in range(0, sys.maxsize):
                hb = await self.test_heartbeat(i)
                await xml.heartBeat(device, hb)
                time.sleep(1)

    async def demoStorageUpdate(self):
        """
        This function will open a RTI TMS Participant connection. This connection gets passed to the translator. The
        translator handles the creation of the storage update messages, forms them, and writes it to the RTI network.
        """
        with rti.open_connector(
                config_name="TmsParticipantLibrary::TmsParticipant",
                url=ppath) as device:
            await xml.testStorageUpdate(connection=device)

    async def heartbeatDemo(self, connection):
        for i in range(0, sys.maxsize):
            # hb = await test_heartbeat(i)
            await xml.testHeartbeat(connection, {'deviceId': "cadet-battery", 'heartbeat': i})
            # time.sleep(1)

    async def sprintThreeReview(self):
        user = Battery(IP=cerbo_IP, port=cerbo_port)
        await user.create_client()
        with rti.open_connector(
                config_name="TmsParticipantLibrary::TmsParticipant",
                url=ppath) as device:
            for i in range(0, sys.maxsize):
                hb = await user.heartbeat()
                sud = await user.storage_update()
                await xml.heartBeat(device, hb)
                await xml.publishDevicecUpdate(device=device, dictionary=sud)
                await xml.testDeviceInfo(device)

                time.sleep(1)

    async def offlineSprintThreeReview(self):
        with rti.open_connector(
                config_name="TmsParticipantLibrary::TmsParticipant",
                url=ppath) as device:
            for i in range(0, sys.maxsize):
                await xml.testHeartbeat(device, {'deviceId': "cadet-battery", 'heartbeat': i})
                await xml.testStorageUpdateOnce(connection=device)
                await xml.testDeviceInfo(device)
                time.sleep(1)

    async def testingDeviceInfoWriter(self):
        with rti.open_connector(
                config_name="TmsParticipantLibrary::TmsParticipant",
                url=ppath) as device:
            for i in range(0, sys.maxsize):
                await xml.testDeviceInfo(device)
                time.sleep(1)


async def storageUpdate():
    """
    This function opens an RTI Participant Connection and creates a connection to the battery.
    We create a client and then we generate a heartbeat every second. We take this heartbeat
    which is a dictionary and then pass it to the translator. The translator will then package
    this dictionary into a TMS message and write the message onto the RTI network. It will then
    sleep for one second.
    """
    with rti.open_connector(
            config_name="TmsParticipantLibrary::TmsParticipant",
            url=ppath) as device:
        user = Battery(IP=cerbo_IP, port=cerbo_port)
        await user.create_client()
        print(f"Battery device ID: {user.deviceID}")
        for i in range(0, sys.maxsize):
            update = await user.storage_update()
            await xml.publishDevicecUpdate(update, device)
            time.sleep(1)

asyncio.run(storageUpdate())

async def heartbeat():
    user = Battery(IP=cerbo_IP, port=cerbo_port)
    await user.create_client()
    with rti.open_connector(
            config_name="TmsParticipantLibrary::TmsParticipant",
            url=ppath) as device:
        for i in range(0, sys.maxsize):
            hb = await user.heartbeat()
            await xml.heartBeat(device, hb)


async def productInfoTest():
    user = Battery(IP=cerbo_IP, port=cerbo_port)
    await user.create_client()
    with rti.open_connector(
            config_name="TmsParticipantLibrary::TmsParticipant",
            url=ppath) as device:
        thing = await user.deviceInfo()
        await xml.publishDeviceInfo(device, thing)
        print(thing)


async def pullRegisters(reg, slaveType):
    user = Battery(IP=cerbo_IP, port=cerbo_port)
    await user.create_client()
    await user.testRegister(reg, slaveType)
