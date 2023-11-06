from mppt.mpptsrne.mppt_srne import MpptSrneTCP, MpptSrneSetting, SrneParserSetting
from mppt.base import MpptError
import json
import time
from typing import List

if __name__ == "__main__" :
    srneSettingfile = json.load(open('mppt/mpptsrne/register_config_tcp.json')) #convert the json file into dict
    srneHost = srneSettingfile['host'] #get port name from register_config.json file
    mpptSrne =  MpptSrneTCP(host=srneHost, port=502, timeout=0.5) #setup modbus with specified port, 9600 baudrate, 0.1s timeout
    parser = SrneParserSetting() #create ParserSetting object
    srneSettingList : List[MpptSrneSetting] = parser.parse(srneSettingfile) #get value from "parameter" key 

    for a in srneSettingList : #for loop to write a new setting
        mpptSrne.change_setting(a) #change setting
        
    slaveList = mpptSrne.scan(4,6) #start id scan
    print("start scan")
    print("List of connected slave :", slaveList)

    while(1) :
        for slave in slaveList :
            params = mpptSrne.get_current_setting(slave) #get current setting of mppt
            if (params is not None) :
                params.printContainer() #print the container
            if (mpptSrne.set_load_mode_auto(slave)) : #set load mode to 17
                print("Success set load mode to auto")
            else :
                print("Failed to set load mode to auto")
            if (mpptSrne.set_load_mode_manual(slave)) : #set load mode to 15
                print("Success set load mode to manual")
            else :
                print("Failed to set load mode to manual")

            mpptSrne.setLoadMode(slave, 15) #set load mode to 15

            if (mpptSrne.set_load_off(slave)) : #set load off
                print("Success set load off at id", slave)
            else :
                print("Failed set load off at id", slave)

            if (mpptSrne.set_load_on(slave)) : #set load on
                print("Success set load on at id", slave)
            else :
                print("Failed set load on at id", slave)
            print(mpptSrne.get_status_info(slave))
            print(mpptSrne.get_pv_info(slave)) #get pv info
            print(mpptSrne.get_generated_energy(slave)) #get generated energy
            print(mpptSrne.get_battery_info(slave)) #get battery info
            print(mpptSrne.get_load_info(slave)) #get load info
            print(mpptSrne.get_load_state(slave)) #get load state
            time.sleep(0.5) #always add sleep when using modbus within for loop. without sleep, the modbus result always failed
        time.sleep(0.5)