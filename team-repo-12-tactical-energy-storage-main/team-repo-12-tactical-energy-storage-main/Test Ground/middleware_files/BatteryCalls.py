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

# import XMLTranslator as xmlt
# -----

ppath = r"C:\Users\thomas.mcgowan\XE4012\team-repo-12-tactical-energy-storage\Capstone\xml\tmg_xml_24_mar.xml"

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


class Battery:
    def __init__(self, IP: str = None, port: int = None, deviceName: str = 'cadet-battery'):
        """
        Here we initialize the important data that we will need for basic operations such as heartbeat.
        We define the device's ID as an integer representation of the device's MAC address
        We define the framer as a socket.
        :param IP: string, represents the Cerbo GX's IP address
        :param port: int, represents the Cerbo GX's port number
        """
        self.self = self
        if IP is not None:
            self.IP = IP
        else:
            self.IP = cerbo_IP
        if port is not None:
            self.port = port
        else:
            self.port = cerbo_port
        self.framer = FramerType.SOCKET
        self.client = ModbusClient.AsyncModbusTcpClient(
            host=self.IP,
            port=self.port,
            framer=self.framer
        )
        # I feel that for the heartbeat, as long as we can connect to it, we should be fine
        self.heartbeatID = 0
        self.deviceID = deviceName
        self.deviceInfo = {
            'deviceId': self.deviceID,
            'role': None,
            'controlHardware': None,
            'powerHardware': None,
            'controlParameters': None,
            'metricParameters': None,
            'controlService': None,
            'powerDevice': None
        }

    async def create_client(self) -> None:
        """
        In this function, we are creating the user's client object and setting it to the class' client field
        :return: None
        """
        await self.client.connect()
        assert self.client.connected
        if self.deviceID is None:
            try:
                mac = await self.client.read_holding_registers(800, 1, 100)
                self.deviceID = mac.registers[0]

            except Exception as e:
                print(f"Could not get device ID: {e}")

        self.client.close()

    '''
    async def get_starter_info(self):
        """
        This function will
        :return: None
        """
        await self.client.connect()
        assert self.client.connected
        try:
            mac = await self.client.read_holding_registers(address=800, count=1, slave=100)
            self.deviceID = mac.registers[0]
        except Exception as e:
            print(f"Could not get device ID:\n{e}")

        self.client.close()

    async def make_tms_message(self, rdict: dict) -> None or str:
        """
        This function will take in a dictionary that was creataed by a client function and convert it into the required
        XML document that is needed for the microgrid controller to understand. This XML file will be sent onto the
        network and interpretted by the microgrid controller.
        :param rdict: dictionary. Holds all of the values and data that were translated from the battery's registers
        :return: None or string. Still waiting to figure it out.
        """
        # TODO: Ian, figure out the XML formatting that we need to make this work and either write the script or teach
        # me what I need to do to write it.
        pass
    '''

    async def make_product_info(self):
        """
        This function is essentially an enumeration of the product information that TMS required of all devices before
        they can publish themselves as TMS compliant.
        :return:
        """
        await self.client.connect()
        assert self.client.connected

        serialNumber = await self.client.read_holding_registers(address=800, count=1, slave=100)
        serialNumber = serialNumber.registers[0]
        print(f"Here is the serial number {serialNumber}")
        productInfo = {
            "nsn": '9999',  # Made up/Hard coded
            "gtin": '9999',  # Made up/Hard coded
            "manufacturerName": "Viridi",  # Made up/Hard coded
            "modelName": "Faveo",  # Made up/Hard coded
            "modelNumber": '312',  # Made up/Hard coded
            "serialNumber": str(serialNumber),
            "softwareVersion": '001'  # Made up/Hard coded
        }
        self.client.close()
        return productInfo

    # ----- TMS related functions -----

    async def storage_update(self) -> None:
        """
        This function will produce all of the values required of a TMS <storage_update> call and send the data to the
        publisher to put onto the network
        :return: None
        """
        # --- Ensuring that we are connected to the battery ---
        await self.client.connect()
        assert self.client.connected
        # --- Will fail if we are not connected to the battery
        register_values = {}
        # This is the dictionary that we will use to store all of the register values that we're going to need
        try:
            # register_values["deviceID"] = [self.deviceID, SYSTEMSLAVE, BATTERYSLAVE, VEBUSSLAVE]
            register_values['deviceID'] = 'cadet battery'
            try:
                internalVoltage = await self.client.read_holding_registers(address=840, count=1, slave=SYSTEMSLAVE)
                # Grabbing the internal voltage from register 840 which is a system register
            except:
                print("cannot read from that register for internal voltage")
            try:
                stateOfCharge = await self.client.read_holding_registers(address=843, count=1, slave=SYSTEMSLAVE)
                # Grabbing the state of charge from register 843 which is a system register
            except:
                print("cannot read from that register for state of charge")
            try:
                availableEnergy = await self.client.read_holding_registers(address=258, count=1, slave=BATTERYSLAVE)
                # Grabbing the available energy from register 258 which is a battery register
            except:
                print("cannot read from that register for available energy")
            # holdTime = float32
            try:
                holdTime = await self.client.read_holding_registers(address=846, count=1, slave=SYSTEMSLAVE)
                # Grabbing the hold time from register 846 which is a system register
            except:
                print("Cannot read from that register for hold time")
            # chargeTime --> Curve2D
            chargeTimeCurve = sC.Curve2D()  # We initialize our curve that we'll use for this function
            denominator = 0
            try:
                '''
                (5KWH*(r266)current charge in battery)
                '''
                # start_time = time.time()  # Used for testing run time
                numerator = 5 * stateOfCharge.registers[0]  # We store the state of charge * 5 KWH
                maxChargeVoltage = await self.client.read_holding_registers(address=305, count=1, slave=BATTERYSLAVE)
                maxChargeCurrent = await self.client.read_holding_registers(address=307, count=1, slave=BATTERYSLAVE)
                # Grabbing the max charge voltage and current from registers 305 and 307 which are battery registers
                denominator = maxChargeCurrent.registers[0] * maxChargeVoltage.registers[0] * 1000
                # The denominator for all of our calculations is the max charge voltage * current * 1000
                '''
                If we look at all integer possibilities within the denominator, then we are going to have a run time of
                about 10 minutes. By decreasing the domain by 2 order of magnitude, we can shrink this down to about 3 
                seconds.
                '''
                # print("Generating the charge time")
                lengthOfArray = 21  # This is the maximum number of elements we can store in the Curve2D
                # We have to bring the number down by 2 orders of magnitude to bring the run time down from 630 seconds
                # all the way down to 2 seconds
                indices = np.linspace(0.5, denominator, lengthOfArray)
                # This will calculate the load levels based on the indices.
                # For this we are starting at 0.5 and iterating for every 100th value.
                chargeTimes = (numerator / indices)  # This computes the charge times
                for i in range(0, lengthOfArray):  # This is what generates the Curve Points and adds them
                    point = sC.Point2D(x=float(indices[i]), y=float(chargeTimes[i]))
                    chargeTimeCurve.add_data(point)  # Curve2D.addData(point)
                # print(chargeTimeCurve)
            except Exception as e:
                print(f"Could not complete charge time :-(\n{e}")

                '''
                Discharge times are done in a similar fashion but with different register values
                ((Current energy in the battery which is r266* 5KWH))/ (Iteration from -0.5KW to the max discharge rate 
                of (r305*r307)*1000)
                '''
            dischargeTimeCurve = sC.Curve2D()
            try:
                # print("Generating the discharge time")
                indices = np.linspace(-0.5, denominator, lengthOfArray)
                dischargeTimes = (numerator / indices)  # This computes the charge times
                for i in range(0, lengthOfArray):  # This is what generates the Curve Points and adds them
                    point = sC.Point2D(x=float(indices[i]), y=float(dischargeTimes[i]))
                    dischargeTimeCurve.add_data(point)
                # print(dischargeTimeCurve)
            except:
                print("cannot complete discharge time")

            try:
                batteryTemperature = await self.client.read_holding_registers(address=61, count=1, slave=VEBUSSLAVE)
                maxChargeRate = None  # Something to do with temperature and state of charge
                maxDischargeRate = None  # Something to do with temperature and state of charge
            except Exception as e:
                print(f"Could not get max Charge/Discharge Rate(s)\n{e}")

                # maxChargeTime = ??? --> Curve2D
                # maxDischargeTime = ??? --> Curve2D

            self.client.close()
            try:
                # -------
                print(chargeTimeCurve)
                print("----")
                print(dischargeTimeCurve)
                print("----")
                print(tempCurvechargeTime)
                print("=====")
                print(tempCurvedischargeTime)
                print("!!!!")
                print(tempCurvechargeTime == chargeTimeCurve)
                register_values["deviceId"] = 'cadet-battery'
                register_values["internalVoltage"] = internalVoltage.registers[0] / 10
                register_values["stateOfCharge"] = stateOfCharge.registers[0] / 100
                register_values["availableEnergy"] = availableEnergy.registers[0]
                register_values["holdTime"] = holdTime.registers[0]
                register_values["chargeTime"] = {'chargeTime': chargeTimeCurve.to_dict()}
                register_values["dischargeTime"] = {'dischargeTime': dischargeTimeCurve.to_dict()}
                # register_values['chargeTime'] = tempCurvechargeTime
                # register_values['dischargeTime'] = tempCurvedischargeTime
                register_values["maxChargeTime"] = tempCurvemaxChargeTime
                register_values["maxDischargeTime"] = tempCurvemaxDischargeTime
                register_values["maxChargeRate"] = 1  # TODO: Change these (how to calc?)
                register_values["maxDischargeRate"] = -1  # TODO: Change these (how to calc?)

            except Exception as e:
                print(f"There was something wrong with putting the values in the dictionary\n{e}")

            try:
                # Here we are going to try and send the dictionary that we made to the TMS publisher
                "Call to the TMS reader"
                self.client.close()
                return register_values
                pass
            except:
                # We'll need to capture the errors we get.
                pass

        except ModbusException as exc:
            print(f"Received ModbusException ({exc}) from library")
            self.client.close()
        except Exception as exc:
            print(f"Received another error: {exc}")
            self.client.close()

        self.client.close()

    async def heartbeat(self):  # -> None:
        """
        This is to be published once every 1 second and upon request
        :return:
        """
        # TODO: Add conditions for ESS warnings/errors/alarms that can kill the connection/sever heartbeat
        await self.client.connect()
        assert self.client.connected
        try:
            self.heartbeatID += 1
            self.client.close()
            # await self.make_tms_message({"deviceID": self.deviceID, "heartbeat": self.heartbeatID})
            return {"deviceId": str(self.deviceID), "heartbeat": self.heartbeatID}
        except Exception as e:
            print(f"Unknown error occurred: {e}")
        finally:
            self.client.close()

    async def device_info(self) -> dict:
        """
        This function will gather all of the pertinent device information required from the TMS documentation. It will
        compile the information into a dictionary. This dictionary will
        :return: dict
        """
        await self.client.connect()
        assert self.client.connected
        print("Making product info")
        productInfo = await self.make_product_info()
        print("Made product info")
        self.deviceInfo = {
            "deviceID": str(self.deviceID),
            "role": {"DeviceRole": "ROLE_STORAGE"},
            "product": productInfo,  # This needs to be a dict
            "topics": sC.TopicInfo(
                "cadet_battery",
                sC.TopicList().addName("RTI Connext DDS")),
        }
        print(f"{self.deviceInfo = }")
        self.client.close()
        return self.deviceInfo

    # ----- Testing functions -----

    async def testRegister(self, register: int, slaveType):
        await self.client.connect()
        assert self.client.connected
        thing = await self.client.read_holding_registers(address=register, count=1, slave=slaveType)
        print(thing.registers[0])
        self.client.close()
        return thing.registers[0]

    async def printSomething(self):
        print("thing!")

