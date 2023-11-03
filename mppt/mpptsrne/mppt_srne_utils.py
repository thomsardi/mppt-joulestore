from typing import List
from ..base import ParameterSetting, ParserSetting

class MpptSrneSetting(ParameterSetting) :
    """
    Parameter setting class for epever
    """
    def __init__(self) -> None:
        """
        ParameterSetting Object with each member default value :
        id : default 0
        capacity : 100 - 3000 Ah (default 56 * 16 = 896)
        systemVoltage : 12336 (Hi Byte 48V, Lo Byte 48V)
        batteryType : 0 = User, 1 = Flooded, 2 = Sealed, 3 = Gel (default 0)
        overvoltageThreshold : default 5570
        chargingLimitVoltage : default 5520
        equalizeChargingVoltage : default 5470
        boostChargingVoltage : default 5470
        floatChargingVoltage : default 5470
        boostReconnectVoltage : default 5370
        overdischargeRecoveryVoltage : default 4900
        underVoltageWarning : default 4800
        overdischargeVoltage : default 4700
        dischargingLimitVoltage : default 4600
        charge
        overdischargeTimeDelay : default 5
        equalizingChargingTime : default 0
        boostChargingTime : default 120
        equalizingChargingInterval : default 0
        tempCompensation : 0 - 5 (default 0)
        """
        super().__init__()
        self.__id = 0
        self.__capacity = 896
        self.__systemVoltage = 12336
        self.__batteryType = 0
        self.__overvoltageThreshold = 5570
        self.__chargingLimitVoltage = 5520
        self.__equalizeChargingVoltage = 5470
        self.__boostChargingVoltage = 5470
        self.__floatChargingVoltage = 5470
        self.__boostReconnectVoltage = 5370
        self.__overdischargeRecoveryVoltage = 4950
        self.__underVoltageWarning = 4800
        self.__overdischargeVoltage = 4700
        self.__dischargingLimitVoltage = 4600
        self.__chargeDischargeSoc = 25650
        self.__overdischargeTimeDelay = 5
        self.__equalizingChargingTime = 120
        self.__boostChargingTime = 120
        self.__equalizingChargingInterval = 120
        self.__tempCompensation = 0
        self.__paramList : List[int] = []

    def __eq__(self, other): 
        if not isinstance(other, MpptSrneSetting):
            # don't attempt to compare against unrelated types
            print("Error : Attempted to compare between different type, returning False")
            return NotImplemented

        if self.id == other.id \
        and self.capacity == other.capacity \
        and self.systemVoltage == other.systemVoltage \
        and self.batteryType == other.batteryType \
        and self.overvoltageThreshold == other.overvoltageThreshold \
        and self.chargingLimitVoltage == other.chargingLimitVoltage \
        and self.equalizeChargingVoltage == other.equalizeChargingVoltage \
        and self.boostChargingVoltage == other.boostChargingVoltage \
        and self.floatChargingVoltage == other.floatChargingVoltage \
        and self.boostReconnectVoltage == other.boostReconnectVoltage \
        and self.overdischargeRecoveryVoltage == other.overdischargeRecoveryVoltage \
        and self.underVoltageWarning == other.underVoltageWarning \
        and self.overdischargeVoltage == other.overdischargeVoltage \
        and self.dischargingLimitVoltage == other.dischargingLimitVoltage \
        and self.overdischargeTimeDelay == other.overdischargeTimeDelay \
        and self.equalizingChargingTime == other.equalizingChargingTime \
        and self.boostChargingTime == other.boostChargingTime \
        and self.equalizingChargingInterval == other.equalizingChargingInterval \
        and self.tempCompensation == other.tempCompensation :
            return True
        else :
            return False

    def printContainer(self) :
        """
        Print each member value
        """
        print ("Id :", self.__id)
        print ("Capacity :", self.__capacity)
        print ("System voltage :", self.__systemVoltage >> 8)
        print ("Recognized voltage :", (self.__systemVoltage & 0xff))
        print ("Battery type :", self.__batteryType)
        print ("Overvoltage threshold :", self.__overvoltageThreshold)
        print ("Charging limit voltage :", self.__chargingLimitVoltage)
        print ("Equalize charging voltage :", self.__equalizeChargingVoltage)
        print ("Boost charging voltage :", self.__boostChargingVoltage)
        print ("Float charging voltage :", self.__floatChargingVoltage)
        print ("Boost reconnect voltage :", self.__boostReconnectVoltage)
        print ("Overdischarge recovery voltage :", self.__overdischargeRecoveryVoltage)
        print ("Undervoltage warning :", self.__underVoltageWarning)
        print ("Overdischarge voltage :", self.__overdischargeVoltage)
        print ("Discharging limit voltage :", self.__dischargingLimitVoltage)
        print ("Charge discharge soc :", self.__chargeDischargeSoc)
        print ("Overdischarge time delay :", self.__overdischargeTimeDelay)
        print ("Equalizing charging time :", self.__equalizingChargingTime)
        print ("Boost charging time :", self.__boostChargingTime)
        print ("Equalizing charging interval :", self.__equalizingChargingInterval)
        print ("Temperature compensation :", self.__tempCompensation)
    
    def getListParam(self) -> List[int]:
        value : List[int] = [
            self.__id,
            self.__capacity,
            self.__systemVoltage,
            self.__batteryType,
            self.__overvoltageThreshold,
            self.__chargingLimitVoltage,
            self.__equalizeChargingVoltage,
            self.__boostChargingVoltage,
            self.__floatChargingVoltage,
            self.__boostReconnectVoltage,
            self.__overdischargeRecoveryVoltage,
            self.__underVoltageWarning,
            self.__overdischargeVoltage,
            self.__dischargingLimitVoltage,
            self.__chargeDischargeSoc,
            self.__overdischargeTimeDelay,
            self.__equalizingChargingTime,
            self.__boostChargingTime,
            self.__equalizingChargingInterval,
            self.__tempCompensation
        ]
        return value

    def setParam(self, registerList : List[int]) -> int:
        """
        Set each member parameter, only valid if the received list length is 19

        Args :
        registerList (list) : a list of integer value, received from register modbus
        """
        length = len(registerList)
        if (length == 19) :
            self.__capacity = registerList[0]
            self.__systemVoltage = registerList[1]
            self.__batteryType = registerList[2]
            self.__overvoltageThreshold = registerList[3]
            self.__chargingLimitVoltage = registerList[4]
            self.__equalizeChargingVoltage = registerList[5]
            self.__boostChargingVoltage = registerList[6]
            self.__floatChargingVoltage = registerList[7]
            self.__boostReconnectVoltage = registerList[8]
            self.__overdischargeRecoveryVoltage = registerList[9]
            self.__underVoltageWarning = registerList[10]
            self.__overdischargeVoltage = registerList[11]
            self.__dischargingLimitVoltage = registerList[12]
            self.__chargeDischargeSoc = registerList[13]
            self.__overdischargeTimeDelay = registerList[14]
            self.__equalizingChargingTime = registerList[15]
            self.__boostChargingTime = registerList[16]
            self.__equalizingChargingInterval = registerList[17]
            self.__tempCompensation = registerList[18]
            self.__paramList = registerList.copy()
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
    def systemVoltage(self) -> int :
        return self.__systemVoltage
    
    @systemVoltage.setter
    def systemVoltage(self, val : int) :
        self.__systemVoltage = val

    @property
    def tempCompensation(self) -> int :
        return self.__tempCompensation
    
    @tempCompensation.setter
    def tempCompensation(self, val : int) :
        self.__tempCompensation = val

    @property
    def overvoltageThreshold(self) -> int:
        return self.__overvoltageThreshold
    
    @overvoltageThreshold.setter
    def overvoltageThreshold(self, val : int) :
        self.__overvoltageThreshold = val

    @property
    def chargingLimitVoltage(self) -> int :
        return self.__chargingLimitVoltage
    
    @chargingLimitVoltage.setter
    def chargingLimitVoltage(self, val : int) :
        self.__chargingLimitVoltage = val

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
    def overdischargeRecoveryVoltage(self) -> int :
        return self.__overdischargeRecoveryVoltage
    
    @overdischargeRecoveryVoltage.setter
    def overdischargeRecoveryVoltage(self,val : int):
        self.__overdischargeRecoveryVoltage = val

    @property
    def underVoltageWarning(self) -> int :
        return self.__underVoltageWarning
    
    @underVoltageWarning.setter
    def underVoltageWarning(self, val : int) :
        self.__underVoltageWarning = val

    @property
    def overdischargeVoltage(self) -> int :
        return self.__overdischargeVoltage
    
    @overdischargeVoltage.setter
    def overdischargeVoltage(self, val : int) :
        self.__overdischargeVoltage = val

    @property
    def dischargingLimitVoltage(self) -> int :
        return self.__dischargingLimitVoltage
    
    @dischargingLimitVoltage.setter
    def dischargingLimitVoltage(self, val : int) :
        self.__dischargingLimitVoltage = val

    @property
    def chargeDischargeSoc(self) -> int :
        return self.__chargeDischargeSoc

    @property
    def overdischargeTimeDelay(self) -> int :
        return self.__overdischargeTimeDelay
    
    @overdischargeTimeDelay.setter
    def overdischargeTimeDelay(self, val : int) :
        self.__overdischargeTimeDelay = val

    @property
    def equalizingChargingTime(self) -> int :
        return self.__equalizingChargingTime
    
    @equalizingChargingTime.setter
    def equalizingChargingTime(self, val : int) :
        self.__equalizingChargingTime = val

    @property
    def boostChargingTime(self) -> int :
        return self.__boostChargingTime
    
    @boostChargingTime.setter
    def boostChargingTime(self, val : int) :
        self.__boostChargingTime = val

    @property
    def equalizingChargingInterval(self) -> int :
        return self.__equalizingChargingInterval
    
    @equalizingChargingInterval.setter
    def equalizingChargingInterval(self, val : int) :
        self.__equalizingChargingInterval = val

    @property
    def getParamList(self) -> List[int] :
        return self.__paramList.copy()

class SrneParserSetting(ParserSetting) :
    """
    Parser class for epever json setting
    """
    def __init__(self) -> None:
        super().__init__()

    def parse(self, val : dict) -> List[MpptSrneSetting] :
        """
        Parse json file from register_config.json into list of ParameterSetting

        Args :
        val (dict) : dictionary of register_config

        Returns :
        List[ParameterSetting] : list of ParameterSetting
        """
        deviceList : List[dict] = val['device']
        paramList : List[MpptSrneSetting] = []
        for a in deviceList :
            p = MpptSrneSetting()
            p.id = a['slave']
            p.capacity = a['parameter']['battery_capacity']
            p.systemVoltage = a['parameter']['system_voltage']
            p.batteryType = a['parameter']['battery_type']
            p.overvoltageThreshold = a['parameter']['overvoltage_threshold']
            p.chargingLimitVoltage = a['parameter']['charging_limit_voltage']
            p.equalizeChargingVoltage = a['parameter']['equalizing_charge_voltage']
            p.boostChargingVoltage = a['parameter']['boost_charging_voltage']
            p.floatChargingVoltage = a['parameter']['floating_charging_voltage']
            p.boostReconnectVoltage = a['parameter']['boost_charging_recovery_voltage']
            p.overdischargeRecoveryVoltage = a['parameter']['overdischarge_recovery_voltage']
            p.underVoltageWarning = a['parameter']['undervoltage_warning_level']
            p.overdischargeVoltage = a['parameter']['overdischarge_voltage']
            p.dischargingLimitVoltage = a['parameter']['discharging_limit_voltage']
            p.overdischargeTimeDelay = a['parameter']['overdischarge_time_delay']
            p.equalizingChargingTime = a['parameter']['equalizing_charging_time']
            p.boostChargingTime = a['parameter']['boost_charging_time']
            p.equalizingChargingInterval = a['parameter']['equalizing_charging_interval']
            p.tempCompensation = a['parameter']['temperature_comp']
            paramList.append(p)
        return paramList