from pymodbus.server import ModbusSimulatorServer
import asyncio

test = {
    "server_list": {
        "server": {
            "comm": "tcp",
            "host": "0.0.0.0",
            "port": 5020,
            "ignore_missing_slaves": False,
            "framer": "socket",
            "identity": {
                "VendorName": "pymodbus",
                "ProductCode": "PM",
                "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
                "ProductName": "pymodbus Server",
                "ModelName": "pymodbus Server",
                "MajorMinorRevision": "3.1.0"
            }
        },
        "server_try_serial": {
            "comm": "serial",
            "port": "/dev/tty0",
            "stopbits": 1,
            "bytesize": 8,
            "parity": "N",
            "baudrate": 9600,
            "timeout": 3,
            "reconnect_delay": 2,
            "framer": "rtu",
            "identity": {
                "VendorName": "pymodbus",
                "ProductCode": "PM",
                "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
                "ProductName": "pymodbus Server",
                "ModelName": "pymodbus Server",
                "MajorMinorRevision": "3.1.0"
            }
        },
        "server_try_tls": {
            "comm": "tls",
            "host": "0.0.0.0",
            "port": 5020,
            "certfile": "certificates/pymodbus.crt",
            "keyfile": "certificates/pymodbus.key",
            "ignore_missing_slaves": False,
            "framer": "tls",
            "identity": {
                "VendorName": "pymodbus",
                "ProductCode": "PM",
                "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
                "ProductName": "pymodbus Server",
                "ModelName": "pymodbus Server",
                "MajorMinorRevision": "3.1.0"
            }
        },
        "server_test_try_udp": {
            "comm": "udp",
            "host": "0.0.0.0",
            "port": 5020,
            "ignore_missing_slaves": False,
            "framer": "socket",
            "identity": {
                "VendorName": "pymodbus",
                "ProductCode": "PM",
                "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
                "ProductName": "pymodbus Server",
                "ModelName": "pymodbus Server",
                "MajorMinorRevision": "3.1.0"
            }
        }
    },
    "device_list": {
        "device": {
            "setup": {
                "co size": 63000,
                "di size": 63000,
                "hr size": 63000,
                "ir size": 63000,
                "shared blocks": True,
                "type exception": True,
                "defaults": {
                    "value": {
                        "bits": 0,
                        "uint16": 0,
                        "uint32": 0,
                        "float32": 0.0,
                        "string": " "
                    },
                    "action": {
                        "bits": None,
                        "uint16": "increment",
                        "uint32": "increment",
                        "float32": "increment",
                        "string": None
                    }
                }
            },
            "invalid": [
                1
            ],
            "write": [
                3
            ],
            "bits": [
                {"addr": 2, "value": 7}
            ],
            "uint16": [
                {"addr": 3, "value": 17001, "action": None},
                2100
            ],
            "uint32": [
                {"addr": [4, 5], "value": 617001, "action": None},
                [3037, 3038]
            ],
            "float32": [
                {"addr": [6, 7], "value": 404.17},
                [4100, 4101]
            ],
            "string": [
                5047,
                {"addr": [16, 20], "value": "A_B_C_D_E_"}
            ],
            "repeat": [
            ]
        },
        "device_try": {
            "setup": {
                "co size": 63000,
                "di size": 63000,
                "hr size": 63000,
                "ir size": 63000,
                "shared blocks": True,
                "type exception": True,
                "defaults": {
                    "value": {
                        "bits": 0,
                        "uint16": 0,
                        "uint32": 0,
                        "float32": 0.0,
                        "string": " "
                    },
                    "action": {
                        "bits": None,
                        "uint16": None,
                        "uint32": None,
                        "float32": None,
                        "string": None
                    }
                }
            },
            "invalid": [
                [0, 5],
                77
            ],
            "write": [
                10
            ],
            "bits": [
                10,
                1009,
                [1116, 1119],
                {"addr": 1144, "value": 1},
                {"addr": [1148, 1149], "value": 32117},
                {"addr": [1208, 1306], "action": "random"}
            ],
            "uint16": [
                11,
                2027,
                [2126, 2129],
                {"addr": 2164, "value": 1},
                {"addr": [2168, 2169], "value": 32117},
                {"addr": [2208, 2304], "action": "increment"},
                {"addr": 2305,
                 "value": 50,
                 "action": "increment",
                 "parameters": {"minval": 45, "maxval": 155}
                 },
                {"addr": 2306,
                 "value": 50,
                 "action": "random",
                 "parameters": {"minval": 45, "maxval": 55}
                 }
            ],
            "uint32": [
                [12, 13],
                [3037, 3038],
                [3136, 3139],
                {"addr": [3174, 3175], "value": 1},
                {"addr": [3188, 3189], "value": 32514},
                {"addr": [3308, 3407], "action": None},
                {"addr": [3688, 3875], "value": 115, "action": "increment"},
                {"addr": [3876, 3877],
                 "value": 50000,
                 "action": "increment",
                 "parameters": {"minval": 45000, "maxval": 55000}
                 },
                {"addr": [3878, 3879],
                 "value": 50000,
                 "action": "random",
                 "parameters": {"minval": 45000, "maxval": 55000}
                 }
            ],
            "float32": [
                [14, 15],
                [4047, 4048],
                [4146, 4149],
                {"addr": [4184, 4185], "value": 1},
                {"addr": [4188, 4191], "value": 32514.2},
                {"addr": [4308, 4407], "action": None},
                {"addr": [4688, 4875], "value": 115.7, "action": "increment"},
                {"addr": [4876, 4877],
                 "value": 50000.0,
                 "action": "increment",
                 "parameters": {"minval": 45000.0, "maxval": 55000.0}
                 },
                {"addr": [4878, 48779],
                 "value": 50000.0,
                 "action": "random",
                 "parameters": {"minval": 45000.0, "maxval": 55000.0}
                 }
            ],
            "string": [
                {"addr": [16, 20], "value": "A_B_C_D_E_"},
                {"addr": [529, 544], "value": "Brand name, 32 bytes...........X"}
            ],
            "repeat": [
            ]
        }
    }
}


async def run():
    simulator = ModbusSimulatorServer(
        modbus_server="server",
        modbus_device="device",
        http_host="localhost",
        http_port=8080
    )
    await simulator.run_forever(only_start=True)

    await simulator.stop()


asyncio.run(run())
# print(test["server_list"]['server'])
