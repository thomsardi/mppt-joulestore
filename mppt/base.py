import asyncio
import json
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from enum import Enum
from typing import List
from abc import ABC, abstractmethod
import logging

class MpptError(Exception) :
    def __init__(self, errCode : int, *args: object) -> None:
        super().__init__(*args)
        self.__errCode = errCode

    def get_message(self) -> str :    
        if (self.__errCode == 1) :
            return "Writing success!"
        elif (self.__errCode == 0) :
            return "Modbus write failed!"
        else :
            return "Same setting, skip writing!"
class ParameterSetting :
    def __init__(self) -> None:
        self.__paramList : list[int] = []
    
    @abstractmethod
    def __eq__(self, other): 
        pass

    @abstractmethod
    def printContainer(self) :
        pass
    
    @abstractmethod
    def getListParam(self) -> list[int]:
        pass

    @abstractmethod
    def setParam(self, registerList : list[int]) -> int:
        pass

    @property
    def paramList(self) -> list[int] :
        return self.__paramList.copy()
    
    @paramList.setter
    def paramList(self, val : list[int]) :
        self.__paramList = val.copy()
class BaseMPPTSync(ABC):

    def __init__(self, port, baudrate, timeout=1):
        self.__port = port
        self.__baudrate = baudrate
        self.__timeout = timeout
        self.client = ModbusClient(port=port, baudrate=baudrate, method='rtu',timeout=timeout)
        self.modbusInit = True

    @property
    def port(self) -> str:
        return self.__port

    @property
    def baudrate(self) -> int:
        return self.__baudrate

    def begin(self, port : str, baudrate : int, method : str, timeout : float) :
        self.client = ModbusClient(port=port, baudrate=baudrate, method=method, timeout=timeout)
        self.modbusInit = True

    def end(self) :
        self.client = None
        self.modbusInit = False

    def setRegisters(self, id:int, addr:int, val:list):
        if (not self.client.connect()) :
            return None
        request = self.client.write_registers(addr, val, unit=id)
        self.client.close()
        return request

    def getRegisters(self, id:int, info:tuple) -> list:
        addr = info[0]
        length = info[1]
        response_register = self.client.read_holding_registers(addr, length, unit=id)
        return response_register

    @abstractmethod
    def scan(self, start_id : int, end_id : int) -> list[int]:
        pass

    @abstractmethod
    def get_pv_info(self, id : int) -> dict:
        pass

    @abstractmethod
    def get_load_info(self, id : int) -> dict:
        pass

    @abstractmethod
    def get_battery_info(self, id : int) -> dict:
        pass

    @abstractmethod
    def get_generated_energy(self, id : int) -> dict:
        pass

    @abstractmethod
    def get_load_state(self, id : int) -> int:
        pass

    @abstractmethod
    def get_current_setting(self, id : int) -> ParameterSetting :
        pass

    @abstractmethod
    def change_setting(self, setting : ParameterSetting) -> MpptError :
        pass

    @abstractmethod
    def set_load_on(self, id : int) -> int :
        pass

    @abstractmethod
    def set_load_off(self, id : int) -> int :
        pass

    def set_load_auto(self, id : int) -> int :
        pass

    def set_load_manual(self, id : int) -> int :
        pass


class BaseMPPTAsync:

    async def getPVInfo(self, id):

        raise NotImplementedError

    async def setRegisters(self, id:int, addr:int, val:list):

        raise NotImplementedError

    async def getRegisters(self, id:int, info:tuple) -> list:
        raise NotImplementedError

    async def getPVInfo(self, id:int) -> dict:
        raise NotImplementedError

    # async def getProductModel(self, id:int) -> list:
    #     raise NotImplementedError

    # async def getSoftwareVersion(self, id:int) -> str:
    #     raise NotImplementedError

    # async def getHardwareVersion(self, id:int) -> str:

    #     raise NotImplementedError

    # async def getSerialNumber(self, id:int) -> str:
    #     raise NotImplementedError

    async def getEnergyDay(self, id:int) -> dict:

        raise NotImplementedError

    # async def getTemperature(self, id:int) -> dict:

    #     raise NotImplementedError

class BatteryType(Enum) :
    USER = 0
    SEALED = 1
    GEL = 2
    FLOODED = 3

class BatteryRatedVoltage(Enum) :
    AUTO_RECOGNIZED = 0
    VOLTAGE_12V = 1
    VOLTAGE_24V = 2
    VOLTAGE_36V = 3
    VOLTAGE_48V = 4
    VOLTAGE_60V = 5
    VOLTAGE_110V = 6
    VOLTAGE_120V = 7
    VOLTAGE_220V = 8
    VOLTAGE_240V = 9      
class ParserSetting() :
    def __init__(self) -> None:
        pass

    @abstractmethod
    def parse(self, val : dict) -> List[ParameterSetting] :
        pass

class BatteryStatus() :
    def __init__(self) -> None:
        self.batteryCondition = -1
        self.batteryTemperature = -1
        self.batteryInnerResistance = -1
        self.wrongIdentification = -1

class ChargingStatus() :
    def __init__(self) -> None:
        self.chargingState = -1
        self.chargingCondition = -1
        self.chargingStatus = -1
        self.pvInput = -1
        self.disequilibrium = -1
        self.loadMosfet = -1
        self.loadState = -1
        self.loadCurrent = -1
        self.inputCurrent = -1
        self.antiReverseMosfet = -1
        self.chargingAntiReverseMosfet = -1
        self.chargingMosfet = -1
        self.inputVoltage = -1

class DischargingStatus() :
    def __init__(self) -> None:
        self.dischargingState = -1
        self.dischargingCondition = -1
        self.outputState = -1
        self.boostState = -1
        self.highVoltageSide = -1
        self.inputVoltage = -1
        self.outputVoltage = -1
        self.stopDischarging = -1
        self.discharge = -1
        self.dischargingOutput = -1
        self.outputPower = -1
        self.inputVoltage = -1


class Status() :
    def __init__(self) -> None:
        """
        Collection of BatteryStatus, ChargingStatus and DischargingStatus
        """
        self.batteryStatus = BatteryStatus()
        self.chargingStatus = ChargingStatus()
        self.dischargingStatus = DischargingStatus()

    def unpackBatteryStatus(self, val : int) -> dict :
        """
        Unpack integer value into bit with each bit represent the state

        Args :
        val (int) : integer value that need to be unpacked

        Returns :
        dict : dictionary of the battery status
        """

        self.batteryStatus.batteryCondition = val & 0xf

        if (self.batteryStatus.batteryCondition == 0x00) :
            batteryConditionMsg = "normal"
        elif (self.batteryStatus.batteryCondition == 0x01) :
            batteryConditionMsg = "overvoltage"
        elif (self.batteryStatus.batteryCondition == 0x02) :
            batteryConditionMsg = "undervoltage"
        elif (self.batteryStatus.batteryCondition == 0x03) :
            batteryConditionMsg = "overdicharge"
        elif (self.batteryStatus.batteryCondition == 0x04) :
            batteryConditionMsg = "fault"
        else :
            batteryConditionMsg = "unrecognized"

        self.batteryStatus.batteryTemperature = (val >> 4) & 0xf

        if (self.batteryStatus.batteryTemperature == 0x00) :
            batteryTemperatureMsg = "normal"
        elif (self.batteryStatus.batteryTemperature == 0x01) :
            batteryTemperatureMsg = "overtemp"
        elif (self.batteryStatus.batteryTemperature == 0x02) :
            batteryTemperatureMsg = "lowtemp"
        else :
            batteryTemperatureMsg = "unrecognized"

        self.batteryStatus.batteryInnerResistance = (val >> 7) & 0x1
        if (self.batteryStatus.batteryInnerResistance == 0x00) :
            batteryInnerResistanceMsg = "normal"
        elif (self.batteryStatus.batteryInnerResistance == 0x01) :
            batteryInnerResistanceMsg = "abnormal"
        else :
            batteryInnerResistanceMsg = "unrecognized"

        self.batteryStatus.wrongIdentification = (val >> 15) & 0x1
        if (self.batteryStatus.wrongIdentification == 0x00) :
            wrongIdentificationMsg = "normal"
        elif (self.batteryStatus.wrongIdentification == 0x01) :
            wrongIdentificationMsg = "wrong"
        else :
            wrongIdentificationMsg = "unrecognized"

        result = {
            'battery_condition' : batteryConditionMsg,
            'battery_temperature' : batteryTemperatureMsg,
            'battery_inner_resistance' : batteryInnerResistanceMsg,
            'battery_identification' : wrongIdentificationMsg
        }

        return result

    def unpackChargingStatus(self, val : int) -> dict :
        """
        Unpack integer value into bit with each bit represent the state

        Args :
        val (int) : integer value that need to be unpacked

        Returns :
        dict : dictionary of the charging status
        """

        self.chargingStatus.chargingState = val & 0x1
        if (self.chargingStatus.chargingState == 0x00) :
            chargingStateMsg = "standby"
        elif (self.chargingStatus.chargingState == 0x01) :
            chargingStateMsg = "running"
        else :
            chargingStateMsg = "unrecognized"


        self.chargingStatus.chargingCondition = (val >> 1) & 0x1
        if (self.chargingStatus.chargingCondition == 0x00) :
            chargingConditionMsg = "normal"
        elif (self.chargingStatus.chargingCondition == 0x01) :
            chargingConditionMsg = "fault"
        else :
            chargingConditionMsg = "unrecognized"

        self.chargingStatus.chargingStatus = (val >> 2) & 0x03
        if (self.chargingStatus.chargingStatus == 0x00) :
            chargingStatusMsg = "no_charging"
        elif (self.chargingStatus.chargingStatus == 0x01) :
            chargingStatusMsg = "float"
        elif (self.chargingStatus.chargingStatus == 0x02) :
            chargingStatusMsg = "boost"
        elif (self.chargingStatus.chargingStatus == 0x03) :
            chargingStatusMsg = "equalization"
        else :
            chargingStatusMsg = "unrecognized"

        self.chargingStatus.pvInput = (val >> 4) & 0x1
        if (self.chargingStatus.pvInput == 0x00) :
            pvInputMsg = "normal"
        elif (self.chargingStatus.pvInput == 0x01) :
            pvInputMsg = "short_circuit"
        else :
            pvInputMsg = "unrecognized"

        self.chargingStatus.disequilibrium = (val >> 6) & 0x01
        if (self.chargingStatus.disequilibrium == 0x00) :
            disequilibriumMsg = "normal"
        elif (self.chargingStatus.disequilibrium == 0x01) :
            disequilibriumMsg = "disequilibrium"
        else :
            disequilibriumMsg = "unrecognized"

        self.chargingStatus.loadMosfet = (val >> 7) & 0x01
        if (self.chargingStatus.loadMosfet == 0x00) :
            loadMosfetMsg = "normal"
        elif (self.chargingStatus.loadMosfet == 0x01) :
            loadMosfetMsg = "short_circuit"
        else :
            loadMosfetMsg = "unrecognized"

        self.chargingStatus.loadState = (val >> 8) & 0x01
        if (self.chargingStatus.loadState == 0x00) :
            loadStateMsg = "normal"
        elif (self.chargingStatus.loadState == 0x01) :
            loadStateMsg = "short_circuit"
        else :
            loadStateMsg = "unrecognized"

        self.chargingStatus.loadCurrent = (val >> 9) & 0x01
        if (self.chargingStatus.loadCurrent == 0x00) :
            loadCurrentMsg = "normal"
        elif (self.chargingStatus.loadCurrent == 0x01) :
            loadCurrentMsg = "over_current"
        else :
            loadCurrentMsg = "unrecognized"

        self.chargingStatus.inputCurrent = (val >> 10) & 0x01
        if (self.chargingStatus.inputCurrent == 0x00) :
            inputCurrentMsg = "normal"
        elif (self.chargingStatus.inputCurrent == 0x01) :
            inputCurrentMsg = "over_current"
        else :
            inputCurrentMsg = "unrecognized"

        self.chargingStatus.antiReverseMosfet = (val >> 11) & 0x01
        if (self.chargingStatus.antiReverseMosfet == 0x00) :
            antiReverseMosfetMsg = "normal"
        elif (self.chargingStatus.antiReverseMosfet == 0x01) :
            antiReverseMosfetMsg = "short_circuit"
        else :
            antiReverseMosfetMsg = "unrecognized"

        self.chargingStatus.chargingAntiReverseMosfet = (val >> 12) & 0x01
        if (self.chargingStatus.chargingAntiReverseMosfet == 0x00) :
            chargingAntiReverseMosfetMsg = "normal"
        elif (self.chargingStatus.chargingAntiReverseMosfet == 0x01) :
            chargingAntiReverseMosfetMsg = "open_circuit"
        else :
            chargingAntiReverseMosfetMsg = "unrecognized"

        self.chargingStatus.chargingMosfet = (val >> 13) & 0x01
        if (self.chargingStatus.chargingMosfet == 0x00) :
            chargingMosfetMsg = "normal"
        elif (self.chargingStatus.chargingMosfet == 0x01) :
            chargingMosfetMsg = "short_circuit"
        else :
            chargingMosfetMsg = "unrecognized"

        self.chargingStatus.inputVoltage = (val >> 14) & 0x03
        if (self.chargingStatus.inputVoltage == 0x00) :
            inputVoltageMsg = "normal"
        elif (self.chargingStatus.inputVoltage == 0x01) :
            inputVoltageMsg = "no_input_power"
        elif (self.chargingStatus.inputVoltage == 0x02) :
            inputVoltageMsg = "higher_input_voltage"
        elif (self.chargingStatus.inputVoltage == 0x03) :
            inputVoltageMsg = "input_voltage_error"
        else :
            inputVoltageMsg = "unrecognized"

        result = {
            'charging_state' : chargingStateMsg,
            'charging_condition' : chargingConditionMsg,
            'charging_status' : chargingStatusMsg,
            'pv_input' : pvInputMsg,
            'disequilibrium' : disequilibriumMsg,
            'load_mosfet' : loadMosfetMsg,
            'load_state' : loadStateMsg,
            'load_current' : loadCurrentMsg,
            'input_current' : inputCurrentMsg,
            'anti_reverse_mosfet' : antiReverseMosfetMsg,
            'charging_anti_reverse_mosfet' : chargingAntiReverseMosfetMsg,
            'charging_mosfet' : chargingMosfetMsg,
            'input_voltage_status' : inputVoltageMsg,
        }

        return result
    
    def unpackDischargingStatus(self, val : int) -> dict :
        """
        Unpack integer value into bit with each bit represent the state

        Args :
        val (int) : integer value that need to be unpacked

        Returns :
        dict : dictionary of the discharging status
        """
        self.dischargingStatus.dischargingState = val & 0x1
        if (self.dischargingStatus.dischargingState == 0x00) :
            dischargingStateMsg = "standby"
        elif (self.dischargingStatus.dischargingState == 0x01) :
            dischargingStateMsg = "running"
        else :
            dischargingStateMsg = "unrecognized"


        self.dischargingStatus.dischargingCondition = (val >> 1) & 0x1
        if (self.dischargingStatus.dischargingCondition == 0x00) :
            dischargingConditionMsg = "normal"
        elif (self.dischargingStatus.dischargingCondition == 0x01) :
            dischargingConditionMsg = "fault"
        else :
            dischargingConditionMsg = "unrecognized"

        self.dischargingStatus.outputState = (val >> 4) & 0x01
        if (self.dischargingStatus.outputState == 0x00) :
            outputStateMsg = "normal"
        elif (self.dischargingStatus.outputState == 0x01) :
            outputStateMsg = "overvoltage"
        else :
            outputStateMsg = "unrecognized"

        self.dischargingStatus.boostState = (val >> 5) & 0x1
        if (self.dischargingStatus.boostState == 0x00) :
            boostStateMsg = "normal"
        elif (self.dischargingStatus.boostState == 0x01) :
            boostStateMsg = "overvoltage"
        else :
            boostStateMsg = "unrecognized"

        self.dischargingStatus.highVoltageSide = (val >> 6) & 0x01
        if (self.dischargingStatus.highVoltageSide == 0x00) :
            highVoltageSideMsg = "normal"
        elif (self.dischargingStatus.highVoltageSide == 0x01) :
            highVoltageSideMsg = "short_circuit"
        else :
            highVoltageSideMsg = "unrecognized"

        self.dischargingStatus.inputVoltage = (val >> 7) & 0x01
        if (self.dischargingStatus.inputVoltage == 0x00) :
            inputVoltageMsg = "normal"
        elif (self.dischargingStatus.inputVoltage == 0x01) :
            inputVoltageMsg = "overvoltage"
        else :
            inputVoltageMsg = "unrecognized"

        self.dischargingStatus.outputVoltage = (val >> 8) & 0x01
        if (self.dischargingStatus.outputVoltage == 0x00) :
            outputVoltageMsg = "normal"
        elif (self.dischargingStatus.outputVoltage == 0x01) :
            outputVoltageMsg = "abnormal"
        else :
            outputVoltageMsg = "unrecognized"

        self.dischargingStatus.stopDischarging = (val >> 9) & 0x01
        if (self.dischargingStatus.stopDischarging == 0x00) :
            stopDischargingMsg = "normal"
        elif (self.dischargingStatus.stopDischarging == 0x01) :
            stopDischargingMsg = "unable"
        else :
            stopDischargingMsg = "unrecognized"

        self.dischargingStatus.discharge = (val >> 10) & 0x01
        if (self.dischargingStatus.discharge == 0x00) :
            dischargeMsg = "normal"
        elif (self.dischargingStatus.discharge == 0x01) :
            dischargeMsg = "unable"
        else :
            dischargeMsg = "unrecognized"

        self.dischargingStatus.dischargingOutput = (val >> 11) & 0x01
        if (self.dischargingStatus.dischargingOutput == 0x00) :
            dischargingOutputMsg = "normal"
        elif (self.dischargingStatus.dischargingOutput == 0x01) :
            dischargingOutputMsg = "short_circuit"
        else :
            dischargingOutputMsg = "unrecognized"

        self.dischargingStatus.outputPower = (val >> 12) & 0x03
        if (self.dischargingStatus.outputPower == 0x00) :
            outputPowerMsg = "light_load"
        elif (self.dischargingStatus.outputPower == 0x01) :
            outputPowerMsg = "moderate"
        elif (self.dischargingStatus.outputPower == 0x02) :
            outputPowerMsg = "rated"
        elif (self.dischargingStatus.outputPower == 0x03) :
            outputPowerMsg = "overload"
        else :
            outputPowerMsg = "unrecognized"


        self.dischargingStatus.inputVoltage = (val >> 14) & 0x03
        if (self.dischargingStatus.inputVoltage == 0x00) :
            inputVoltageMsg = "normal"
        elif (self.dischargingStatus.inputVoltage == 0x01) :
            inputVoltageMsg = "low_voltage"
        elif (self.dischargingStatus.inputVoltage == 0x02) :
            inputVoltageMsg = "high_voltage"
        elif (self.dischargingStatus.inputVoltage == 0x03) :
            inputVoltageMsg = "no_access"
        else :
            inputVoltageMsg = "unrecognized"

        result = {
            'discharging_state' : dischargingStateMsg,
            'discharging_condition' : dischargingConditionMsg,
            'output_state' : outputStateMsg,
            'boost_state' : boostStateMsg,
            'high_voltage_side' : highVoltageSideMsg,
            'input_voltage' : inputVoltageMsg,
            'output_voltage' : outputVoltageMsg,
            'stop_discharging' : stopDischargingMsg,
            'discharge' : dischargeMsg,
            'discharging_output' : dischargingOutputMsg,
            'output_power' : outputPowerMsg,
            'input_voltage' : inputVoltageMsg,
        }

        return result
            
