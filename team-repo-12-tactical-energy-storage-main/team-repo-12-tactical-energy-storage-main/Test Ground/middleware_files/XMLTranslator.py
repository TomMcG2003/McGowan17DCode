# See RTI python documentation for how to make sure
# the RTI provided python packages can be loaded
import rticonnextdds_connector as rti
import csv
import time
import asyncio

'''
file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")
print("Start " + repr(__file__))
config_path = os.path.join(file_path, "xml", "NewProject.xml")
print(f"Here is the file path: {config_path}")
'''
ppath = r"C:\Users\thomas.mcgowan\XE4012\team-repo-12-tactical-energy-storage\Capstone\xml\tmg_xml_24_mar.xml"


class Publisher:
    def __init__(self, connector):
        self.self = self
        self.connector = connector
        self.heartbeatWriter = self.connector.get_output("TmsPublisher::HeartbeatWriter")
        try:
            self.deviceUpdateWriter = self.connector.get_output("TmsPublisher::StorageUpdateWriter")
        except:
            print("squawk")
        try:
            self.deviceInfoWriter = self.connector.get_output("TmsPublisher::DeviceInfoWriter")
        except:
            print("Sqeak")

    async def publishHeartbeat(self, value_dictionary: dict) -> None:
        """
        This function will take a device ID and a sequence number and publish it as a heartbeat
        :param value_dictionary:
        :return: None
        """
        ef = 0
        if self.heartbeatWriter is not None:  # Here we make sure that the writer object was initialized
            try:
                # We are going to set the value of the deviceId in the 'deviceId' tag of the XML document
                self.heartbeatWriter.instance.set_string("deviceId", value_dictionary["deviceId"])
            except:
                # We catch the error and save it in the flag counter for later error printing
                ef += 1
            try:
                # We are going to set the sequence number as the heartbeat
                self.heartbeatWriter.instance.set_number('sequenceNumber', value_dictionary['heartbeat'])
            except KeyError as e:
                # Here we save the error for later
                ef += 2
            if ef == 0:  # If we have no errors, then we can continue
                try:
                    # We write the message onto the network and print a success statement
                    self.heartbeatWriter.write()
                    print(f"Wrote message {value_dictionary}")
                except Exception as e:
                    # We catch any errors with sending the message
                    print(f"Error in writing the heartbeat for heartbeat: {e}")
            elif ef == 1:
                print(f"Issue writing the device ID {value_dictionary['deviceId']}")
            elif ef == 2:
                print(f"Issue writing the sequence number {value_dictionary['heartbeat']}")
            else:
                print(f"Issue writing both deviceId and sequence number")
        else:
            # We alert the user that the writer object was not initialized
            print("The heartbeatWriter has not been set yet.")

    async def publishDeviceUpdate(self, value_dictionary: dict) -> None:
        if self.deviceUpdateWriter is not None:  # Here we make sure that the writer object was initialized
            try:
                self.deviceUpdateWriter.instance.set_string("deviceId", value_dictionary["deviceId"])
                self.deviceUpdateWriter.instance.set_number("internalVoltage", value_dictionary["internalVoltage"])
                self.deviceUpdateWriter.instance.set_number("stateOfCharge", value_dictionary["stateOfCharge"])
                self.deviceUpdateWriter.instance.set_number("availableEnergy", value_dictionary["availableEnergy"])
                self.deviceUpdateWriter.instance.set_number("holdTime", value_dictionary["holdTime"])
                self.deviceUpdateWriter.instance.set_dictionary(value_dictionary['chargeTime'])
                self.deviceUpdateWriter.instance.set_dictionary(value_dictionary['dischargeTime'])
                self.deviceUpdateWriter.instance.set_dictionary(value_dictionary['maxChargeTime'])
                self.deviceUpdateWriter.instance.set_dictionary(value_dictionary['maxDischargeTime'])
                self.deviceUpdateWriter.instance.set_number('maxChargeRate', value_dictionary['maxChargeRate'])
                self.deviceUpdateWriter.instance.set_number('maxDischargeRate', value_dictionary['maxDischargeRate'])
            except Exception as e:
                print(f"4: {e = }")
            try:
                self.deviceUpdateWriter.write()
                print("wrote storage update")
            except:
                print("No wrote")

    async def publishDeviceInfo(self, value_dictionary: dict) -> None:
        if self.deviceInfoWriter is not None:
            try:
                self.deviceInfoWriter.instance.set_string("deviceId", value_dictionary['deviceId'])
                self.deviceInfoWriter.instance.set_string('role', value_dictionary['role'])
                self.deviceInfoWriter.instance.set_dictionary('product', value_dictionary['product'])
                self.deviceInfoWriter.instance.set_dictionary('topics', value_dictionary['topics'])
                self.deviceInfoWriter.write()
                print("Wrote Dev Info")
            except Exception as e:
                print(f"{e = }")


class Subscriber:
    def __init__(self, connector):
        self.self = self
        self.connector = connector

    async def listen(self):
        '''

        participant = dds.DomainParticipant(domain_id=0)
        topic = dds.Topic(participant, 'HelloWorld Topic', HelloWorld)
        reader = dds.DataReader(participant.implicit_subscriber, topic)


        async def print_data():
        async for data in reader.take_data_async():
        print(f"Received: {data}")
        :return:
        '''


global messages
messages = []

biggerValues = []


def test_storage_update(self):
    path = r"C:\Users\thomas.mcgowan\XE4012\team-repo-12-tactical-energy-storage\Test Ground\middleware_files\TEST_storage_update_data.csv"
    curCount = 0

    # keys = {}
    # messages = []
    with open(path, 'r') as f:
        file = csv.reader(f)
        for line in file:
            register_values = {}
            if curCount == 0:
                # keys = self.generateKey(line)
                curCount += 1
            else:
                print(f"{curCount = }")
                curCount += 1
                # -------
                register_values["deviceId"] = line[0]
                register_values["internalVoltage"] = float(line[1])
                register_values["soc"] = float(line[2])
                register_values["availableEnergy"] = float(line[3])
                register_values["holdTime"] = float(line[4])
                register_values["chargeTime"] = self.tempCurvechargeTime
                register_values["dischargeTime"] = self.tempCurvedischargeTime
                register_values["maxChargeTime"] = self.tempCurvemaxChargeTime
                register_values["maxDischargeTime"] = self.tempCurvemaxDischargeTime
                register_values["maxChargeRate"] = float(line[9])
                register_values["maxDischargeRate"] = float(line[10])
                biggerValues.append(register_values)
    f.close()


class Demo:
    def __init__(self, connector):
        self.self = self
        self.connector = connector
        self.heartbeatWriter = self.connector.get_output("TmsPublisher::HeartbeatWriter")
        self.deviceUpdateWriter = self.connector.get_output("TmsPublisher::StorageUpdateWriter")
        self.deviceInfoWriter = self.connector.get_output("TmsPublisher::DeviceInfoWriter")
        self.bigValues = biggerValues  # test_storage_update()
        # asyncio.run(self.test_storage_update())
        self.tempCurve = {
            "points": [
                {"x": 1.0, "y": 2.0},
                {"x": 3.5, "y": 4.5},
                {"x": 5.0, "y": 6.0},
                # Add more points as needed, up to 21
            ]
        }
        self.tempCurvechargeTime = {
            'chargeTime': {
                "points": [
                    {"x": 1.0, "y": 2.0},
                    {"x": 3.5, "y": 4.5},
                    {"x": 5.0, "y": 6.0},
                    # Add more points as needed, up to 21
                ]
            }
        }
        self.tempCurvedischargeTime = {
            'dischargeTime': {
                "points": [
                    {"x": 1.0, "y": 2.0},
                    {"x": 3.5, "y": 4.5},
                    {"x": 5.0, "y": 6.0},
                    # Add more points as needed, up to 21
                ]
            }
        }
        self.tempCurvemaxChargeTime = {
            'maxChargeTime': {
                "points": [
                    {"x": 1.0, "y": 2.0},
                    {"x": 3.5, "y": 4.5},
                    {"x": 5.0, "y": 6.0},
                    # Add more points as needed, up to 21
                ]
            }
        }
        self.tempCurvemaxDischargeTime = {
            'maxDischargeTime': {
                "points": [
                    {"x": 1.0, "y": 2.0},
                    {"x": 3.5, "y": 4.5},
                    {"x": 5.0, "y": 6.0},
                    # Add more points as needed, up to 21
                ]
            }
        }
        # Corrected product info dictionary for RTI Connext DDS
        self.product_info = {
            "product": {
                "nsn": ["1234567890123"],  # Fixed-length array of 13 characters
                "gtin": ["00123456789012"],  # Fixed-length array of 14 characters
                "manufacturerName": "Acme Corp",  # Standard strings
                "modelName": "SmartDeviceX",
                "modelNumber": "SDX-1000",
                "serialNumber": "SN12345678",
                "softwareVersion": "v1.0.3",
                "platformId": "Platform-42"  # Optional field
            }
        }
        self.topicInfo = {
            "topics": {
                "dataModelVersion": "0.0.0",
                "publishedConditionalTopics": ["CS_CONNECTED"],
                "publishedOptionalTopics": ["CS_CONNECTED"],
                "supportedRequestTopics": ["CS_CONNECTED"],
            }
        }

    def generateKey(self, line):
        keys = {}
        counter = 0
        for thing in line:
            keys[thing] = counter
            counter += 1
        return keys

    async def test_storage_update(self):
        path = r"C:\Users\thomas.mcgowan\XE4012\team-repo-12-tactical-energy-storage\Test Ground\middleware_files\TEST_storage_update_data.csv"
        curCount = 0

        # keys = {}
        # messages = []
        with open(path, 'r') as f:
            file = csv.reader(f)
            for line in file:
                register_values = {}
                if curCount == 0:
                    # keys = self.generateKey(line)
                    curCount += 1
                else:
                    print(f"{curCount = }")
                    curCount += 1
                    # -------
                    register_values["deviceId"] = line[0]
                    register_values["internalVoltage"] = float(line[1])
                    register_values["soc"] = float(line[2])
                    register_values["availableEnergy"] = float(line[3])
                    register_values["holdTime"] = float(line[4])
                    register_values["chargeTime"] = self.tempCurvechargeTime
                    register_values["dischargeTime"] = self.tempCurvedischargeTime
                    register_values["maxChargeTime"] = self.tempCurvemaxChargeTime
                    register_values["maxDischargeTime"] = self.tempCurvemaxDischargeTime
                    register_values["maxChargeRate"] = float(line[9])
                    register_values["maxDischargeRate"] = float(line[10])
                    # asyncio.run(xml.publishDevicecUpdate(register_values))
                    # message = await xml.testStorageUpdate(data=register_values, message=None)
                    # print(message)
                    self.bigValues.append(register_values)
        f.close()
        return self.bigValues

    async def createStorageUpdateMessage(self, dataD: dict = None):
        print(self.bigValues)
        # await self.test_storage_update()

        if self.deviceUpdateWriter is not None:  # Here we make sure that the writer object was initialized
            for data in self.bigValues:
                print("data")
                try:
                    self.deviceUpdateWriter.instance.set_string("deviceId", data["deviceId"])
                    self.deviceUpdateWriter.instance.set_number("internalVoltage", data["internalVoltage"])
                    self.deviceUpdateWriter.instance.set_number("stateOfCharge", data["soc"])
                    self.deviceUpdateWriter.instance.set_number("availableEnergy", data["availableEnergy"])
                    self.deviceUpdateWriter.instance.set_number("holdTime", data["holdTime"])
                    self.deviceUpdateWriter.instance.set_dictionary(data['chargeTime'])
                    self.deviceUpdateWriter.instance.set_dictionary(data['dischargeTime'])
                    self.deviceUpdateWriter.instance.set_dictionary(data['maxChargeTime'])
                    self.deviceUpdateWriter.instance.set_dictionary(data['maxDischargeTime'])
                    self.deviceUpdateWriter.instance.set_number('maxChargeRate', data['maxChargeRate'])
                    self.deviceUpdateWriter.instance.set_number('maxDischargeRate', data['maxDischargeRate'])
                    print(self.deviceUpdateWriter.instance)
                    self.deviceUpdateWriter.write()
                    time.sleep(1)
                    # print(f"Wrote {self.deviceUpdateWriter.instance = }")

                except Exception as e:
                    print(f"4: {e = }")

    async def createStorageUpdateMessagePassed(self, data: dict = None):
        print("data")
        if self.deviceUpdateWriter is not None:  # Here we make sure that the writer object was initialized
            try:
                self.deviceUpdateWriter.instance.set_string("deviceId", data["deviceId"])
                self.deviceUpdateWriter.instance.set_number("internalVoltage", data["internalVoltage"])
                self.deviceUpdateWriter.instance.set_number("stateOfCharge", data["soc"])
                self.deviceUpdateWriter.instance.set_number("availableEnergy", data["availableEnergy"])
                self.deviceUpdateWriter.instance.set_number("holdTime", data["holdTime"])
                self.deviceUpdateWriter.instance.set_dictionary(data['chargeTime'])
                self.deviceUpdateWriter.instance.set_dictionary(data['dischargeTime'])
                self.deviceUpdateWriter.instance.set_dictionary(data['maxChargeTime'])
                self.deviceUpdateWriter.instance.set_dictionary(data['maxDischargeTime'])
                self.deviceUpdateWriter.instance.set_number('maxChargeRate', data['maxChargeRate'])
                self.deviceUpdateWriter.instance.set_number('maxDischargeRate', data['maxDischargeRate'])
                print(self.deviceUpdateWriter.instance)
                self.deviceUpdateWriter.write()
                time.sleep(1)
                # print(f"Wrote {self.deviceUpdateWriter.instance = }")

            except Exception as e:
                print(f"4: {e = }")

    async def createDeviceInfoMessage(self, dataD: dict = None) -> None:
        if self.deviceInfoWriter is not None:
            try:
                self.deviceInfoWriter.instance.set_string('deviceId', "cadet-battery")
                self.deviceInfoWriter.instance.set_number('role', 4)
                self.deviceInfoWriter.instance.set_dictionary(self.product_info)
                self.deviceInfoWriter.instance.set_dictionary(self.topicInfo)  # tms::topicinfo
                self.deviceInfoWriter.write()
                print("WROTE IT")
            except Exception as e:
                print(f"{e = }")


async def heartBeat(connection, dictionary: dict) -> None:
    """
    In this function, we initialize a connector and pass that into our publisher class. We then await the function
    :param dictionary: dictionary that holds the data from the Middleware script
    :return: None
    """
    # with rti.open_connector(
    #         config_name="TmsParticipantLibrary::TmsParticipant",
    #         url=ppath) as device:
    #     test = Publisher(device)
    test = Publisher(connection)
    await test.publishHeartbeat(dictionary)


import datetime


async def publishDevicecUpdate(dictionary: dict, device) -> None:
    # with rti.open_connector(
    #         config_name="TmsParticipantLibrary::TmsParticipant",
    #         url=ppath) as device:
    test = Publisher(device)
    # print(f"time before we publish: {datetime.datetime.now()}")
    await test.publishDeviceUpdate(dictionary)
    # print(f"Time after we publish: {datetime.datetime.now()}")


async def testStorageUpdate(connection, data=None, message=None):
    # with rti.open_connector(
    #         config_name="TmsParticipantLibrary::TmsParticipant",
    #         url=ppath) as device:
    test = Demo(connection)
    await test.test_storage_update()
    await test.createStorageUpdateMessage()


async def testStorageUpdateOnce(connection, data=None):
    test = Demo(connection)
    await test.test_storage_update()
    data = biggerValues[0]
    await test.createStorageUpdateMessagePassed(data)


async def testHeartbeat(connection, hb):
    test = Demo(connection)
    test.heartbeatWriter.instance.set_string("deviceId", hb['deviceId'])
    test.heartbeatWriter.instance.set_number('sequenceNumber', hb['heartbeat'])
    # await test.heartbeatWriter.instn
    test.heartbeatWriter.write()


async def publishDeviceInfo(connection, info):
    test = Publisher(connection)
    await test.publishDeviceInfo(info)


async def testDeviceInfo(connection):
    test = Demo(connection)
    await test.createDeviceInfoMessage()
