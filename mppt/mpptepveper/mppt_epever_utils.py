from typing import List
from ..base import ParameterSetting, ParserSetting, BatteryType, BatteryRatedVoltage

class MpptEpeverSetting(ParameterSetting) :
    """
    Parameter setting class for epever
    """
    def __init__(self) -> None:
        """
        MpptEpeverSetting Object with each member default value :
        id : default 0
        batteryType : 0 = User, 1 = Sealed, 2 = GEL, 3 = Flooded (default 0)
        capacity : 1 - 9999 Ah (default 56 * 16 = 896)
        tempCompensation : 0 - 900 (default 300)
        overvoltagedisconnect : default 5570
        chargingLimitVoltage : default 5520
        overvoltageReconnect : default 5370
        equalizeChargingVoltage : default 5470
        boostChargingVoltage : default 5470
        floatChargingVoltage : default 5470
        boostReconnectVoltage : default 5370
        lowVoltageReconnect : default 4950
        underVoltageWarningRecover : default 4900
        underVoltageWarning : default 4800
        lowVoltageDisconnect : default 4700
        dischargingLimitVoltage : default 4600
        batteryRatedVoltage : default 4
        defaultLoadState : default 1
        equalizingDuration : default 0
        boostDuration : 120
        """
        self.__id = 0
        self.__batteryType = BatteryType.USER.value
        self.__capacity = 832
        self.__tempCompensation = 300
        self.__overvoltageDisconnect = 5570
        self.__chargingLimitVoltage = 5520
        self.__overvoltageReconnect = 5370
        self.__equalizeChargingVoltage = 5470
        self.__boostChargingVoltage = 5470
        self.__floatChargingVoltage = 5470
        self.__boostReconnectVoltage = 5370
        self.__lowVoltageReconnect = 4950
        self.__underVoltageWarningRecover = 4900
        self.__underVoltageWarning = 4800
        self.__lowVoltageDisconnect = 4700
        self.__dischargingLimitVoltage = 4600
        self.__batteryRatedVoltage = BatteryRatedVoltage.VOLTAGE_48V.value
        self.__defaultLoadState = 1
        self.__equalizingDuration = 0
        self.__boostDuration = 120
        self.paramList = [0] * 19

    def __eq__(self, other): 
        if not isinstance(other, MpptEpeverSetting):
            # don't attempt to compare against unrelated types
            print("Error : Attempted to compare between different type, returning False")
            return NotImplemented

        if self.id == other.id \
        and self.batteryType == other.batteryType \
        and self.capacity == other.capacity \
        and self.tempCompensation == other.tempCompensation \
        and self.overvoltageDisconnect == other.overvoltageDisconnect \
        and self.chargingLimitVoltage == other.chargingLimitVoltage \
        and self.overvoltageReconnect == other.overvoltageReconnect \
        and self.equalizeChargingVoltage == other.equalizeChargingVoltage \
        and self.boostChargingVoltage == other.boostChargingVoltage \
        and self.floatChargingVoltage == other.floatChargingVoltage \
        and self.boostReconnectVoltage == other.boostReconnectVoltage \
        and self.lowVoltageReconnect == other.lowVoltageReconnect \
        and self.underVoltageWarningRecover == other.underVoltageWarningRecover \
        and self.underVoltageWarning == other.underVoltageWarning \
        and self.lowVoltageDisconnect == other.lowVoltageDisconnect \
        and self.dischargingLimitVoltage == other.dischargingLimitVoltage \
        and self.batteryRatedVoltage == other.batteryRatedVoltage \
        and self.defaultLoadState == other.defaultLoadState \
        and self.equalizingDuration == other.equalizingDuration \
        and self.boostDuration == other.boostDuration :
            return True
        else :
            return False

    def printContainer(self) :
        """
        Print each member value
        """
        print ("Id :", self.__id)
        print ("Battery type :", self.__batteryType)
        print ("Capacity :", self.__capacity)
        print ("Temperature compensation :", self.__tempCompensation)
        print ("Overvoltage disconnect :", self.__overvoltageDisconnect)
        print ("Charging limit voltage :", self.__chargingLimitVoltage)
        print ("Overvoltage reconnect :", self.__overvoltageReconnect)
        print ("Equalize charging voltage :", self.__equalizeChargingVoltage)
        print ("Boost charging voltage :", self.__boostChargingVoltage)
        print ("Float charging voltage :", self.__floatChargingVoltage)
        print ("Boost reconnect voltage :", self.__boostReconnectVoltage)
        print ("Low voltage reconnect :", self.__lowVoltageReconnect)
        print ("Undervoltage warning recover :", self.__underVoltageWarningRecover)
        print ("Undervoltage warning :", self.__underVoltageWarning)
        print ("Low voltage disconnect :", self.__lowVoltageDisconnect)
        print ("Discharging limit voltage :", self.__dischargingLimitVoltage)
        print ("Battery rated voltage :", self.__batteryRatedVoltage)
        print ("Default load state :", self.__defaultLoadState)
        print ("Equalizing duration :", self.__equalizingDuration)
        print ("Boost duration :", self.__boostDuration)
    
    def getListParam(self) -> List[int]:
        value : List[int] = [
            self.__id,
            self.__batteryType,
            self.__capacity,
            self.__tempCompensation,
            self.__overvoltageDisconnect,
            self.__chargingLimitVoltage,
            self.__overvoltageReconnect,
            self.__equalizeChargingVoltage,
            self.__boostChargingVoltage,
            self.__floatChargingVoltage,
            self.__boostReconnectVoltage,
            self.__lowVoltageReconnect,
            self.__underVoltageWarningRecover,
            self.__underVoltageWarning,
            self.__lowVoltageDisconnect,
            self.__dischargingLimitVoltage,
            self.__batteryRatedVoltage,
            self.__defaultLoadState,
            self.__equalizingDuration,
            self.__boostDuration
        ]
        return value

    def setParam(self, registerList : List[int]) -> int:
        """
        Set each member parameter, only valid if the received list length is 15, 3, 1

        Args :
        registerList (list) : a list of integer value, received from register modbus
        """
        length = len(registerList)
        if (length == 15) :
            self.__batteryType = registerList[0]
            self.__capacity = registerList[1]
            self.__tempCompensation = registerList[2]
            self.__overvoltageDisconnect = registerList[3]
            self.__chargingLimitVoltage = registerList[4]
            self.__overvoltageReconnect = registerList[5]
            self.__equalizeChargingVoltage = registerList[6]
            self.__boostChargingVoltage = registerList[7]
            self.__floatChargingVoltage = registerList[8]
            self.__boostReconnectVoltage = registerList[9]
            self.__lowVoltageReconnect = registerList[10]
            self.__underVoltageWarningRecover = registerList[11]
            self.__underVoltageWarning = registerList[12]
            self.__lowVoltageDisconnect = registerList[13]
            self.__dischargingLimitVoltage = registerList[14]
            for index, val in enumerate(registerList) :
                self.paramList[index] = val
            return 1
        elif (length == 1) :
            self.paramList[15] = registerList[0]
            self.__batteryRatedVoltage = registerList[0]
            return 1
        elif (length == 3) :
            for index, val in enumerate (registerList) :
                self.paramList[index+16] = val
            self.__defaultLoadState = registerList[0]
            self.__equalizingDuration = registerList[1]
            self.__boostDuration = registerList[2]
            return 1
        return -1

    @property
    def id(self) -> int :
        return self.__id
    
    @id.setter
    def id(self, val : int) :
        self.__id = val

    @property
    def batteryType(self) -> int:
        return self.__batteryType
    
    @batteryType.setter
    def batteryType(self, val : int) :
        self.__batteryType = val

    @property
    def capacity(self) -> int :
        return self.__capacity
    
    @capacity.setter
    def capacity(self, val : int) :
        self.__capacity = val

    @property
    def tempCompensation(self) -> int :
        return self.__tempCompensation
    
    @tempCompensation.setter
    def tempCompensation(self, val : int) :
        self.__tempCompensation = val

    @property
    def overvoltageDisconnect(self) -> int:
        return self.__overvoltageDisconnect
    
    @overvoltageDisconnect.setter
    def overvoltageDisconnect(self, val : int) :
        self.__overvoltageDisconnect = val

    @property
    def chargingLimitVoltage(self) -> int :
        return self.__chargingLimitVoltage
    
    @chargingLimitVoltage.setter
    def chargingLimitVoltage(self, val : int) :
        self.__chargingLimitVoltage = val

    @property
    def overvoltageReconnect(self) -> int :
        return self.__overvoltageReconnect
    
    @overvoltageReconnect.setter
    def overvoltageReconnect(self, val : int) :
        self.__overvoltageReconnect = val

    @property
    def equalizeChargingVoltage(self) -> int:
        return self.__equalizeChargingVoltage
    
    @equalizeChargingVoltage.setter
    def equalizeChargingVoltage(self, val : int):
        self.__equalizeChargingVoltage = val

    @property
    def boostChargingVoltage(self) -> int :
        return self.__boostChargingVoltage
    
    @boostChargingVoltage.setter
    def boostChargingVoltage(self, val : int):
        self.__boostChargingVoltage = val

    @property
    def floatChargingVoltage(self) -> int :
        return self.__floatChargingVoltage
    
    @floatChargingVoltage.setter
    def floatChargingVoltage(self, val : int) :
        self.__floatChargingVoltage = val

    @property
    def boostReconnectVoltage(self) -> int :
        return self.__boostReconnectVoltage
    
    @boostReconnectVoltage.setter
    def boostReconnectVoltage(self, val : int) :
        self.__boostReconnectVoltage = val

    @property
    def lowVoltageReconnect(self) -> int :
        return self.__lowVoltageReconnect
    
    @lowVoltageReconnect.setter
    def lowVoltageReconnect(self,val : int):
        self.__lowVoltageReconnect = val

    @property
    def underVoltageWarningRecover(self) -> int :
        return self.__underVoltageWarningRecover
    
    @underVoltageWarningRecover.setter
    def underVoltageWarningRecover(self, val : int) -> int :
        self.__underVoltageWarningRecover = val

    @property
    def underVoltageWarning(self) -> int :
        return self.__underVoltageWarning
    
    @underVoltageWarning.setter
    def underVoltageWarning(self, val : int) :
        self.__underVoltageWarning = val

    @property
    def lowVoltageDisconnect(self) -> int :
        return self.__lowVoltageDisconnect
    
    @lowVoltageDisconnect.setter
    def lowVoltageDisconnect(self, val : int) :
        self.__lowVoltageDisconnect = val

    @property
    def dischargingLimitVoltage(self) -> int :
        return self.__dischargingLimitVoltage
    
    @dischargingLimitVoltage.setter
    def dischargingLimitVoltage(self, val : int) :
        self.__dischargingLimitVoltage = val

    @property
    def batteryRatedVoltage(self) -> int :
        return self.__batteryRatedVoltage
    
    @batteryRatedVoltage.setter
    def batteryRatedVoltage(self, val : int) :
        self.__batteryRatedVoltage = val

    @property
    def defaultLoadState(self) -> int :
        return self.__defaultLoadState
    
    @defaultLoadState.setter
    def defaultLoadState(self, val : int) :
        self.__defaultLoadState = val

    @property
    def equalizingDuration(self) -> int :
        return self.__equalizingDuration
    
    @equalizingDuration.setter
    def equalizingDuration(self, val : int) :
        self.__equalizingDuration = val

    @property
    def boostDuration(self) -> int :
        return self.__boostDuration
    
    @boostDuration.setter
    def boostDuration(self, val : int) :
        self.__boostDuration = val

class EpeverParserSetting(ParserSetting) :
    """
    Parser class for epever json setting
    """
    def __init__(self) -> None:
        super().__init__()

    def parse(self, val : dict) -> List[MpptEpeverSetting] :
        """
        Parse json file from register_config.json into list of MpptEpeverSetting

        Args :
        val (dict) : dictionary of register_config

        Returns :
        List[MpptEpeverSetting] : list of MpptEpeverSetting
        """
        deviceList : List[dict] = val['device']
        paramList : List[MpptEpeverSetting] = []
        for a in deviceList :
            p = MpptEpeverSetting()
            p.id = a['slave']
            p.batteryType = a['parameter']['battery_type']
            p.capacity = a['parameter']['battery_capacity']
            p.tempCompensation = a['parameter']['temperature_comp']
            p.overvoltageDisconnect = a['parameter']['overvoltage_disconnect']
            p.chargingLimitVoltage = a['parameter']['charging_limit_voltage']
            p.overvoltageReconnect = a['parameter']['overvoltage_reconnect']
            p.equalizeChargingVoltage = a['parameter']['equalize_charging_voltage']
            p.boostChargingVoltage = a['parameter']['boost_charging_voltage']
            p.floatChargingVoltage = a['parameter']['float_charging_voltage']
            p.boostReconnectVoltage = a['parameter']['boost_reconnect_charging_voltage']
            p.lowVoltageReconnect = a['parameter']['low_voltage_reconnect']
            p.underVoltageWarningRecover = a['parameter']['undervoltage_warning_recover']
            p.underVoltageWarning = a['parameter']['undervoltage_warning']
            p.lowVoltageDisconnect = a['parameter']['low_voltage_disconnect']
            p.dischargingLimitVoltage = a['parameter']['discharging_limit_voltage']
            p.batteryRatedVoltage = a['parameter']['battery_rated_voltage']
            p.defaultLoadState = a['parameter']['default_load_state']
            p.equalizingDuration = a['parameter']['equalizing_duration']
            p.boostDuration = a['parameter']['boost_duration']
            paramList.append(p)
        return paramList