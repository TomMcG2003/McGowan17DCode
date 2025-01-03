# hello_publisher.py

import sys
from sys import path as sys_path
from os import path as os_path
from time import sleep
import rticonnextdds_connector as rti

ppath = r"C:\Users\thomas.mcgowan\XE4012\team-repo-12-tactical-energy-storage\Capstone\xml\tmg_xml_24_mar.xml"

device = rti.open_connector(
        config_name="TmsParticipantLibrary::TmsParticipant",
        url=ppath)
print(f"connector\t{device}")
heartbeatWriter = device.get_output("TmsPublisher::HeartbeatWriter")
