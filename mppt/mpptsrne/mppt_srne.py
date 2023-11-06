from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient, BaseModbusClient
from .address import *
from ..base import BaseMPPTSync, Status
import time
from typing import List
from .mppt_srne_utils import *

class BaseMpptSrne(BaseMPPTSync):
    def __init__(self):
        super().__init__()
        self.__connectedSlaveList = []
        self.client : BaseModbusClient = None

    @property
    def get_connected_slave_list(self) -> List[int] :
        return self.__connectedSlaveList.copy()

    def getHoldingRegisters(self, id:int, info:tuple) -> list:
        addr = info[0]
        length = info[1]
        # rr = self.client.read_holding_registers(addr, length, unit=id)
        if(not self.client.connect()) :
            print("Failed to connect")
            return None
        response_register = self.client.read_holding_registers(addr, length, unit=id)
        self.client.close()
        return response_register
    
    def getInputRegisters(self, id:int, info:tuple) -> list:
        addr = info[0]
        length = info[1]
        # rr = self.client.read_holding_registers(addr, length, unit=id)
        if(not self.client.connect()) :
            print("Failed to connect")
            return None
        response_register = self.client.read_input_registers(addr, length, unit=id)
        self.client.close()
        return response_register
    
    def setRegisters(self, id:int, addr:int, val:list):
        if (not self.client.connect()) :
            return None
        request = self.client.write_registers(addr, val, unit=id)
        self.client.close()
        return request
    
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

    def scan(self, start_id : int, end_id : int) -> List[int] :
        """
        Scan for connected id

        Args :
        start_id(int) : start id to be scanned
        end_id(int) : end id to be scanned

        Returns :
        List[int] : list of connected id
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
    
    def get_status_info(self, id : int) -> dict:
        return self.getStatusInfo(id)
    
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

    def startScan(self, startId : int, endId : int) -> List[int] :
        """
        Scan for connected id

        Args :
        startId (int) : start id to be scanned
        endId (int) : last id to be scanned

        Returns :
        List[int] : list of connected id
        """
        connectedIdList : List[int] = []
        for i in range(startId, endId+1) :
            batterySoc = self.getBatterySocValue(i)
            if batterySoc is None :
                time.sleep(0.1)
                continue
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
        value : List[int] = [
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
            if (request is None) :
                return 0
            if (not request.isError()) :
                return 1
            else :
                return 0
        else :
            return 0
    
    def getCurrentSetting(self, id : int) -> MpptSrneSetting :
        """
        Get current parameter setting from address 0xe002 - 0xe014

        Args :
        id (int) : slave id of target device

        Returns :
        MpptSrneSetting : object

        """
        response = self.getHoldingRegisters(id, MpptSrneAddress.SETTING_PARAMETER)
        p = MpptSrneSetting()

        if (response is None) : 
            return None
        if (response.isError()) :
            return None
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
        response = self.getHoldingRegisters(id, MpptSrneAddress.PV_INFO)
        if (response is not None) :
            if (not response.isError()) :
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
        response = self.getHoldingRegisters(id, MpptSrneAddress.ENERGY_GENERATED)
        if (response is not None) :
            if (not response.isError()) :
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
        response = self.getHoldingRegisters(id, MpptSrneAddress.LOAD_MODE)
        if (response is not None) :
            if (not response.isError()) :
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
        if (request is None) :
            return 0
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
        if (request is None) :
            return 0
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

    def setLoadModeAuto(self, id):
        request =self.client.write_register(MpptSrneAddress.LOAD_MODE[0], 17, unit=id)
        if (request is None) :
            return 0
        if (request.isError()) :
            return 0
        return 1
    
    def setLoadModeManual(self, id):
        request =self.client.write_register(MpptSrneAddress.LOAD_MODE[0], 15, unit=id)
        if (request is None) :
            return 0
        if (request.isError()) :
            return 0
        return 1
    
    def setLoadMode(self, id:int, val:int):
        request =self.client.write_register(MpptSrneAddress.LOAD_MODE[0], val, unit=id)
        if (request is None) :
            return 0
        if (request.isError()) :
            return 0
        return 1

    def setDateTime(self, id, dt=None):
        return NotImplemented

    def getSettingParam(self, id):
        response = self.getHoldingRegisters(id, MpptSrneAddress.SETTING_PARAMETER)
        if (response is not None) :
            if (not response.isError()) :
                return response.registers
        return None
    
    def getBatteryInfo(self, id : int) -> dict:
        """
        Get battery info such as battery voltage & current

        Args : 
        id(int) : slave id of target device

        Returns :
        dict : dictionary with key:value pair
        """
        response = self.getHoldingRegisters(id, MpptSrneAddress.BATTERY_INFO)
        batteryVoltage = -1
        batteryCurrent = -1
        if (response is not None) :
            if (not response.isError()) :
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
        response = self.getHoldingRegisters(id, MpptSrneAddress.LOAD_INFO)
        loadVoltage = -1
        loadCurrent = -1
        loadPower = -1
        if (response is not None) :
            if (not response.isError()) :
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
        response = self.getHoldingRegisters(id, MpptSrneAddress.BATTERY_SOC)
        soc = -1
        if (response is not None) :
            if (not response.isError()) :
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
        response = self.getHoldingRegisters(id, MpptSrneAddress.BATTERY_SOC)
        soc = -1
        if (response is None) :
            return None
        if (not response.isError()) :
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
        response = self.getHoldingRegisters(id, MpptSrneAddress.TEMPERATURE_INFO)
        batteryTemperature = -1
        deviceTemperature = -1
        if (response is not None) :
            if (not response.isError()) :
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
        stats = Status()
        response = self.getHoldingRegisters(id, MpptSrneAddress.FAULT_INFO)
        result = 0
        hiReg = 0
        lowReg = 0
        if (response is not None) :
            if (not response.isError()) :
                hiReg = response.registers[0]
                lowReg = response.registers[1]
                result = 1
        
        result = {
            'result' : result,
            'fault': {
                'batt_overdisc': stats.extractBit(lowReg, 0),
                'batt_overvolt' : stats.extractBit(lowReg, 1),
                'batt_undervolt' : stats.extractBit(lowReg, 2),
                'load_short' : stats.extractBit(lowReg, 3),
                'load_over_current_power' : stats.extractBit(lowReg, 4),
                'controller_temp_high' : stats.extractBit(lowReg, 5),
                'batt_hi_temp_protection_1' : stats.extractBit(lowReg, 6),
                'pv_input_overpower' : stats.extractBit(lowReg, 7),
                'pv_input_overvolt' : stats.extractBit(lowReg, 9),
                'solar_panel_working_point_overvolt' : stats.extractBit(lowReg, 11),
                'solar_panel_reversed' : stats.extractBit(lowReg, 12),
                'power_supply_status' : stats.extractBit(hiReg, 6),
                'oo_battery_detected_sld' : stats.extractBit(hiReg, 7),
                'batt_hi_temp_protection_2' : stats.extractBit(hiReg, 8),
                'batt_lo_temp_protection_1' : stats.extractBit(hiReg, 9),
                'overcharge_protection' : stats.extractBit(hiReg, 10),
                'batt_lo_temp_protection_2' : stats.extractBit(hiReg, 11),
                'batt_reversed' : stats.extractBit(hiReg, 12),
                'induction_probe_damaged' : stats.extractBit(hiReg, 14),
                'load_open_circuit' : stats.extractBit(hiReg, 15),
            }
        }
        return result
        
    def getDischargingState(self, id : int) -> int :
        """
        Get discharging state

        Args : 
        id(int) : slave id of target device

        Returns :
        int : 1 is running, 0 is standby
        """
        response = self.getHoldingRegisters(id, MpptSrneAddress.LOAD_STATUS)
        if (response is not None) :
            if (not response.isError()) :
                result = response.registers[0] >> 15
                return result
        return -1
        
    def getChargingState(self, id : int) -> int :
        return NotImplemented
        
    def getRatedChargingCurrent(self, id : int) -> dict :
        return NotImplemented
    
    def getRatedLoadCurrent(self, id : int) -> dict :
        return NotImplemented

class MpptSrneSerial(BaseMpptSrne):
    def __init__(self, port : str, method : str = 'rtu', baudrate : int = 9600, timeout : int = 1):
        super().__init__()
        self.__method : str = method
        self.__port : str = port
        self.__baudrate : int = baudrate
        self.__timeout : int = timeout
        self.client = ModbusSerialClient(method=method, port=port, baudrate=baudrate, timeout=timeout)
        self.modbusInit = True

    @property
    def method(self) -> str :
        return self.__method
    
    @property
    def port(self) -> str :
        return self.__port
    
    @property
    def baudrate(self) -> int :
        return self.__baudrate
    
    @property
    def timeout(self) -> int :
        return self.__timeout
    
    def begin(self, port : str, method : str = 'rtu', baudrate : int = 9600, timeout : int = 1) :
        self.client = ModbusSerialClient(method=method, port=port, baudrate=baudrate, timeout=timeout)

    def end(self) :
        if (self.modbusInit) :
            self.client.close()
        self.client = None
        self.modbusInit = False

class MpptSrneTCP(BaseMpptSrne):
    def __init__(self, host : str, port : int = 502, timeout : int = 1):
        super().__init__()
        self.__host : str = host
        self.__port : int = port
        self.__timeout : int = timeout
        self.client = ModbusTcpClient(host=host, port=port, timeout=timeout)
        self.modbusInit = True

    @property
    def host(self) -> str :
        return self.__host
    
    @property
    def port(self) -> int :
        return self.__port
    
    @property
    def timeout(self) -> int :
        return self.__timeout
    
    def begin(self, host : str, port : int = 502) :
        self.client = ModbusTcpClient(host=host, port=port)

    def end(self) :
        if (self.modbusInit) :
            self.client.close()
        self.client = None
        self.modbusInit = False

