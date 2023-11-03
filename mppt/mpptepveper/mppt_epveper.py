# from mppt.logger import *
from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient, BaseModbusClient
from .address import *
from ..base import BaseMPPTSync, Status, MpptError, BatteryRatedVoltage, BatteryType
import datetime
import time
from typing import List
from .mppt_epever_utils import *

class BaseMPPTEPVEPER(BaseMPPTSync):
    def __init__(self):
        super().__init__()
        self.__connectedSlaveList = []
        self.client : BaseModbusClient = None

    @property
    def get_connected_slave_list(self) -> List[int] :
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
    
    def setRegisters(self, id:int, addr:int, val:list):
        if (not self.client.connect()) :
            return None
        request = self.client.write_registers(addr, val, unit=id)
        self.client.close()
        return request

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
    
    def get_status_info(self, id : int) -> dict :
        return self.getStatusInfo(id)

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
        value : List[int] = [
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

        battType = [member.value for member in BatteryType]
        battRatedVoltage = [member.value for member in BatteryRatedVoltage]

        if setting.batteryType not in battType :
            print("invalid type")
            return 0

        if setting.batteryRatedVoltage not in battRatedVoltage :
            print("invalid rated voltage")
            return 0

        request = self.setRegisters(setting.id, MpptEpeverAddress.SETTING_PARAMETER[0], value)
        
        if (request is None) :
            return 0
        
        if (request.isError()) :
            return 0
            
        value : List[int] = [
            setting.batteryRatedVoltage
        ]

        request = self.setRegisters(setting.id, MpptEpeverAddress.BATTERY_RATED_VOLTAGE_PARAMETER[0], value)

        if (request is None) :
            return 0
        
        if (request.isError()) :
            return 0
        
        value : List[int] = [
            setting.defaultLoadState,
            setting.equalizingDuration,
            setting.boostDuration
        ]

        request = self.setRegisters(setting.id, MpptEpeverAddress.OTHER_PARAMETER[0], value)

        if (request is None) :
            return 0
        
        if (request.isError()) :
            return 0
        
        return 1

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
        if (response is not None) :
            if (not response.isError()) :
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
        p = MpptEpeverSetting()
        response = self.getRegisters(id, MpptEpeverAddress.SETTING_PARAMETER)
        
        if (response is not None) :
            if (response.isError()) :
                return None
        else :
            return None
        
        if (not p.setParam(response.registers)) :
            print("Failed to set parameter")
            return None
        
        response = self.getRegisters(id, MpptEpeverAddress.BATTERY_RATED_VOLTAGE_PARAMETER)
        
        if (response is not None) :
            if (response.isError()) :
                return None
        else :
            return None

        try :
            if (not p.setParam(response.registers)) :
                print("Failed to set parameter")
                return None
        except :
            return None
        

        response = self.getRegisters(id, MpptEpeverAddress.OTHER_PARAMETER)
        
        if (response is not None) :
            if (response.isError()) :
                return None
        else :
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
        response = self.getRegisters(id, MpptEpeverAddress.PV_INFO, input_register=True)
        if (response is not None) :
            if (not response.isError()) :
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
        if (response is not None) :
            if (not response.isError()) :
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
    
    def getNightTimeThreshold(self, id : int) -> int :
        """
        Get all PV info such as voltage, current and power

        Args :
        id (int) : slave id of the target device

        Returns :
        dict : dictionary with key:value pair
        """
        value = -1
        response = self.getRegisters(id, MpptEpeverAddress.NIGHT_TIME_THRESHOLD)
        if (response is not None) :
            if (not response.isError()) :
                value = round(response.registers[0] / 100, 2) 
        
        result = {
            'night_time_threshold': {
                'value': value,
                'satuan': 'Volt'
            }
        }
        
        return result
    
    def getDayTimeThreshold(self, id : int) -> int :
        """
        Get all PV info such as voltage, current and power

        Args :
        id (int) : slave id of the target device

        Returns :
        dict : dictionary with key:value pair
        """
        value = -1
        response = self.getRegisters(id, MpptEpeverAddress.DAY_TIME_THRESHOLD)
        
        if (response is not None) :
            if (not response.isError()) :
                value = round(response.registers[0] / 100, 2)            
        
        result = {
            'day_time_threshold': {
                'value': value,
                'satuan': 'Volt'
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
        request = self.client.write_coil(MpptEpeverAddress.LOAD_MANUAL_CONTROL[0], 0, unit=id)
        if (request is None) :
            return 0
        if (request.isError()) or (request is None):
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
        if (request is None) :
            return 0
        if (request.isError()):
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
        if (request.isError()) or (request is None):
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
        if (request is None) :
            return 0
        if (request.isError()):
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
        if request is None :
            return 0
        if (request.isError()):
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
        if (request is None) :
            return 0
        if (request.isError()) or (request is None):
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
        if request is None :
            return 0
        if (request.isError()) or (request is None):
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
    
    def setChargingModeSoc(self, id : int) -> int:
        """
        Set Bulk Parameter, convert MpptEpeverSetting into list of integer with length of 15
        
        Args :
        setting (MpptEpeverSetting) : MpptEpeverSetting Object, refer to MpptEpeverSetting description for member information        
        """
        
        request = self.setRegisters(id, MpptEpeverAddress.CHARGING_MODE[0], 1)
        
        if (request is None) :
            return 0
        
        if (not request.isError()) :
            return 1
        else :
            return 0
        
    def setChargingModeVoltageCompensation(self, id : int) -> int:
        """
        Set Bulk Parameter, convert MpptEpeverSetting into list of integer with length of 15
        
        Args :
        setting (MpptEpeverSetting) : MpptEpeverSetting Object, refer to MpptEpeverSetting description for member information        
        """
        
        request = self.setRegisters(id, MpptEpeverAddress.CHARGING_MODE[0], 0)
        
        if (request is None) :
            return 0
        
        if (not request.isError()) :
            return 1
        else :
            return 0
        
    def restoreSystemDefault(self, id : int) -> int :
        """
        Restore to factory system setting

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.RESTORE_SYSTEM_DEFAULTS[0], 1, unit=id)
        if (request is None) :
            return 0
        if (request.isError()) :
            return 0
        return 1
    
    def clearLog(self, id : int) -> int :
        """
        Clear log

        Args :
        id (int) : slave id of target device

        Returns :
        int : 1 if success, 0 if failed
        """
        request = self.client.write_coil(MpptEpeverAddress.CLEAR_LOG[0], 1, unit=id)
        if request is None :
            return 0
        if (request.isError()):
            return 0
        return 1

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
        if (response is not None) :
            if (not response.isError()) :
                return response.registers
        return None

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
        
        if (response is not None) :
            if (not response.isError()) :
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

        if (response is not None) :
            if (not response.isError()) :
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
        if (response is not None) :
            if (not response.isError()) :
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
        if (response is not None) :
            if (not response.isError()) :
                batteryStatus = response.registers[0]
                print("Battery status value :", batteryStatus)
                batteryStatusDict = s.unpackBatteryStatus(batteryStatus)
                chargingStatus = response.registers[1]
                print("Charging status value :", chargingStatus)
                chargingStatusDict = s.unpackChargingStatus(chargingStatus)
                dischargingStatus = response.registers[2]
                print("Discharging status value :", dischargingStatus)
                dischargingStatusDict = s.unpackDischargingStatus(dischargingStatus)
            
                result = {
                    'battery_status' : batteryStatusDict,
                    'charging_status' : chargingStatusDict,
                    'discharging_status' : dischargingStatusDict
                }
                return result
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
        if (response is not None) :
            if (not response.isError()) :
                batteryStatus = response.registers[0]
                s.unpackBatteryStatus(batteryStatus)
                chargingStatus = response.registers[1]
                s.unpackChargingStatus(chargingStatus)
                dischargingStatus = response.registers[2]
                s.unpackDischargingStatus(dischargingStatus)
                result = s.dischargingStatus.dischargingState 
                return result
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
        if (response is not None) :
            if (not response.isError()) :
                batteryStatus = response.registers[0]
                s.unpackBatteryStatus(batteryStatus)
                chargingStatus = response.registers[1]
                s.unpackChargingStatus(chargingStatus)
                dischargingStatus = response.registers[2]
                s.unpackDischargingStatus(dischargingStatus)
                result = s.chargingStatus.chargingState 
                return result
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
        if (response is not None) :
            if (not response.isError()) :
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
        if (response is not None) :
            if (not response.isError()) :
                loadCurrent = round(response.registers[0] / 100, 2)
        
        result = {
            'rated_load_current': {
                'value': loadCurrent,
                'satuan': 'Ampere'
            }
        }
        return result
    
class MpptEpeverSerial(BaseMPPTEPVEPER) :
    def __init__(self, port : str, method : str = 'rtu', baudrate : int = 115200, timeout : int = 1):
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
    
    def begin(self, port : str, method : str = 'rtu', baudrate : int = 115200, timeout : int = 1) :
        self.client = ModbusSerialClient(method=method, port=port, baudrate=baudrate, timeout=timeout)

    def end(self) :
        if (self.modbusInit) :
            self.client.close()
        self.client = None
        self.modbusInit = False

class MpptEpeverTCP(BaseMPPTEPVEPER):
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