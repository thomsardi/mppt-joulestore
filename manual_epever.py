from mppt.mpptepveper.mppt_epveper import MPPTEPVEPER, MpptEpeverSetting, EpeverParserSetting
from mppt.base import MpptError
import json
import time
from typing import List

if __name__ == "__main__" :
    epeverSettingfile = json.load(open('mppt/mpptepveper/register_config.json')) #convert the json file into dict
    epeverPort = epeverSettingfile['port'] #get port name from register_config.json file
    mpptEpever =  MPPTEPVEPER(port=epeverPort, timeout=0.1) #setup modbus with specified port, 115200 baudrate, 0.1s timeout
    parser = EpeverParserSetting() #create ParserSetting object
    epeverSettingList : List[MpptEpeverSetting] = parser.parse(epeverSettingfile) #get value from "parameter" key 

    for a in epeverSettingList : #for loop to write a new setting
        status = mpptEpever.change_setting(a) #change setting
        if (status < 0) :
            print("Modbus error")
        elif (status == 0) :
            print("Same setting, skip writing!")
        else :
            print("Success writing")
        time.sleep(0.1)

    # for a in epeverSettingList : #for loop to write a new setting
    #     mpptEpever.change_setting(a) #change setting
    # print(epeverPort)    
    # slaveList = mpptEpever.scan(1,10) #start id scan
    # print("List of connected slave :", slaveList)
    # for slave in slaveList :
    while(1) :
        
        # print(epeverPort)
        if (mpptEpever.set_load_on(1)) : #set load on
            print("Success set load on at id", 1)
        else :
            print("Failed set load on at id", 1)

        params = mpptEpever.get_current_setting(1) #get current setting of mppt

        if (params is not None) :
            params.printContainer()

        print(mpptEpever.get_pv_info(1)) #get pv info
        print(mpptEpever.get_generated_energy(1)) #get generated energy
        print(mpptEpever.get_battery_info(1)) #get battery info
        print(mpptEpever.getBatterySoc(1))
        print(mpptEpever.get_load_info(1)) #get load info
        print(mpptEpever.get_load_state(1)) #get load state
        print(mpptEpever.getStatusInfo(1))
        time.sleep(0.1) #always add sleep when using modbus within for loop. without sleep, the modbus result always failed

        if (mpptEpever.set_load_on(2)) : #set load on
            print("Success set load on at id", 2)
        else :
            print("Failed set load on at id", 2)

        if (mpptEpever.setChargeOn(2)) :
            print("Success set charge on")

        if (mpptEpever.clearLog(2)) :
            print("Success clear log")

        params = mpptEpever.get_current_setting(2) #get current setting of mppt

        if (params is not None) :
            params.printContainer()

        print(mpptEpever.get_pv_info(2)) #get pv info
        print(mpptEpever.get_generated_energy(2)) #get generated energy
        print(mpptEpever.get_battery_info(2)) #get battery info
        print(mpptEpever.getBatterySoc(2))
        print(mpptEpever.get_load_info(2)) #get load info
        print(mpptEpever.get_load_state(2)) #get load state
        print(mpptEpever.getNightTimeThreshold(2))
        print(mpptEpever.getDayTimeThreshold(2))
        print(mpptEpever.getStatusInfo(2))
        time.sleep(0.1) #always add sleep when using modbus within for loop. without sleep, the modbus result always failed

        if (mpptEpever.set_load_on(3)) : #set load on
            print("Success set load on at id", 3)
        else :
            print("Failed set load on at id", 3)

        print(mpptEpever.get_pv_info(3)) #get pv info
        print(mpptEpever.get_generated_energy(3)) #get generated energy
        print(mpptEpever.get_battery_info(3)) #get battery info
        print(mpptEpever.get_load_info(3)) #get load info
        print(mpptEpever.get_load_state(3)) #get load state
        print(mpptEpever.getStatusInfo(3))
        time.sleep(0.1) #always add sleep when using modbus within for loop. without sleep, the modbus result always failed
    time.sleep(0.1)