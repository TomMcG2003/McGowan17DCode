from enum import Enum


class ConfigID(Enum):
    CONFIG_UNKNOWN = 0
    CONFIG_DEFAULTS = 1
    CONFIG_ACTIVE = 2
    CONFIG_ON_REBOOT = 3
    CONFIG_ON_COMMS_LOSS = 4


class ReplyStatus(Enum):
    REPLY_UNKNOWN = 0
    REPLY_OK = 1
    REPLY_BAD_REQUEST = 2
    REPLY_METHOD_NOT_ALLOWED = 3
    REPLY_CONFLICT = 4
    REPLY_GONE = 5
    REPLY_PRECONDITION_FAILED = 6
    REPLY_INTERNAL_SERVER_ERROR = 7
    REPLY_NOT_IMPLEMENTED = 8
    REPLY_SERVICE_UNAVAILABLE = 9
    REPLY_PENDINN_AUTHORIZATION = 10
    REPLY_NOT_MASTER = 11


class MicrogridDashboardFeature(Enum):
    MDF_UNKNOWN = 0
    MDF_DISPLAY = 1
    MDF_CONTROL = 2


class DeviceRole(Enum):
    ROLE_UNKNOWN = 0
    ROLE_MICROGRID_CONTROLLER = 1
    ROLE_SOURCE = 2
    ROLE_LOAD = 3
    ROLE_STORAGE = 4
    ROLE_DISTRIBUTION = 5
    ROLE_MICROGRID_DASHBOARD = 6
    ROLE_CONVERSION = 7
    ROLE_MONITOR = 8


class MicrogridControllerFeature(Enum):
    MCF_UNKNOWN = 0
    MCF_FIXED = 1
    MCF_GENERAL = 2


class CircuitWiring(Enum):
    WIRING_UNKNOWN = 0
    WIRING_AC_SINGLE = 1
    WIRING_AC_SPLIT = 2
    WIRING_AC_3WYE = 3
    WIRING_AC_3DELTA = 4
    WIRING_DC = 5
    WIRING_DC_3WIRE = 6


class PowerPortDirectionality(Enum):
    PPD_UNKNOWN = 0
    PPD_NONE = 1
    PPD_IN = 2
    PPD_OUT = 3
    PPD_IN_OUT = 4


class PowerConnectorFeature(Enum):
    PCF_UNKNOWN = 0
    PCF_CABLE_SENSE = 1
    PCF_CABLE_ID_READER = 2
    PCF_CABLE_MEASUREMENT = 3
    PCF_COMMUNICATION = 4
    PCF_TOPOLOGY_DISCOVERY = 5


class PowerConnectorType(Enum):
    CONNECTOR_UNKNOWN = 0
    CONNECTOR_TERMINAL_BLOCK = 1
    CONNECTOR_MILSTD = 2
    CONNECTOR_NEMA5 = 3
    CONNECTOR_CAMLOCK = 4
    CONNECTOR_POWERLOCK = 5
    CONNECTOR_IEC60309 = 6
    CONNECTOR_J1772 = 7
    CONNECTOR_POWERLOK = 8
    CONNECTOR_MILSTD1651 = 9
    CONNECTOR_MILDTL22992 = 10
    CONNECTOR_MILDTL53126 = 11
    CONNECTOR_OTHER = 12
    CONNECTOR_METER = 13
    CONNECTOR_BUS = 14


class PowerConnectorPolarity(Enum):
    POLARITY_UNKNOWN = 0
    POLARITY_PIN = 1
    POLARITY_SOCKET = 2
    POLARITY_UNIVERSAL = 3


class PowerSwitchFeature(Enum):
    PAF_UNKNOWN = 0
    PSF_MANUAL_OPEN = 1
    PSF_MANUAL_CLOSE = 2
    PSF_AUTO_OPEN = 3
    PSF_AUTO_CLOSE = 4
    PSF_REQUEST_OPEN = 5
    PSF_REQUEST_CLOSE = 6
    PSF_LOCK = 7
    PSF_RECLOSER = 8
    PSF_BREAKER = 9
    PSF_GFI = 10
    PSF_ARC_FLASH = 11
    PSF_SYNCHRONIZER = 12
    PSF_SURGE = 13
    PSF_SWITCH_CONDITIONS = 14


class GroundingDesignType(Enum):
    GROUNDING_UNKNOWN = 0
    GROUNDING_UNGROUNDED = 1
    GROUNDING_SOLID = 2
    GROUNDING_HIGH_RESISTANCE = 3
    GROUNDING_LOW_RESISTANCE = 4
    GROUNDING_REACTANCE = 5


class ConversionFeature(Enum):
    CONVF_UNKNOWN = 0
    CONVF_ACTIVE = 1
    CONVF_PASSIVE = 2


class DistributionFeature(Enum):
    DISTF_UNKNOWN = 0
    DISTF_CLAMP_METER = 1
    DISTF_TAP_METER = 2
    DISTF_PCC = 3
    DISTF_FEEDER = 4
    DISTF_DISTRIBUTION = 5


class SourceFeature(Enum):
    SRCF_UNKNOWN = 0
    SRCF_GENSTE = 1
    SRCF_FUEL_CELL = 2
    SRCF_SOLAR = 3
    SRCF_WIND = 4
    SRCF_VEHICLE = 5


class EnergyStartStopLevel(Enum):
    ESSL_UNKNOWN = 0
    ESSL_ANY = 1
    ESSL_OFF = 2
    ESSL_WARM = 3
    ESSL_IDLE = 4
    ESSL_READY = 5
    ESSL_READY_SYNCED = 6
    ESSL_OPERATIONAL = 7


class StorageFeature(Enum):
    STORF_UNKNOWN = 0
    STORF_GRID = 1
    STORF_SUBCYCLES_UPS = 2
    STORF_CHARGING = 3
    STORF_VEHICHLE = 4


class LoadFeature(Enum):
    LOADF_UNKNOWN = 0
    LOADF_DEMAND_RESPONSE = 1
    LOADF_CHANGE_NOTIFICATION = 2
    LOADF_SOFT_START = 3
