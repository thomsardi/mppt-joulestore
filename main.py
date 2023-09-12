from mppt.mpptepveper.mppt_epveper import MPPTEPVEPER, MpptEpeverSetting, EpeverParserSetting
from mppt.mpptsrne.mppt_srne import MpptSrne, MpptSrneSetting, SrneParserSetting
from mppt.base import MpptError
import json
import time
from typing import List

if __name__ == "__main__" :
   epeverSettingfile = json.load(open('mppt/mpptepveper/register_config.json')) #convert the json file into dict
   epeverPort = epeverSettingfile['port'] #get port name from register_config.json file
   # mpptEpever = MPPTEPVEPER(port=epeverPort, timeout=0.1) #setup modbus with specified port, 115200 baudrate, 0.1s timeout
   parser = EpeverParserSetting() #create ParserSetting object
   epeverSettingList : List[MpptEpeverSetting] = parser.parse(epeverSettingfile) #get value from "parameter" key 

   srneSettingfile = json.load(open('mppt/mpptsrne/register_config.json')) #convert the json file into dict
   srnePort = srneSettingfile['port'] #get port name from register_config.json file
   # mpptSrne = MpptSrne(port=srnePort, timeout=0.1) #setup modbus with specified port, 115200 baudrate, 0.1s timeout
   parser = SrneParserSetting() #create ParserSetting object
   srneSettingList : List[MpptSrneSetting] = parser.parse(srneSettingfile) #get value from "parameter" key 

   choice : bool = False

   while(1) :
      if (choice) :
         print("Connecting modbus to epever")
         mppt = MPPTEPVEPER(port=epeverPort, timeout=0.1)
         settingList = epeverSettingList
      else :
         print("Connecting modbus to srne")
         mppt = MpptSrne(port=srnePort, timeout=0.1)
         settingList = srneSettingList

      for a in settingList : #for loop to write a new setting
        mppt.change_setting(a) #change setting
        
      slaveList = mppt.scan(1,20) #start id scan
      print("List of connected slave :", slaveList)
      for slave in slaveList :
         params = mppt.get_current_setting(slave) #get current setting of mppt
         if (params is not None) :
               params.printContainer() #print the container
         if (mppt.set_load_mode_auto(slave)) : #set load mode to 17
               print("Success set load mode to auto")
         else :
               print("Failed to set load mode to auto")
         if (mppt.set_load_mode_manual(slave)) : #set load mode to 15
               print("Success set load mode to manual")
         else :
               print("Failed to set load mode to manual")

         mppt.setLoadMode(slave, 15) #set load mode to 15

         if (mppt.set_load_off(slave)) : #set load off
               print("Success set load off at id", slave)
         else :
               print("Failed set load off at id", slave)

         if (mppt.set_load_on(slave)) : #set load on
               print("Success set load on at id", slave)
         else :
               print("Failed set load on at id", slave)

         print(mppt.get_pv_info(slave)) #get pv info
         print(mppt.get_generated_energy(slave)) #get generated energy
         print(mppt.get_battery_info(slave)) #get battery info
         print(mppt.get_load_info(slave)) #get load info
         print(mppt.get_load_state(slave)) #get load state
         time.sleep(0.1) #always add sleep when using modbus within for loop. without sleep, the modbus result always failed
      choice = not choice
      time.sleep(0.1)


   
    