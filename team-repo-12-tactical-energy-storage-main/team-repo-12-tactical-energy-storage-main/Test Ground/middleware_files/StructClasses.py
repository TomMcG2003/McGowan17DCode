import EnumClasses as ec


class Point2D:
    def __init__(self, x: int, y: int):
        self.self = self
        self.x = x
        self.y = y
        self.point = {'x': self.x, 'y': self.y}

    def __str__(self):
        # return f"({self.x}, {self.y})"
        return f"{self.point}"


class Point2DSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def add_data(self, data: Point2D):
        """
        This can only append Point2D objects
        :param data:
        :return:
        """
        self.sequence.append(data.point)

    def append_data(self, data: Point2D):
        pass

    def delete_data(self, data: Point2D):
        self.sequence.remove(data)

    def __len__(self):
        return len(self.sequence)

    def __str__(self):
        # string = ""
        # for point in self.sequence:
        #     string += f"{str(point)}, "
        # return string
        return f"{self.sequence}"


class Curve2D:
    """
    This is the data structure used for all of the Curve2D requirements of the TMS standard
    """

    def __init__(self):
        self.self = self
        self.data_points = {'points': []}

    def to_dict(self):
        return self.data_points

    def add_data(self, point: Point2D or Point2DSequence or dict) -> None:
        """
        Adds a data point into the data list
        :param point: tuple of (x, y) form
        :return: None or TypeError
        """
        # print(f"{point = }")
        # print(f"{self.data_points = }")
        if isinstance(point, Point2D):
            # self.data_points['points'].append(point)
            self.data_points['points'].append(point.point)
        elif isinstance(point, Point2DSequence):
            for i in point:
                self.data_points['points'].add_data(i)
        elif isinstance(point, list):
            self.data_points['points'] += point
        else:
            raise TypeError

    def remove_point(self, point: Point2D) -> tuple:
        """
        Removes the first instance of a data point and returns the removed data point
        :param point: tuple of (x, y) form
        :return: tuple or TypeError
        """
        if isinstance(point, Point2D):
            self.data_points.delete_data(point)
            return point
        else:
            raise TypeError

    def __len__(self):
        return len(self.data_points)

    def __str__(self):
        return f"length: {len(self.data_points)}, {self.data_points}"


class EngineInfo:
    def __init__(self, minOilPressure: float, maxOilPressure: float, minCoolantTemperature: float,
                 maxCoolantTemperature: float, minEngineSpeed: float, maxEngineSpeed: float,
                 minWetStackPreventionLoad: float, minWetStackMitigationLoad: float):
        self.self = self
        self.minOilPressure = minOilPressure
        self.maxOilPressure = maxOilPressure
        self.minCoolantTemperature = minCoolantTemperature
        self.maxCoolantTemperature = maxCoolantTemperature
        self.minEngineSpeed = minEngineSpeed
        self.maxEngineSpeed = maxEngineSpeed
        self.minWetStackPreventionLoad = minWetStackPreventionLoad
        self.minWetStackMitigationLoad = minWetStackMitigationLoad


class FuelInfo:
    def __init__(self, maxFuelLevel: float, minFuelLevelCutoff: float):
        self.self = self
        self.maxFuelLevel = maxFuelLevel
        self.minFuelLevelCutoff = minFuelLevelCutoff


class GeneratorInfo:
    def __init__(self, minFieldCurrent: float, maxFieldCurrent: float, maxStatorTemperature: float):
        self.self = self
        self.minFieldCurrent = minFieldCurrent
        self.maxFieldCurrent = maxFieldCurrent
        self.maxStatorTemperature = maxStatorTemperature


class EnergyStorageInfo:
    def __init__(self, highStateOfCharge: float, lowStateOfCharge: float, minTemperature: float, nomTemperature: float,
                 maxTemperature: float):
        self.self = self
        self.highStateOfCharge = highStateOfCharge
        self.lowStateOfCharge = lowStateOfCharge
        self.minTemperature = minTemperature
        self.nomTemperature = nomTemperature
        self.maxTemperature = maxTemperature


class PowerElectronicsInfo:
    def __init__(self, minTemperature: float, maxTemperature: float):
        self.self = self
        self.minTemperature = minTemperature
        self.maxTemperature = maxTemperature


class ThermalInfo:
    def __init__(self, thermalZone: tuple[str]):
        self.self = self
        self.thermalZone = thermalZone


class ThermalZoneSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def __append__(self, thermalValue: str):
        if len(thermalValue) > 32:
            raise ValueError
        else:
            self.sequence.append(thermalValue)


class SynchronousMachineCoefficients:
    def __init__(self, statorResistancePerPhase: float,
                 statorLeakageReactance: float,
                 zeroSequenceReactance: float,
                 negativeSequenceReactance: float,
                 zeroSequenceResistance: float,
                 negativeSequenceResistance: float,
                 directAxisSynchronousReactance: float,
                 directAxisTransientReactance: float,
                 directAxisSubtransientReactance: float,
                 quadratureAxisSynchronousReactance: float,
                 quadratureAxisTransientReactance: float,
                 quadratureAxisSubtransientReactance: float,
                 directAxisTransientShortCircuitTimeConstant: float,
                 directAxisSubtransientShortCircuitTimeConstant: float,
                 directAxisTransientOpenCircuitTimeConstant: float,
                 directAxisSubtransientOpenCircuitTimeConstant: float,
                 quadratureAxisTransientShortCircuitTimeConstant: float,
                 quadratureAxisSubtransientShortCircuitTimeConstant: float,
                 quadratureAxisTransientOpenCircuitTimeConstant: float,
                 quadratureAxisSubtransientOpenCircuitTimeConstant: float
                 ):
        self.self = self
        self.statorResistancePerPhase = statorResistancePerPhase
        self.statorLeakageReactance = statorLeakageReactance
        self.zeroSequenceReactance = zeroSequenceReactance
        self.negativeSequenceReactance = negativeSequenceReactance
        self.zeroSequenceResistance = zeroSequenceResistance
        self.negativeSequenceResistance = negativeSequenceResistance
        self.directAxisSynchronousReactance = directAxisSynchronousReactance
        self.directAxisTransientReactance = directAxisTransientReactance
        self.directAxisSubtransientReactance = directAxisSubtransientReactance
        self.quadratureAxisSynchronousReactance = quadratureAxisSynchronousReactance
        self.quadratureAxisTransientReactance = quadratureAxisTransientReactance
        self.quadratureAxisSubtransientReactance = quadratureAxisSubtransientReactance
        self.directAxisTransientShortCircuitTimeConstant = directAxisTransientShortCircuitTimeConstant
        self.directAxisSubtransientShortCircuitTimeConstant = directAxisSubtransientShortCircuitTimeConstant
        self.directAxisTransientOpenCircuitTimeConstant = directAxisTransientOpenCircuitTimeConstant
        self.directAxisSubtransientOpenCircuitTimeConstant = directAxisSubtransientOpenCircuitTimeConstant
        self.quadratureAxisTransientShortCircuitTimeConstant = quadratureAxisTransientShortCircuitTimeConstant
        self.quadratureAxisSubtransientShortCircuitTimeConstant = quadratureAxisSubtransientShortCircuitTimeConstant
        self.quadratureAxisTransientOpenCircuitTimeConstant = quadratureAxisTransientOpenCircuitTimeConstant
        self.quadratureAxisSubtransientOpenCircuitTimeConstant = quadratureAxisSubtransientOpenCircuitTimeConstant


class TopicList:
    def __init__(self):
        self.self = self
        self.sequence = {"topics":[]}
        self.MAX_NUM = 64

    def addName(self, name: str):
        if len(self.sequence) == self.MAX_NUM:
            raise OverflowError
        else:
            self.sequence.append(name)


class ControlHardwareInfo:
    def __init(self, hasRealtimeClock: bool, minTemperature: float, maxTemperature: float, numNetworkPorts: int):
        self.self = self
        self.hasRealtimeClock = hasRealtimeClock
        self.minTemperature = minTemperature
        self.maxTemperature = maxTemperature
        self.numNetworkPorts = numNetworkPorts


class PowerHardwareInfo:
    def __init__(self, engine: EngineInfo = None, fuel: FuelInfo = None, generator: GeneratorInfo = None,
                 energyStorage: EnergyStorageInfo = None, powerElectronics: PowerElectronicsInfo = None,
                 thermal: ThermalInfo = None, synchronousMachineModel: SynchronousMachineCoefficients = None):
        self.self = self
        self.engine = engine
        self.fuel = fuel
        self.generator = generator
        self.energyStorage = energyStorage
        self.powerElectronics = powerElectronics
        self.thermal = thermal
        self.synchronousMachineModel = synchronousMachineModel


class EnumLabelSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def __append__(self, label: str):
        if len(label) > 32:
            raise ValueError
        if len(self.sequence >= 128):
            raise ValueError
        else:
            self.sequence.append(label)


class ParameterMetadata:
    def __init__(self, name: str, units: str, nominalMinValue: float, hardMinValue: float, nominalMaxValue: float,
                 hardMaxValue: float, resolution: float, enumLabels: EnumLabelSequence):
        self.self = self
        self.name = name
        self.units = units
        self.nominalMinValue = nominalMinValue
        self.hardMinValue = hardMinValue
        self.nominalMaxValue = nominalMaxValue
        self.hardMaxValue = hardMaxValue
        self.resolution = resolution
        self.enumLabels = enumLabels


class ParameterMetadataSequence:
    def __init__(self, parameterMetadata: ParameterMetadata):
        self.self = self
        self.sequence = [parameterMetadata]

    def addMetadata(self, parameterMetadata: ParameterMetadata):
        self.sequence.append(parameterMetadata)


class PowerPortNumber:
    def __init__(self, maxPorts: int, invalidPortNumber: int):
        self.self = self
        self.maxPorts = maxPorts
        self.invalidPortNumber = invalidPortNumber


class PowerPortNumberSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def add_PPN(self, ppn: PowerPortNumber):
        self.sequence.append(ppn)


class PowerConnectorFeatureSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def add_PCF(self, pcf: ec.PowerConnectorFeature):
        self.sequence.append(pcf)


class PowerConnectorInfo:
    def __init__(self, features: PowerConnectorFeatureSequence, physicalType: ec.PowerConnectorType,
                 polarity: ec.PowerConnectorPolarity):
        self.self = self
        self.features = features
        self.physicalType = physicalType
        self.polarity = polarity


class PowerSwitchFeatureSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def add_PSF(self, psf: ec.PowerSwitchFeature):
        self.sequence.append(psf)


class PowerSwitchInfo:
    def __init__(self, features: PowerSwitchFeatureSequence, interruptAmperage: float):
        self.self = self
        self.features = features
        self.interruptAmperage = interruptAmperage


class PowerPortInfo:
    def __init__(self, portNumber: PowerPortNumber, wiring: ec.CircuitWiring,
                 directionality: ec.PowerPortDirectionality, hasSwitch: bool, hasExternalMeter: bool,
                 hasInternalMeter: bool, hasSummaryMeasurementUpdate: bool, minAmperage: float, maxAmperage: float,
                 shortCircuitAmperage: float, minVoltage: float, maxVoltage: float, connectorInfo: PowerConnectorInfo,
                 minFrequency: float = None, maxFrequency: float = None, switchInfo: PowerSwitchInfo = None):
        self.self = self
        self.portNumber = portNumber
        self.wiring = wiring
        self.directionality = directionality
        self.hasSwitch = hasSwitch
        self.hasExternalMeter = hasExternalMeter
        self.hasInternalMeter = hasInternalMeter
        self.hasSummaryMeasurementUpdate = hasSummaryMeasurementUpdate
        self.minAmperage = minAmperage
        self.maxAmperage = maxAmperage
        self.shortCircuitAmperage = shortCircuitAmperage
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.connectorInfo = connectorInfo
        self.minFrequency = minFrequency
        self.maxFrequency = maxFrequency
        self.switchInfo = switchInfo


class PowerPortInfoSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def add_PPF(self, ppf: PowerPortInfo):
        self.sequence.append(ppf)


class GroundingInfo:
    def __init__(self, groundingNumber: (int, int), groundType: ec.GroundingDesignType,
                 protectedPorts: PowerPortNumberSequence, controlSwitchFeatures: PowerSwitchFeatureSequence,
                 pulseSwitchFeatures: PowerSwitchFeatureSequence):
        self.self = self
        self.groundingNumber = groundingNumber
        self.groundType = groundType
        self.protectedPorts = protectedPorts
        self.controlSwitchFeatures = controlSwitchFeatures,
        self.pulseSwitchFeatures = pulseSwitchFeatures


class GroundingInfoSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def add_GI(self, gi: GroundingInfo):
        self.sequence.append(gi)


class MicrogridDashboardFeatureSequence:
    def __init__(self):
        self.self = self
        self.sequence = []

    def __append__(self, feature: ec.MicrogridControllerFeature):
        if len(self.sequence) >= 3:
            raise ValueError
        self.sequence.append(feature)


class MicrogridDashboardInfo:
    def __init__(self, features: MicrogridDashboardFeatureSequence):
        self.self = self
        self.sequence = features


class MicrogridControllerFeatureSequence:
    def __init__(self):
        self.self = self
        self.sequence = []
        self.MAX_NUM = 3

    def addMCF(self, mcf: ec.MicrogridControllerFeature):
        if len(self.sequence) == self.MAX_NUM:
            raise OverflowError
        else:
            self.sequence.append(mcf)


class ControllerServiceInfo:
    def __init__(self, features: MicrogridControllerFeatureSequence):
        self.self = self
        self.features = features


class MicrogridControllerInfo:
    def __init__(self, features: MicrogridControllerFeatureSequence):
        self.self = self
        self.sequence = features


class ConversionFeatureSequence:
    def __init__(self):
        self.self = self
        self.sequence = []
        self.MAX_NUM_FEATURES = 3

    def addCF(self, cf):
        if len(self.sequence) == self.MAX_NUM_FEATURES:
            raise OverflowError
        else:
            self.sequence.append(cf)


class LoadStepResponse:
    def __init__(self, loadStepLowRealPower: float, loadStepHighRealPower: float, loadStepLowReactivePower: float,
                 loadStepHighReactivePower: float, loadAcceptanceFrequency: Curve2D, loadAcceptanceVoltage: Curve2D,
                 loadAcceptanceRealPower: Curve2D, loadAcceptanceReactivePower: Curve2D,
                 loadRejectionFrequency: Curve2D,
                 loadRejectionVoltage: Curve2D, loadRejectionRealPower: Curve2D, loadRejectionReactivePower: Curve2D):
        self.self = self
        self.loadStepLowRealPower = loadStepLowRealPower
        self.loadStepHighRealPower = loadStepHighRealPower
        self.loadStepLowReactivePower = loadStepLowReactivePower
        self.loadStepHighReactivePower = loadStepHighReactivePower
        self.loadAcceptanceFrequency = loadAcceptanceFrequency
        self.loadAcceptanceVoltage = loadAcceptanceVoltage
        self.loadAcceptanceRealPower = loadAcceptanceRealPower
        self.loadAcceptanceReactivePower = loadAcceptanceReactivePower
        self.loadRejectionFrequency = loadRejectionFrequency
        self.loadRejectionVoltage = loadRejectionVoltage
        self.loadRejectionRealPower = loadRejectionRealPower
        self.loadRejectionReactivePower = loadRejectionReactivePower


class LoadStepResponseSequence:
    def __init__(self):
        self.self = self
        self.sequence = []
        self.MAX_NUM = 16

    def addLSR(self, lsr):
        if len(self.sequence) == self.MAX_NUM:
            raise OverflowError
        else:
            self.sequence.append(lsr)


class LoadSharingInfo:
    def __init__(self, portNumber: PowerPortNumber, supportsDrop: bool, supportsMultiSegmentDroop: bool,
                 supportsConstantPower: bool, minRealPower: float, maxRealPower: float, minReactivePower: float,
                 maxReactivePower: float, maxApparentPower: float, powerFactor: float,
                 maxOverloadRealPower: Curve2D = None, loadResponse: LoadStepResponseSequence = None):
        self.self = self
        self.portNumber = portNumber
        self.supportsDrop = supportsDrop
        self.supportsMultiSegmentDroop = supportsMultiSegmentDroop
        self.supportsConstantPower = supportsConstantPower
        self.minRealPower = minRealPower
        self.maxRealPower = maxRealPower
        self.minReactivePower = minReactivePower
        self.maxReactivePower = maxReactivePower
        self.maxApparentPower = maxApparentPower
        self.powerFactor = powerFactor
        self.maxOverloadRealPower = maxOverloadRealPower
        self.loadResponse = loadResponse


class LoadSharingInfoSequence:
    def __init__(self, MAX_PORTS: int):
        self.self = self
        self.sequence = []
        self.MAX_PORTS = MAX_PORTS

    def addLSI(self, lsi: LoadSharingInfo):
        if len(self.sequence) == self.MAX_PORTS:
            raise OverflowError
        else:
            self.sequence.append(lsi)


class ActiveConversionInfo:
    def __init__(self, loadSharing: LoadSharingInfoSequence):
        self.self = self
        self.loadSharing = loadSharing


class ConversionTapInfo:
    def __init__(self, phaseShift: float, voltageRatio: float, tapId: int = 0):
        self.self = self
        self.phaseShift = phaseShift
        self.voltageRatio = voltageRatio
        self.tapId = tapId


class ConversionTapInfoSequence:
    def __init__(self, MAX_TAPS: int):
        self.self = self
        self.sequence = []
        self.MAX_TAPS = MAX_TAPS

    def addCTI(self, cti: ConversionTapInfo):
        if len(self.sequence) == self.MAX_TAPS:
            raise OverflowError
        else:
            self.sequence.append(cti)


class PowerPortConversionInfoSequence:
    def __init__(self, portNumber: PowerPortNumber, conversionTaps: ConversionTapInfoSequence, changeUnderLoad: bool):
        self.self = self
        self.portNumber = portNumber
        self.conversionTaps = conversionTaps
        self.changeUnderLoad = changeUnderLoad


class PassiveConversionInfo:
    def __init__(self, portConversion: PowerPortConversionInfoSequence):
        self.self = self
        self.portConversion = portConversion


class ConversionInfo:  # ConversionInfo is a optional parameter.
    def __init__(self, features: ConversionFeatureSequence, activeConversion: ActiveConversionInfo = None,
                 passiveConversion: PassiveConversionInfo = None):
        self.self = self
        self.features = features
        self.activeConversion = activeConversion
        self.passiveConverison = passiveConversion


class DistributionFeatureSequence:
    def __init__(self):
        self.self = self
        self.sequence = []
        self.MAX_NUM = 6

    def addDF(self, df: ec.DistributionFeature):
        if len(self.sequence) == self.MAX_NUM:
            raise OverflowError
        else:
            self.sequence.append(df)


class DistributionInfo:  # DistributionInfo a optional parameter.
    def __init__(self, features: DistributionFeatureSequence):
        self.self = self
        self.features = features


class SourceFeatureSequence:
    def __init__(self):
        self.self = self
        self.sequence = []
        self.MAX_NUM = 6

    def addSF(self, sf: ec.SourceFeature):
        if len(self.sequence) == self.MAX_NUM:
            raise OverflowError
        else:
            self.sequence.append(sf)


class EnergyStartStopLevelSequence:
    def __init__(self):
        self.self = self
        self.sequence = []
        self.MAX_NUM = 8

    def addESSL(self, essl: ec.EnergyStartStopLevel):
        if len(self.sequence) == self.MAX_NUM:
            raise OverflowError
        else:
            self.sequence.append(essl)


class SourceInfo:
    def __init__(self, features: SourceFeatureSequence, loadSharing: LoadSharingInfo,
                 supportedEnergyStartStopLevelSequence: EnergyStartStopLevelSequence):
        self.self = self
        self.features = features
        self.loadSharing = loadSharing
        self.supportedEnergyStartStopLevelSequence = supportedEnergyStartStopLevelSequence


class LoadFeatureSequence:
    def __init__(self):
        self.self = self
        self.sequence = []
        self.MAX_NUM = 4

    def addLF(self, lf: ec.LoadFeature):
        if len(self.sequence) == self.MAX_NUM:
            raise OverflowError
        else:
            self.sequence.append(lf)


class LoadInfo:
    def __init__(self, features: LoadFeatureSequence, maxRealPower: float, maxReactivePower: float):
        self.self = self
        self.features = features
        self.maxRealPower = maxRealPower
        self.maxReactivePower = maxReactivePower


class StorageFeaturesSequence:
    def __init__(self):
        self.self = self
        self.sequence = []
        self.MAX_NUM = 5

    def addSF(self, sf: ec.StorageFeature):
        if len(self.sequence) == self.MAX_NUM:
            raise OverflowError
        else:
            self.sequence.append(sf)


class StorageInfo:
    def __init__(self, features: StorageFeaturesSequence, maxChargeEnergy: float, loadSharing: LoadSharingInfo,
                 supportedEnergyStartStopLevels: EnergyStartStopLevelSequence):
        self.self = self
        self.features = features
        self.maxChargeEnergy = maxChargeEnergy
        self.loadSharing = loadSharing
        self.supportedEnergyStartStopLevels = supportedEnergyStartStopLevels


class PowerDeviceInfo:
    def __init__(self, powerPorts: PowerPortInfoSequence, grounds: GroundingInfoSequence,
                 conversion: ConversionInfo = None, distribution: DistributionInfo = None, source: SourceInfo = None,
                 storage: StorageInfo = None, load: LoadInfo = None):
        self.self = self
        self.powerPorts = powerPorts
        self.grounds = grounds
        self.conversion = conversion
        self.distribution = distribution
        self.source = source
        self.storage = storage
        self.load = load


class ProductInfo:
    def __init__(self, nsn: str, gtin: str, manufacturerName: str, modelName: str, serialNumber: str,
                 softwareVersion: str, platformID: str = None):
        self.self = self
        self.nsn = nsn
        self.gtin = gtin
        self.manufacturerName = manufacturerName
        self.modelName = modelName
        self.serialNumber = serialNumber
        self.softwareVersion = softwareVersion
        self.platformID = platformID


class TopicInfo:
    def __init__(self, dataModelVersion: str, publishedConditionalTopics: TopicList, publishedOptionalTopics: TopicList,
                 supportedRequestTopics: TopicList, extensionTopics: TopicList = None):
        self.self = self
        self.dataModelVersion = dataModelVersion,
        self.publishedOptionalTopics = publishedConditionalTopics
        self.publishedOptionalTopics = publishedOptionalTopics
        self.supportedRequestTopics = supportedRequestTopics
        self.extensionTopics = extensionTopics


class DeviceInfo:
    def __init__(self, deviceID: str, role: ec.DeviceRole, product: ProductInfo, topics: TopicInfo,
                 controlHardware: ControlHardwareInfo = None, powerHardware: PowerHardwareInfo = None,
                 controlParameters: ParameterMetadataSequence = None,
                 metricParameters: ParameterMetadataSequence = None,
                 controlService: ControllerServiceInfo = None, powerDevice: PowerDeviceInfo = None):
        self.self = self
        self.deviceID = deviceID
        self.role = role
        self.product = product
        self.topics = topics
        self.controlHardware = controlHardware
        self.powerHardware = powerHardware
        self.controlParameters = controlParameters
        self.metricParameters = metricParameters
        self.controlService = controlService
        self.powerDevice = powerDevice
        self.data_points = []

    def remove_every_instance(self, point: tuple) -> None:
        """
        Removes every instance of a data point in the data list
        :param point: tuple of (x, y) form
        :return: None or TypeError
        """
        if isinstance(point, tuple):
            while point in self.data_points:
                self.data_points.remove(point)
        else:
            raise TypeError

    def clear_points(self) -> None:
        """
        Resets the data list
        :return: None
        """
        self.data_points = []

    def pop_point(self, index: int) -> tuple:
        """
        Pops a given index from the list and returns the popped value.
        :param index: int
        :return: data_values[index] or TypeError or ValueError
        """
        if isinstance(index, int) and index >= 0:
            popped_value = self.data_points[index]
            self.data_points.pop(index)
            return popped_value
        elif not isinstance(index, int):
            raise TypeError
        else:
            raise ValueError


class RequestSequence:
    def __init__(self, number: int):
        self.self = self
        self.number = number


class Reply:
    def __init__(self, requestingDeviceID, targetDeviceID, config: ec.ConfigID, portNumber: PowerPortNumber,
                 requestSequenceID: RequestSequence, status: ec.ReplyStatus):
        self.self = self
        self.requestingDeviceID = requestingDeviceID
        self.targetDeviceID = targetDeviceID
        self.config = config
        self.portNumber = portNumber
        self.requestSequenceID = requestSequenceID
        self.status = status


class Identity: # 137
    def __init__(self, identity: str):
        self.self = self
        self.identity = identity


class IdentityNicknameState:
    def __init__(self, deviceID, identityID, nickname: str):
        self.self = self
        self.deviceID = deviceID
        self.identityID = identityID
        self.nickname = nickname
