import sys
import pprint

# See RTI python documentation for how to make sure
# the RTI provided python packages can be loaded
from sys import path as sys_path
from os import path as os_path
# from middleware_files.BatterCalls import Battery
# TODO: How can I import the BatteryCalls module from the other file?

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")
ppath = "C:\\Users\\thomas.mcgowan\\XE4012\\team-repo-12-tactical-energy-storage\\Capstone\\xml\\tmg_xml_24_mar.xml"
# file_path + "/xml/NewProject.xml"

import rticonnextdds_connector as rti

print("Start " + repr(__file__))
print(file_path)
# Join a DDS Domain with the specified subscriber
with rti.open_connector(
        config_name="TmsParticipantLibrary::TmsParticipant",
        url=ppath) as connector:
    # Get a data reader from the subscriber for each TMS topic needed
    print("Get HeartbeatReader...")
    heartbeatReader = connector.get_input("TmsSubscriber::HeartbeatReader")

    print("Get StorageUpdate Reader...")
    storageUpdateReader = connector.get_input("TmsSubscriber::StorageUpdateReader")

    print("Get DeviceInfoReader...")
    deviceInfoReader = connector.get_input("TmsSubscriber::DeviceInfoReader")

    print("Get ESS Command Reader...")
    essCommandReader = connector.get_input("TmsSubscriber::ESSCommandReader")

    # Create a pretty printer to format topic data dictionary
    pp = pprint.PrettyPrinter(indent=2)

    print("Waiting for topic data...")
    for i in range(1, sys.maxsize):  # sys.maxsize
        try:
            # Add additional data readers as needed.
            # read the TMS DeviceInfo topic
            # Throws exception if timeout is reached
            deviceInfoReader.wait(100)  # wait for data
            # if this is reached, there is at least 1 instance to "read".
            deviceInfoReader.take()

            # Each instance read include sample information and the topic data
            for sample in deviceInfoReader.samples.valid_data_iter:
                # Get the time stamp from when the publisher wrote the instance
                source_timestamp = sample.info['source_timestamp']
                # Get the type data for this topic
                deviceInfo = sample.get_dictionary()
                print(repr(i) + " DeviceInfo: ")
                # Use the pretty printer so the output can be copy/pasted into a data writer
                # call to set_dictionary.
                pp.pprint(deviceInfo)
        except:
            print("No DeviceInfo samples")

        # read the TMS Heart beat topic

        try:
            # Throws exception if timeout
            heartbeatReader.wait(1000)  # wait for data on this heartbeatReader
            heartbeatReader.take()

            for sample in heartbeatReader.samples.valid_data_iter:
                heartbeat = sample.get_dictionary()
                deviceId = heartbeat['deviceId']
                sequenceNumber = heartbeat['sequenceNumber']
                print(repr(i) + " heartbeat: " + repr(heartbeat))
        except:
            print("No heartbeat samples")

        try:
            storageUpdateReader.wait(1000)
            storageUpdateReader.take()
            for sample in storageUpdateReader.samples.valid_data_iter:
                update = sample.get_dictionary()
                deviceId = update['deviceId']
                internalVoltage = update['internalVoltage']
                soc = update["stateOfCharge"]
                availEnergy = update["availableEnergy"]
                holdTime = update["holdTime"]
                chargeTime = update["chargeTime"]
                dischargeTime = update["dischargeTime"]
                maxCT = update['maxChargeTime']
                maxDT = update['maxDischargeTime']
                mcr = update['maxChargeRate']
                mdr = update['maxDischargeRate']
                print(f"{deviceId = }, {internalVoltage = }, {soc = }, {availEnergy = }, {holdTime = }, "
                      f"{chargeTime = }, {dischargeTime = }, maxChargeTime = {maxCT}, maxDischargeTime = {maxDT}"
                      f"maxChargeRate = {mcr}, maxDischargeRate = {mcr}")

        except Exception as e:
            print(e)
            print("No storage updates")

        try:
            essCommandReader.wait(1000)
            essCommandReader.take()
            for sample in essCommandReader.sample.valid_data_iter:
                command = sample.get_dictionary()
                target = command["TargetESS"]
                print(repr(i) + " command: " + repr(command))
        except:
            print("No ESS Command Info")


    print("Exiting after a really long time :)")
