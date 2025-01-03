# 12 - Tactical Energy Storage

This is the base repository for XE401-XE402 capstone project code for the Team 12 - Tactical Energy Storage group.

This repository will hold all the code for the capstone group. This includes code that we write for AY25 and code 
that was written by prior groups.

## Project Overview
The goal of this project is to deliver a Tactical Microgrid Standard (TMS) compliant Type II Energy Storage System (ESS)
with a updated Type V Control System. The role of the Type V Controller System is to autonomously operate the Microgrid 
(MG) to optimize for two conditions:
    
    1. Fuel efficiency when not under stress (i.e., all generators are operational, the MG is stable, etc.)
    2. Resiliency of the MG (i.e., generator(s) go down, MG is under attack, portions of MG go down, etc.)

To accomplish a TMS compliant ESS, the group must develop a middleware that offers bi-directional translation between 
TMS commands (commands that can be understood by the controller) and battery management system (BMS) commands (commands
that are executable and readable to the ESS' internal controller). For this project, the ESS is a Viridi Faveo Traffic 
Backup System. The group also has access to a Viridi SBR30-150 Mobile Energy Storage Solution. The middleware will be 
compatible between both of these ESS as Viridi uses the same internal controller over their ESS batteries. The 
controller that these ESS use is the Victron Energy Cerbo GX. 


To accomplish the updated controller, the group must analyze the existing control algorithms and either optimize them or
replace them with more applicable, efficient, and acceptable algorithms.

###Major Dependencies
Unique to this project is the need for an API that can communicate to our BMS system. For this, we are using the 
`pymodbus` module. You can find the GitHub repo for this module at *https://github.com/pymodbus-dev/pymodbus*. This 
module gives us access to the register values on the Cerbo GX which pulls the required information off of the Victron
inverter. We have been able to successfully communicate with the CerboGX with both read and write commands using this
API. 

Another unique aspect of this project is the tools that are used to facilitate fast and dynamic communication between
network devices. For this, we used the RTI Connext DDS module. This is a tool that allows the developer to declare and
initialize XML defined data types, quality of service standards, data readers, and data publishers. Using the XML file 
for this project, we can define readers and publishers that can pull packets off of the network and/or push packets onto
the network so that we can have seamless communications between entities on the network.

## ***What Have We Done So Far?***
* The progress that we make comes in work periods which we call sprints. These sprints last 7-9 lessons and can range 
from 2-4 weeks in duration. In total, there will be 6 sprints over the course of this project for AY25. The deliverables
and products of each sprint are listed below:

  - Sprint 1:
    - In this sprint, the main focus was on knowledge acquisition and wrapping our minds around the project. The main 
      deliverables of this project were in graphs and other depictions of the TMG and more speficially the ESS.
  - Sprint 2:
    - The focus of sprint 2 was to get into the battery and be able to communicate with this. This meant that we had to
    establish a LAN and install the battery's recommended API, pymodbus. Once we had the environment established, it 
    was time to review the register list from Viridi and start to communicate. The main deliverables and products from 
    this sprint were more matured block diagrams and other graphical descriptions of the TMG and also a script that 
    demonstrated out capability to communicate with the battery system.
  - Sprint 3:
    - The major lift of this sprint was to establish communication between separate TMS devices. For this sprint, we 
    were issued out RTI Connext DDS licences and then began to program the communication systems. With this, we were
    able to craft messages that were successfully sent and received by multiple TMS compliant control devices over our
    LAN. This solved a major bottleneck of our project.
  - Sprint 4: Not completed
  - Sprint 5: Not completed
  - Sprint 6: Not completed

## Files and Their Descriptions

* ***Capstone***: This folder holds the code from the AY23 capstone group. This code is what runs the controller.
External python modules used in *tms_reader.py* are:

    - rticonnectdds-connector: https://pypi.org/project/rticonnextdds-connector/
    - sys: https://docs.python.org/3/library/sys.html
    - pprint: https://docs.python.org/3/library/pprint.html
    - os: https://docs.python.org/3/library/os.html
    - enum
    - asyncio
    - numpy
    - pymodbus
    - time

External python modules used in *tms_writer.py* are:

    - rticonnectdds-connector: https://pypi.org/project/rticonnextdds-connector/
    - sys: https://docs.python.org/3/library/sys.html
    - os: https://docs.python.org/3/library/os.html
    - time: https://docs.python.org/3/library/time.html

External python moduls used in *tms_reader.py* are:

    - sys
    - pprint
    - os


* ***Files_for_SSHing***: This folder holds code that was written to streamline and expedite the SSHing procedure to get 
onto our Linux machine for the project.
* ***Test Ground***: This file holds code that is currently in product and is not ready to be released or used. Some of
this code is still in its infancy and some is awaiting testing. It is ill advised to use any of this code but feel free
to look at the files and see what is being developed.
  * ***Middleware_files***: This folder holds the code that, once pushed to production, will be placed onto the ESS
  controller.
    * ***rti_tester***: This folder holds the files that we used to test new implementations and features of the RIT
    communication software.
    * ***xml***: This holds the XMl file that we are using in testing
    * ***All other files***: This folder holds the implementation and enumeration of all structs and enumerations of TMS datatypes as 
    outlined in the TMS documentation. Also, within this folder holds the xml translator which acts as a middleware between
    the battery interface and the RTI network.
  * ***Middleware.py***: This file is the working model of the middleware that will be loaded onto the Raspberry Pi. 
  This middleware will be able to receive requests from the network and any packets it subscribes to, translate the
  request, execute required commands to satisfy the request, and put a TMS message back onto the network.
  * ***modbus_tester.py***: This file is used to test functionality of the pymodbus module and the BMS. Some functions
    are tested here to not interfere with any of the code meant for production in any of the other files.
  * ***simulator_tester.py***: This file is our test file to create a pymodbus server that will help to emulate TMS 
    devices. This will allow us to emulate the battery and other devices we would see on the grid which will remove the
    requirement to be connected to the physical battery to test coded.
  * ***readable_registers.txt***: This file tests what registers we can read from either as a system device (unitID=100)
    or as a general device (unitID=1). We still need to work around the fact that some registers ought to be readable but
    the unitID is note a valid reader.
  * ***setupt.json***: This is a running file of the configuration file that the server will need to properly build and
    run.
* ***Unused Code***: As the name suggests, this folder holds some code of projects or tangents that ended up not working
but still may add some insights into the project that we can learn from.

*As files are uploaded, this list will grow accordingly*

### Points of Contact
The members of the group are:

    - CDT Robert Anzilotti
        - Email: robert.anzilotti@westpoint.edu
    - CDT Jaden Beauchamp
        - Email: jaden.beauchamp@westpoint.edu
    - CDT Christopher Hunter
        - Email: christopher.hunter2@westpoint.edu
    - CDT Ian McGary
        - Email: ian.mcgary@westpoint.edu
    - CDT Thomas McGowan
        - Email: thomas.mcgowan@westpoint.edu

The advisors for the group are:

    - LTC Nicholas Barry
        - Email: nicholas.barry@westpoint.edu
    - Dr. Tom Cook
        - Email: thomas.cook@westpoint.edu
    - Dr. Aaron St. Leger
        - Email: aaron.stleger@westpoint.edu

The product owners are:

    - Group Advisors
    - United States Department of Defense
    - Viridi 