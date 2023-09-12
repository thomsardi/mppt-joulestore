# from mppt.logger import *
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from .address import *
from ..base import BaseMPPTSync, ParameterSetting, Status, MpptError, ParserSetting
import datetime
import time
from typing import List

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
        """
        self.__id = 0
        self.__batteryType = 0
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
        and self.dischargingLimitVoltage == other.dischargingLimitVoltage :
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
    
    def getListParam(self) -> list[int]:
        value : list[int] = [
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
            self.__dischargingLimitVoltage
        ]
        return value

    def setParam(self, registerList : list[int]) -> int:
        """
        Set each member parameter, only valid if the received list length is 15

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
            self.paramList = registerList
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
        list[MpptEpeverSetting] : list of MpptEpeverSetting
        """
        deviceList : list[dict] = val['device']
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
            paramList.append(p)
        return paramList

class MPPTEPVEPER(BaseMPPTSync):
    def __init__(self, port:str, baudrate:int=115200, timeout:int = 1):
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
        if input_register:
            response_register = self.client.read_input_registers(addr, length, unit=id)
        else:
            response_register = self.client.read_holding_registers(addr, length, unit=id)
        # log.debug(rr.encode())
        self.client.close()
        return response_register
    
    def checkSetting(self, newSetting : MpptEpeverSetting) -> int :
        """
        Check the equalness of MpptEpeverSetting

        Args :
        newSetting(Parameter Setting) : new parameter to be sent into mppt

        Returns :
        int : the result of comparison between new setting and old setting. return 1 if same, 0 if it is different, -1 if it is different type
        """

        oldSetting = self.getCurrentSetting(newSetting.id)
        if type(oldSetting) is not MpptEpeverSetting :
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
    
    def get_current_setting(self, id : int) -> MpptEpeverSetting :
        """
        Get current setting of mppt

        Args :
        id(int) : slave id

        Returns :
        MpptEpeverSetting : object, refer to MpptEpeverSetting for more member information
        """
        return self.getCurrentSetting(id=id)

    def change_setting(self, newSetting : MpptEpeverSetting) -> MpptError :
        """
        Change setting of mppt when detected new setting

        Args :
        newSetting(MpptEpeverSetting) : MpptEpeverSetting object

        Returns :
        MpptError : exception, refer to MpptError object for more information
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
        return 0
    
    def set_load_mode_manual(self, id : int) -> int :
        return 0

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
            arrayRatedVoltage = self.getArrayRatedVoltage(i)
            if (arrayRatedVoltage >= 0) :
                connectedIdList.append(i)
            time.sleep(0.1) #always add sleep when using modbus within for loop. without sleep, the modbus result always failed
        self.__connectedSlaveList = connectedIdList.copy()
        return connectedIdList

    def setBulkParameter(self, setting : MpptEpeverSetting) -> int:
        """
        Set Bulk Parameter, convert MpptEpeverSetting into list of integer with length of 15
        
        Args :
        setting (MpptEpeverSetting) : MpptEpeverSetting Object, refer to MpptEpeverSetting description for member information        
        """
        value : list[int] = [
            setting.batteryType,
            setting.capacity,
            setting.tempCompensation,
            setting.overvoltageDisconnect,
            setting.chargingLimitVoltage,
            setting.overvoltageReconnect,
            setting.equalizeChargingVoltage,
            setting.boostChargingVoltage,
            setting.floatChargingVoltage,
            setting.boostReconnectVoltage,
            setting.lowVoltageReconnect,
            setting.underVoltageWarningRecover,
            setting.underVoltageWarning,
            setting.lowVoltageDisconnect,
            setting.dischargingLimitVoltage
        ]

        if (len(value) == 15) :
            request = self.setRegisters(setting.id, MpptEpeverAddress.SETTING_PARAMETER[0], value)
            if (not request.isError()) :
                return 1
            else :
                return 0
        else :
            return 0

    def getArrayRatedVoltage(self, id : int) -> int :
        """
        Get array rated voltage

        Args :
        id(int) : slave id

        Returns :
        int : rated voltage of pv array
        """
        ratedVoltage = -1
        response = self.getRegisters(id, MpptEpeverAddress.ARRAY_RATED_VOLTAGE, input_register=True)
        if (not response.isError() and response is not None) :
            ratedVoltage = response.registers[0]
        return ratedVoltage

    def getPVInfo(self, id:int):
        response = self.getRegisters(id, MpptEpeverAddress.PV_INFO, input_register=True)
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
    
    def getCurrentSetting(self, id : int) -> MpptEpeverSetting :
        """
        Get current parameter setting from address 0x9000 - 0x900E

        Args :
        id (int) : slave id of target device

        Returns :
        MpptEpeverSetting : object

        """
        response = self.getRegisters(id, MpptEpeverAddress.SETTING_PARAMETER)
        if (response.isError() and response is not None) :
            # print("Response error")
            return None
        p = MpptEpeverSetting()
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
        response = self.getRegisters(id, MpptEpeverAddress.PV_INFO, input_register=True)
        if (not response.isError() and response is not None) :
            voltage = round(response.registers[0] / 100, 2)
            current = round(response.registers[1] / 100, 2)
            power = round(((response.registers[3] << 16) + response.registers[2]) / 100, 2)
        
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
        response = self.getRegisters(id, MpptEpeverAddress.HARVEST_ENERGY, input_register=True)
        return {
            'harvest_energy': {
                'value': response.registers[0],
                'satuan': '?'
            }
        }
    
    def getGeneratedEnergy(self, id: int) -> dict:
        """
        Get all generated energy info such as today, this month, and this year generated enery

        Args :
        id (int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        generatedEnergyToday = -1
        generatedEnergyThisMonth = -1
        generatedEnergyThisYear = -1
        generatedEnergyTotal = -1
        response = self.getRegisters(id, MpptEpeverAddress.GENERATED_ENERGY_INFO, input_register=True)
        if (not response.isError() and response is not None) :
            generatedEnergyToday = ((response.registers[1] << 16) + response.registers[0]) / 100
            generatedEnergyThisMonth = ((response.registers[3] << 16) + response.registers[2]) / 100
            generatedEnergyThisYear = ((response.registers[5] << 16) + response.registers[4]) / 100
            generatedEnergyTotal = ((response.registers[7] << 16) + response.registers[6]) / 100

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
    
    def setLoadOn(self, id : int) -> int :
        """
        Set load on

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.LOAD_MANUAL_CONTROL[0], 1, unit=id)
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
        request = self.client.write_coil(MpptEpeverAddress.LOAD_MANUAL_CONTROL[0], 0, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setChargeOn(self, id : int) -> int :
        """
        Set charge on

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.CHARGING_SET[0], 1, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setChargeOff(self, id : int) -> int :
        """
        Set charge off

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.CHARGING_SET[0], 0, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setOutputManualMode(self, id : int) -> int :
        """
        Set output mode into manual

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.OUTPUT_CONTROL_MODE[0], 1, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setOutputAutoMode(self, id : int) -> int :
        """
        Set output mode into auto

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.OUTPUT_CONTROL_MODE[0], 0, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setDefaultLoadOn(self, id : int) -> int :
        """
        Set default state of load to on. load will normally on when the mppt turn on

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.DEFAULT_LOAD_STATE[0], 1, unit=id)
        if (request.isError()) :
            return 0
        return 1
    
    def setDefaultLoadOff(self, id : int) -> int :
        """
        Set default state of load to off. load will normally off when the mppt turn on

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.DEFAULT_LOAD_STATE[0], 0, unit=id)
        if (request.isError()) :
            return 0
        return 1

    def settingParameter(self, id ,val = [0, 832,300, 5570, 5520, 5370, 5470, 5470, 5470, 5370, 4950, 4900, 4800, 4700, 4600]):
        request = self.setRegisters(id, MpptEpeverAddress.SETTING_PARAMETER[0], val)
        return request

    def setLoadMode(self, id:int, val:int) -> int:
        return 0

    def setMode(self, id, val=[4,]):
        request =self.setRegisters(id, MpptEpeverAddress.MODE[0], val)
        return request

    def setDateTime(self, id, dt=None):
        if dt is None:
            waktu = datetime.datetime.now()
        else:
            waktu = dt
        raw_menit =  waktu.minute
        raw_detik = waktu.second
        hasil1 = raw_menit*256 + raw_detik

        raw_jam = waktu.hour
        raw_hari = waktu.day
        hasil2 = raw_hari *256 + raw_jam

        raw_bulan = waktu.month
        raw_tahun = int(str(waktu.year)[-2:])
        hasil3 = raw_tahun *256 + raw_bulan

        request = self.setRegisters(id, MpptEpeverAddress.DATETIME_ADDR[0], val=[hasil1,hasil2,hasil3])
        return request

    def getSettingParam(self, id):
        response = self.getRegisters(id, MpptEpeverAddress.SETTING_PARAMETER)
        return response.registers

    def getBattVoltage(self, id: int):
        response = self.getRegisters(id, MpptEpeverAddress.BATT_VOLTAGE, input_register=True)
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
        response = self.getRegisters(id, MpptEpeverAddress.BATTERY_INFO, input_register=True)
        batteryVoltage = -1
        batteryCurrent = -1
        if (not response.isError() and response is not None) :
            batteryVoltage = round(response.registers[0] / 100, 2)
            batteryCurrent = round((((response.registers[2] << 16) + response.registers[1]) / 100) , 2)

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
        response = self.getRegisters(id, MpptEpeverAddress.LOAD_INFO, input_register=True)
        loadVoltage = -1
        loadCurrent = -1
        loadPower = -1
        if (not response.isError() and response is not None) :
            loadVoltage = round(response.registers[0] / 100, 2)
            loadCurrent = round(response.registers[1] / 100, 2)
            loadPower = round((((response.registers[3] << 16) + response.registers[2]) / 100) , 2)

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
        response = self.getRegisters(id, MpptEpeverAddress.BATTERY_SOC, input_register=True)
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
    
    def getTemperatureInfo(self, id : int) -> dict :
        """
        Get temperature info such as battery temperature & device temperature

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getRegisters(id, MpptEpeverAddress.TEMPERATURE_INFO, input_register=True)
        batteryTemperature = -1
        deviceTemperature = -1
        if (not response.isError() and response is not None) :
            batteryTemperature = round(response.registers[0] / 100, 2)
            deviceTemperature = round(response.registers[1] / 100, 2)
        
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
        """
        Get status info such as battery status, charging status and discharging status

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getRegisters(id, MpptEpeverAddress.STATUS_INFO, input_register=True)
        s = Status()
        batteryStatus = -1
        chargingStatus = -1
        dischargingStatus = -1
        if (not response.isError() and response is not None) :
            batteryStatus = response.registers[0]
            batteryStatusDict = s.unpackBatteryStatus(batteryStatus)
            chargingStatus = response.registers[1]
            chargingStatusDict = s.unpackChargingStatus(chargingStatus)
            dischargingStatus = response.registers[2]
            dischargingStatusDict = s.unpackDischargingStatus(dischargingStatus)
        
            result = {
                'battery_status' : batteryStatusDict,
                'charging_status' : chargingStatusDict,
                'discharging_status' : dischargingStatusDict
            }
            return result
        else :
            return None
        
    def getDischargingState(self, id : int) -> int :
        """
        Get discharging state

        Args : 
        id(int) : slave id of target device

        Returns :
        int : 1 is running, 0 is standby
        """
        response = self.getRegisters(id, MpptEpeverAddress.STATUS_INFO, input_register=True)
        s = Status()
        batteryStatus = -1
        chargingStatus = -1
        dischargingStatus = -1
        if (not response.isError() and response is not None) :
            batteryStatus = response.registers[0]
            s.unpackBatteryStatus(batteryStatus)
            chargingStatus = response.registers[1]
            s.unpackChargingStatus(chargingStatus)
            dischargingStatus = response.registers[2]
            s.unpackDischargingStatus(dischargingStatus)
            result = s.dischargingStatus.dischargingState 
            return result
        else :
            return -1
        
    def getChargingState(self, id : int) -> int :
        """
        Get charging state

        Args : 
        id(int) : slave id of target device

        Returns :
        int : 1 is running, 0 is standby
        """
        response = self.getRegisters(id, MpptEpeverAddress.STATUS_INFO, input_register=True)
        s = Status()
        batteryStatus = -1
        chargingStatus = -1
        dischargingStatus = -1
        if (not response.isError() and response is not None) :
            batteryStatus = response.registers[0]
            s.unpackBatteryStatus(batteryStatus)
            chargingStatus = response.registers[1]
            s.unpackChargingStatus(chargingStatus)
            dischargingStatus = response.registers[2]
            s.unpackDischargingStatus(dischargingStatus)
            result = s.chargingStatus.chargingState 
            return result
        else :
            return -1
        
    def getRatedChargingCurrent(self, id : int) -> dict :
        """
        Get rated charging current

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getRegisters(id, MpptEpeverAddress.RATED_CHARGING_CURRENT, input_register=True)
        chargingCurrent = -1
        if (not response.isError() and response is not None) :
            chargingCurrent = round(response.registers[0] / 100, 2)
        
        result = {
            'rated_charging_current': {
                'value': chargingCurrent,
                'satuan': 'Ampere'
            }
        }
        return result
    
    def getRatedLoadCurrent(self, id : int) -> dict :
        """
        Get rated load current

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getRegisters(id, MpptEpeverAddress.RATED_LOAD_CURRENT, input_register=True)
        loadCurrent = -1
        if (not response.isError() and response is not None) :
            loadCurrent = round(response.registers[0] / 100, 2)
        
        result = {
            'rated_load_current': {
                'value': loadCurrent,
                'satuan': 'Ampere'
            }
        }
        return result
