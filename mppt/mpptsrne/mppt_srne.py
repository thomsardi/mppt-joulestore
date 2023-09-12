# from mppt.logger import *
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from .address import *
from ..base import BaseMPPTSync, ParameterSetting, ParserSetting
import datetime
import time
from typing import List

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
        self.__paramList : list[int] = []

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
    
    def getListParam(self) -> list[int]:
        value : list[int] = [
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

    def setParam(self, registerList : list[int]) -> int:
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
    def getParamList(self) -> list[int] :
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
        list[ParameterSetting] : list of ParameterSetting
        """
        deviceList : list[dict] = val['device']
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

class MpptSrne(BaseMPPTSync):
    def __init__(self, port:str, baudrate:int=9600, timeout:int = 1):
        super().__init__(port, baudrate, timeout=timeout)
        self.__connectedSlaveList = []

    @property
    def get_connected_slave_list(self) -> list[int] :
        return self.__connectedSlaveList.copy()

    def getRegisters(self, id:int, info:tuple, input_register=False) -> list:
        addr = info[0]
        length = info[1]
        # rr = self.client.read_holding_registers(addr, length, unit=id)
        if(not self.client.connect()) :
            print("Failed to connect")
            return None
        response_register = self.client.read_holding_registers(addr, length, unit=id)
        # log.debug(rr.encode())
        self.client.close()
        return response_register
    
    def checkSetting(self, newSetting : MpptSrneSetting) -> int :
        """
        Check the equalness of MpptSrneSetting

        Args :
        newSetting(Parameter Setting) : new parameter to be sent into mppt

        Returns :
        int : the result of comparison between new setting and old setting. return 1 if same, 0 if it is different, -1 if it is different type
        """

        oldSetting = self.getCurrentSetting(newSetting.id)
        if type(oldSetting) is not MpptSrneSetting :
            return -1
        return newSetting == oldSetting

    def scan(self, start_id : int, end_id : int) -> list[int] :
        """
        Scan for connected id

        Args :
        start_id(int) : start id to be scanned
        end_id(int) : end id to be scanned

        Returns :
        list[int] : list of connected id
        """
        return self.startScan(startId=start_id, endId=end_id)
    
    def get_pv_info(self, id:int) -> dict:
        """
        Get pv info such as voltage, current, & power

        Args :
        id(int) : slave id

        Returns :
        dict : key:value pair of pv info
        """
        return self.getAllPVInfo(id=id)

    def get_load_info(self, id:int) -> dict:
        """
        Get load info such as voltage, current, & power

        Args :
        id(int) : slave id

        Returns :
        dict : key:value pair of load info
        """
        return self.getLoadInfo(id=id)

    def get_battery_info(self, id:int) -> dict:
        """
        Get battery info such as voltage, current, & power

        Args :
        id(int) : slave id

        Returns :
        dict : key:value pair of battery info
        """
        return self.getBatteryInfo(id=id)

    def get_generated_energy(self, id : int) -> dict:
        """
        Get generated energy info for today, month and year

        Args :
        id(int) : slave id

        Returns :
        dict : key:value pair of generated energy info
        """
        return self.getGeneratedEnergy(id)

    def get_load_state(self, id : int) -> int:
        """
        Get load state

        Args :
        id(int) : slave id

        Returns :
        int : 0 load off, 1 load on
        """
        return self.getDischargingState(id)
    
    def get_load_mode(self, id : int) -> int:
        """
        Get load mode

        Args :
        id(int) : slave id

        Returns :
        int : mode 0 - 17
        """
        return self.getLoadMode(id)
    
    def get_current_setting(self, id : int) -> MpptSrneSetting :
        """
        Get current setting of mppt

        Args :
        id(int) : slave id

        Returns :
        MpptSrneSetting : object, refer to MpptSrneSetting for more member information
        """
        return self.getCurrentSetting(id=id)

    def change_setting(self, newSetting : MpptSrneSetting) -> int :
        """
        Change setting of mppt when detected new setting

        Args :
        newSetting(MpptSrneSetting) : MpptSrneSetting object

        Returns :
        int : return 1 when success, return 0 when skip writing, return -1 when modbus failed
        """
        isSame = self.checkSetting(newSetting=newSetting)
        if (isSame == 0) :
            status = self.setBulkParameter(newSetting)
            if (status) :
                return 1
            else :
                return -1
        return 0
    
    def set_load_mode_auto(self, id : int) -> int :
        """
        Set load mode to auto (17)

        Args :
        id(int) : slave id

        Returns :
        int : 1 if success, 0 if failed
        """
        return self.setLoadModeAuto(id)
    
    def set_load_mode_manual(self, id : int) -> int :
        """
        Set load mode to manual (15)

        Args :
        id(int) : slave id

        Returns :
        int : 1 if success, 0 if failed
        """
        return self.setLoadModeManual(id)
    
    def set_load_on(self, id : int) -> int :
        """
        Set load on

        Args :
        id(int) : slave id

        Returns :
        int : 1 if success, 0 if failed
        """
        return self.setLoadOn(id)
    
    def set_load_off(self, id : int) -> int :
        """
        Set load off

        Args :
        id(int) : slave id

        Returns :
        int : 1 if success, 0 if failed
        """
        return self.setLoadOff(id)

    def startScan(self, startId : int, endId : int) -> list[int] :
        """
        Scan for connected id

        Args :
        startId (int) : start id to be scanned
        endId (int) : last id to be scanned

        Returns :
        list[int] : list of connected id
        """
        connectedIdList : list[int] = []
        for i in range(startId, endId+1) :
            batterySoc = self.getBatterySocValue(i)
            if (batterySoc >= 0) :
                connectedIdList.append(i)
            time.sleep(0.1) #always add sleep when using modbus within for loop. without sleep, the modbus result always failed
        self.__connectedSlaveList = connectedIdList.copy()
        return connectedIdList

    def setBulkParameter(self, setting : MpptSrneSetting) -> int:
        """
        Set Bulk Parameter, convert MpptSrneSetting into list of integer with length of 19
        
        Args :
        setting (MpptSrneSetting) : MpptSrneSetting Object, refer to MpptSrneSetting description for member information        
        """
        value : list[int] = [
            setting.capacity,
            setting.systemVoltage,
            setting.batteryType,
            setting.overvoltageThreshold,
            setting.chargingLimitVoltage,
            setting.equalizeChargingVoltage,
            setting.boostChargingVoltage,
            setting.floatChargingVoltage,
            setting.boostReconnectVoltage,
            setting.overdischargeRecoveryVoltage,
            setting.underVoltageWarning,
            setting.overdischargeVoltage,
            setting.dischargingLimitVoltage,
            setting.chargeDischargeSoc,
            setting.overdischargeTimeDelay,
            setting.equalizingChargingTime,
            setting.boostChargingTime,
            setting.equalizingChargingInterval,
            setting.tempCompensation
        ]

        if (len(value) == 19) :
            request = self.setRegisters(setting.id, MpptSrneAddress.SETTING_PARAMETER[0], value)
            if (not request.isError()) :
                return 1
            else :
                return 0
        else :
            return 0

    def getPVInfo(self, id:int):
        response = self.getRegisters(id, MpptSrneAddress.PV_INFO)
        return {
            'pv_voltage': {
                'value': response.registers[0] * 0.01,
                'satuan': 'Volt'
            },
            'pv_current': {
                'value': response.registers[1] * 0.01,
                'satuan': 'Ampere'
            }
        }
    
    def getCurrentSetting(self, id : int) -> MpptSrneSetting :
        """
        Get current parameter setting from address 0xe002 - 0xe014

        Args :
        id (int) : slave id of target device

        Returns :
        MpptSrneSetting : object

        """
        response = self.getRegisters(id, MpptSrneAddress.SETTING_PARAMETER)
        if (response.isError() and response is not None) :
            # print("Response error")
            return None
        p = MpptSrneSetting()
        if (not p.setParam(response.registers)) :
            print("Failed to set parameter")
            return None
        p.id = id
        return p

    def getAllPVInfo(self, id:int) -> dict:
        """
        Get all PV info such as voltage, current and power

        Args :
        id (int) : slave id of the target device

        Returns :
        dict : dictionary with key:value pair
        """
        voltage = -1
        current = -1
        power = -1
        response = self.getRegisters(id, MpptSrneAddress.PV_INFO, input_register=True)
        if (not response.isError() and response is not None) :
            voltage = round(response.registers[0] / 10, 2)
            current = round(response.registers[1] / 100, 2)
            power = response.registers[2]
        
        result = {
            'pv_voltage': {
                'value': voltage,
                'satuan': 'Volt'
            },
            'pv_current': {
                'value': current,
                'satuan': 'Ampere'
            },
            'pv_power' : {
                'value': power,
                'satuan': 'Watt'
            }
        }
        
        return result

    def getEnergyDay(self, id: int):
        response = self.getRegisters(id, MpptSrneAddress.HARVEST_ENERGY, input_register=True)
        return {
            'harvest_energy': {
                'value': response.registers[0],
                'satuan': '?'
            }
        }
    
    def getGeneratedEnergy(self, id: int) -> dict:
        """
        Get all generated energy info such as today, this month, and this year generated energy

        Args :
        id (int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        generatedEnergyToday = -1
        generatedEnergyThisMonth = -1
        generatedEnergyThisYear = -1
        generatedEnergyTotal = -1
        response = self.getRegisters(id, MpptSrneAddress.ENERGY_GENERATED, input_register=True)
        if (not response.isError() and response is not None) :
            generatedEnergyToday = response.registers[0]

        result = {
            'harvest_energy': {
                'value': generatedEnergyToday,
                'satuan': 'Watt'
            },
            'harvest_energy_this_month': {
                'value': generatedEnergyThisMonth,
                'satuan': 'Watt'
            },
            'harvest_energy_this_year': {
                'value': generatedEnergyThisYear,
                'satuan': 'Watt'
            },
            'harvest_energy_total': {
                'value': generatedEnergyTotal,
                'satuan': 'Watt'
            }
        }
        return result
    
    def getLoadMode(self, id : int) -> int :
        """
        Get load mode

        Args :
        id (int) : slave id of target device

        Returns :
        int : mode 0 - 17, -1 if failed
        """
        response = self.getRegisters(id, MpptSrneAddress.LOAD_MODE)
        if (not response.isError() and response is not None) :
            return response.registers[0]
        return -1
    
    def setLoadOn(self, id : int) -> int :
        """
        Set load on

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_register(MpptSrneAddress.LOAD_COMMAND[0], 1, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setLoadOff(self, id : int) -> int :
        """
        Set load off

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_register(MpptSrneAddress.LOAD_COMMAND[0], 0, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setChargeOn(self, id : int) -> int :
        return NotImplemented
    
    def setChargeOff(self, id : int) -> int :
        return NotImplemented
    
    def setOutputManualMode(self, id : int) -> int :
        return NotImplemented
    
    def setOutputAutoMode(self, id : int) -> int :
        return NotImplemented
    
    def setDefaultLoadOn(self, id : int) -> int :
        return NotImplemented
    
    def setDefaultLoadOff(self, id : int) -> int :
        return NotImplemented

    def settingParameter(self, id ,val = [0, 832,300, 5570, 5520, 5370, 5470, 5470, 5470, 5370, 4950, 4900, 4800, 4700, 4600]):
        request = self.setRegisters(id, MpptSrneAddress.SETTING_PARAMETER[0], val)
        return request

    def setLoadModeAuto(self, id):
        request =self.client.write_register(MpptSrneAddress.LOAD_MODE[0], 17, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setLoadModeManual(self, id):
        request =self.client.write_register(MpptSrneAddress.LOAD_MODE[0], 15, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setLoadMode(self, id:int, val:int):
        request =self.client.write_register(MpptSrneAddress.LOAD_MODE[0], val, unit=id)
        if (request.isError()) :
            return 0
        return 1

    def setDateTime(self, id, dt=None):
        return NotImplemented

    def getSettingParam(self, id):
        response = self.getRegisters(id, MpptSrneAddress.SETTING_PARAMETER)
        return response.registers

    def getBattVoltage(self, id: int):
        response = self.getRegisters(id, MpptSrneAddress.BATTERY_INFO, input_register=True)
        return {
            'battery_voltage': {
                'value': round((response.registers[0]* 0.01), 2),
                'satuan': 'Volt'
            }
        }
    
    def getBatteryInfo(self, id : int) -> dict:
        """
        Get battery info such as battery voltage & current

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getRegisters(id, MpptSrneAddress.BATTERY_INFO, input_register=True)
        batteryVoltage = -1
        batteryCurrent = -1
        if (not response.isError() and response is not None) :
            batteryVoltage = round(response.registers[0] / 10, 2)
            batteryCurrent = round(response.registers[1] / 100 , 2)

        result = {
            'battery_voltage': {
                'value': batteryVoltage,
                'satuan': 'Volt'
            },
            'battery_current': {
                'value': batteryCurrent,
                'satuan': 'Ampere'
            }
        }
        return result
    
    def getLoadInfo(self, id : int) -> dict :
        """
        Get load info such as load voltage, current & power

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getRegisters(id, MpptSrneAddress.LOAD_INFO, input_register=True)
        loadVoltage = -1
        loadCurrent = -1
        loadPower = -1
        if (not response.isError() and response is not None) :
            loadVoltage = round(response.registers[0] / 10, 2)
            loadCurrent = round(response.registers[1] / 100, 2)
            loadPower = response.registers[2]

        result = {
            'load_voltage': {
                'value': loadVoltage,
                'satuan': 'Volt'
            },
            'load_current': {
                'value': loadCurrent,
                'satuan': 'Ampere'
            },
            'load_power': {
                'value': loadPower,
                'satuan': 'Watt'
            }
        }

        return result
    
    def getBatterySoc(self, id : int) -> dict :
        """
        Get battery SoC

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getRegisters(id, MpptSrneAddress.BATTERY_SOC, input_register=True)
        soc = -1
        if (not response.isError() and response is not None) :
            soc = response.registers[0]
        
        result = {
            'battery_soc': {
                'value': soc,
                'satuan': '%'
            }
        }

        return result
    
    def getBatterySocValue(self, id : int) -> int :
        """
        Get battery SoC

        Args : 
        id(int) : slave id of target device

        Returns :
        int : battery soc in %
        """
        response = self.getRegisters(id, MpptSrneAddress.BATTERY_SOC, input_register=True)
        soc = -1
        if (not response.isError() and response is not None) :
            soc = response.registers[0]

        return soc

    def getTemperatureInfo(self, id : int) -> dict :
        """
        Get temperature info such as battery temperature & device temperature

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getRegisters(id, MpptSrneAddress.TEMPERATURE_INFO)
        batteryTemperature = -1
        deviceTemperature = -1
        if (not response.isError() and response is not None) :
            deviceTemperature = response.registers[0] >> 8
            batteryTemperature = response.registers[0] & 0xff
        
        result = {
            'battery_temperature': {
                'value': batteryTemperature,
                'satuan': 'Celsius'
            },
            'device_temperature': {
                'value': deviceTemperature,
                'satuan': 'Celsius'
            }
        }

        return result
    
    def getStatusInfo(self, id : int) -> dict :
        return NotImplemented
        
    def getDischargingState(self, id : int) -> int :
        """
        Get discharging state

        Args : 
        id(int) : slave id of target device

        Returns :
        int : 1 is running, 0 is standby
        """
        response = self.getRegisters(id, MpptSrneAddress.LOAD_STATUS, input_register=True)
        if (not response.isError() and response is not None) :
            result = response.registers[0] >> 15
            return result
        else :
            return -1
        
    def getChargingState(self, id : int) -> int :
        return NotImplemented
        
    def getRatedChargingCurrent(self, id : int) -> dict :
        return NotImplemented
    
    def getRatedLoadCurrent(self, id : int) -> dict :
        return NotImplemented
