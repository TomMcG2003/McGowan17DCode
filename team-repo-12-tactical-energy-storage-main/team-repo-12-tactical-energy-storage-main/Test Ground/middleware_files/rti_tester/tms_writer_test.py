import sys
from sys import path as sys_path
from os import path as os_path
from time import sleep
import rticonnextdds_connector as rti

# See RTI python documentation for how to make sure
# the RTI provided python packages can be loaded 
file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "")
# This will have to changed for production but for testing purposes this will just be changed based on the developer who
# pulls it

"""
Overview of this file:
This file serves as the publishing script for the MicroGrid Controller. This specific script as of 07 DEC 2024 only
supports publishing heartbeats, device information, and active diagnostic state messages. The heartbeat is manually
set without checks of connectivity and only stops publishing when the script or hardware fail/exit. The device
information is statically set as the device information of the controller should not change unless the controller device
is changed. In this case, the engineer who swaps the device will have to revise the device information manually. The 
active diagnostic writer is also statically set and will have to be revised if the user wants dynamic diagnostic data
publishing. 

Overall this script publishes device information and diagnostic state data once at the inception of the script and then
publishes a heartbeat once every second until the maximum system size is reached or the script/hardware has an error. 
"""

ppath = r"C:\Users\thomas.mcgowan\XE4012\team-repo-12-tactical-energy-storage\Capstone\xml\tmg_xml_24_mar.xml"

print(f"{ppath = }")
# print("Start " + repr(__file__))

# Initialize RTI with a specified participant name and XML file.
# Important: the names in this example must match names in the tms_dds_profiles.xml.
with rti.open_connector(
        config_name="TmsParticipantLibrary::TmsParticipant",
        url=ppath) as connector:
    print(f"connector\t{connector}")
    # Get a data writer for each topic that must be published. 
    # These writers must be specified in the XML file (tms_dds_profiles.xml)
    heartbeatWriter = connector.get_output("TmsPublisher::HeartbeatWriter")
    deviceInfoWriter = connector.get_output("TmsPublisher::DeviceInfoWriter")
    activeDiagnosticStateWriter = connector.get_output("TmsPublisher::ActiveDiagnosticStateWriter")
    commandWriter = connector.get_output("TmsPublisher::ESSCommandWriter")
    # This will be the writer for the ESS commander.

    # Set all the required fields in the instance of the DeviceInfo before publishing (a.k.a. writing).
    # See the TMS-TGP IDL for all the required fields including nested types.
    print("Writing DeviceInfo.")

    # Set single field using the instance methods
    deviceInfoWriter.instance.set_string("deviceId", "python-1")
    deviceInfoWriter.instance.set_number("role", 1)
    deviceInfoWriter.instance.set_string("product.manufacturerName", "West Point")

    # Set the instance values using a dictionary
    # TIP: Use the pretty print output from a Python subscriber as a template for the dictionary
    deviceInfoWriter.instance.set_dictionary({
        "product": {
            'nsn': ['4', '5', '6', '9', '1', '1', '1', '1', '1', '0', '0', '0', '1'],
            'manufacturerName': 'My Name Goes Here',
            'modelName': 'West Point MC'
        },
        'topics': {
            'dataModelVersion': '1.2.3',
            'publishedConditionalTopics': [],
            'publishedOptionalTopics': [],
            'supportedRequestTopics': []
        }
    })
    # Call write to "published" the instance
    print(" Writing deviceInfoWriter: " + repr(deviceInfoWriter.instance.get_dictionary()))
    deviceInfoWriter.write()

    # Publish additional topics
    print("Writing ActiveDiagnosticState.")
    activeDiagnosticStateWriter.instance.set_string("deviceId", "python-1")

    print(" Writing ActiveDiagnosticState: " + repr(activeDiagnosticStateWriter.instance.get_dictionary()))
    activeDiagnosticStateWriter.write()

    # Continue to publish the heart beat every second
    print("Writing heart beat loop started...")
    for i in range(1, sys.maxsize):
        heartbeatWriter.instance.set_string("deviceId", "python-1")
        heartbeatWriter.instance.set_number("sequenceNumber", i)
        print("Writing heartbeatWriter sequenceNumber: " + repr(i))
        heartbeatWriter.write()
        '''
        This is where I want to try out writing the controls from the MGC to the BMC.
        <struct name="ESSCommand">
          <member name="TargetESS" type="nonBasic" nonBasicTypeName="tms::Identity" key="true"/>
          <member name="Command" type="nonBasic" nonBasicTypeName="tms::ESS_Commands"/>
          <member name="TargetSOC" type="float32" min="0" max="1"/>
          <member name="ChargeRate" type="float32" min="0" max="10000"/>
          <member name="DischargeRate" type="float32" min="0" max="10000"/>
          <member name="TimeStamp" type="nonBasic" nonBasicTypeName="tms::ClockState"/>
        </struct>
        '''
        commandWriter.instance.set_string("TargetESS", "capstone")
        commandWriter.instance.set_number("Command", 2)
        commandWriter.instance.set_number("TargetSOC", 0.80)
        commandWriter.instance.set_number("ChargeRate", 0.5)
        commandWriter.instance.set_number("DischargeRate", 0.0)

        commandWriter.write()
        print(" Writing commandWriter: " + repr(commandWriter.instance.get_dictionary()))

        # Pause before the next call to write
        sleep(1)

    print("Exiting...")
