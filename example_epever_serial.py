from mppt.mpptepveper.mppt_epveper import MpptEpeverSerial, MpptEpeverSetting, EpeverParserSetting
from mppt.base import MpptError
import json
import time
from typing import List

if __name__ == "__main__" :
    epeverSettingfile = json.load(open('mppt/mpptepveper/register_config.json')) #convert the json file into dict
    epeverPort = epeverSettingfile['port'] #get port name from register_config.json file
    mpptEpever =  MpptEpeverSerial(port=epeverPort, timeout=0.1) #setup modbus with specified port, 115200 baudrate, 0.1s timeout
    parser = EpeverParserSetting() #create ParserSetting object
    epeverSettingList : List[MpptEpeverSetting] = parser.parse(epeverSettingfile) #get value from "parameter" key 

    for a in epeverSettingList : #for loop to write a new setting
        mpptEpever.change_setting(a) #change setting

    slaveList = mpptEpever.scan(1,3) #start id scan
    print("List of connected slave :", slaveList)

    while(1) :
        
        for slave in slaveList :
            params = mpptEpever.get_current_setting(slave) #get current setting of mppt
            if (params is not None) :
                params.printContainer() #print the container
            if (mpptEpever.set_load_mode_auto(slave)) : #set load mode to 17
                print("Success set load mode to auto")
            else :
                print("Failed to set load mode to auto")
            if (mpptEpever.set_load_mode_manual(slave)) : #set load mode to 15
                print("Success set load mode to manual")
            else :
                print("Failed to set load mode to manual")

            mpptEpever.setLoadMode(slave, 15) #set load mode to 15

            if (mpptEpever.set_load_off(slave)) : #set load off
                print("Success set load off at id", slave)
            else :
                print("Failed set load off at id", slave)

            if (mpptEpever.set_load_on(slave)) : #set load on
                print("Success set load on at id", slave)
            else :
                print("Failed set load on at id", slave)

            print(mpptEpever.get_pv_info(slave)) #get pv info
            print(mpptEpever.get_generated_energy(slave)) #get generated energy
            print(mpptEpever.get_battery_info(slave)) #get battery info
            print(mpptEpever.get_load_info(slave)) #get load info
            print(mpptEpever.get_load_state(slave)) #get load state
            time.sleep(0.1) #always add sleep when using modbus within for loop. without sleep, the modbus result always failed
        time.sleep(0.1)