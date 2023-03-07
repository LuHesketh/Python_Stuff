# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 17:46:32 2023

@author: Luiza
"""
import json
from json import JSONEncoder
import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, move_plate, hhs_start_shaker,  hhs_stop_shaker,
 aspirate, dispense, oemerr, resource_list_with_prefix, normal_logging,
 ResourceType)

from pyhamilton import(hhs_begin_monitoring, hhs_create_star_device, hhs_create_usb_device,
            hhs_end_monitoring, hhs_get_firmware_version, hhs_get_serial_num, hhs_get_shaker_param,
            hhs_get_shaker_speed, hhs_get_temp_param, hhs_get_temp, hhs_get_temp_state, hhs_send_firmware_cmd,
            hhs_set_plate_lock, hhs_stop_all_shakers, hhs_set_shaker_param, 
            hhs_set_simulation, hhs_set_temp_param, hhs_set_usb_trace, hhs_start_all_shaker,
            hhs_start_all_shaker_timed, hhs_start_shaker, hhs_start_shaker_timed, hhs_start_temp_ctrl,
            hhs_stop_shaker, hhs_stop_temp_ctrl, hhs_terminate, hhs_wait_for_shaker, hhs_wait_for_temp_ctrl)



from pyhamilton import (mpe2_connect_com, mpe2_filter_plate_placed, mpe2_process_filter_to_waste_container, mpe2_filter_plate_removed)



"""
   This DNA cleanup/purification protocol is to be executed using 2 HAMILTON modules. They are:
       
   * MPE2- Air pressure module. to be used to push/process the liquids through a filter
   * HHS/Heater shaker - to shake the final product at 30 celcius (necessary finalstep)    
       
    the commands will be imported from PyHamilton and they are called out in the final "if name_=_main_" function THIS ORDER:
        
        - robot grab tip
        - use tip to transport DNA from DNA plate to filter plate (later ejecting the tip)
        - process DNA through filter 
        - do 2 washing steps through filter
        - and add water to the filter plate
        - move filter plate to heater shaker
        - do shaking steps
        - retrieve plate manually from heater shaker
       
   """


class TipRack:
   
    def __init__(self, rack):
        self.rack = rack
        self.starting_tips = rack._num_items
        self.remaining_tips = rack._num_items
    
    def get_tips(self, num_tips):
        current_tip = self.starting_tips - self.remaining_tips
        tips_list = [(self.rack, tip) for tip in range(current_tip, current_tip + num_tips)]
        self.remaining_tips -= num_tips
        return tips_list
    
    def get_tips_seq(self, seq):
        num_tips = len([ch for ch in seq.aspirate if ch])
        tips = self.get_tips(num_tips)
        return tips

#the targets here are the wells in the plates
num_targets = 30

#this 'lmgr' is what calls the layout file with all calibrated labwares
lmgr = LayoutManager('deck_.lay')

# we'll bu using two types of tips in this protocol corresponding to the volumes of liquids we want to aspirate and dispense. (300ul - 20ul)
tips_res1 = lmgr.assign_unused_resource(ResourceType(Tip96, 'STF_L_0001')) #low volume tips to transfer DNA
tips_res2 = lmgr.assign_unused_resource(ResourceType(Tip96, 'STF_L_0002')) #standard volume tips to transfer water
sample_plate = lmgr.assign_unused_resource(ResourceType(Plate96, 'Mrx_96_DW_0002'))
water_plate = lmgr.assign_unused_resource(ResourceType(Plate96, 'Mrx_96_DW_0001'))
DNA_plate = lmgr.assign_unused_resource(ResourceType(Plate96, 'Mrx_96_DW_0003'))
Heater_shaker = lmgr.assign_unused_resource(ResourceType(Plate96, 'heater_shaker_position'))


tips1 = TipRack(tips_res1)  

tips2 = TipRack(tips_res2)


# give parameters for MPE functions
Controlpoints = [   
     {  
          "Type": "pressure",
          "Value": 0,
          "Duration": 5
     },
     {  
          "Type": "pressure",
          "Value": 10,
          "Duration": 5
     },
     {  
          "Type": "pressure",   
          "Value": 15,
          "Duration": 5
     },
     {  
          "Type": "pressure",   
          "Value": 20,
          "Duration": 5
     },
     {  
          "Type": "pressure",
          "Value": 30,
          "Duration": 5
     },
     {  
          "Type": "pressure",
          "Value": 40,
          "Duration": 5
     },
     {  
          "Type": "pressure",
          "Value": 50,
          "Duration": 5
     },
     {  
          "Type": "pressure",
          "Value": 60,
          "Duration": 5
     },
     
]

control_points = Controlpoints[:]

#translate MPE parameters to a JSON series
json_string = json.dumps(Controlpoints, indent = 2)
with open('mydata.json', 'w') as f:
    f.write(json_string)



#transfer DNA from source plate to sample plate(should be located on the MPE dock)
def add_DNA(source, target, num_targets, vol):
    remaining_targets = num_targets
    while remaining_targets > 0:
        num_channels = 8 if remaining_targets >= 8 else remaining_targets
        completed_targets = num_targets - remaining_targets
        
        tips_poss1 = tips1.get_tips(num_channels)
        tip_pick_up(ham_int, tips_poss1)

        aspirate_poss = [(source, idx) for idx in range(num_channels)]
        vols = [vol]*num_channels
        aspirate(ham_int, aspirate_poss, vols, liquidClass = 'LowVolumeFilter_96COREHead_Water_DispenseSurface_Part')
        
        dispense_poss = [(target, idx) for idx in range(completed_targets, completed_targets + num_channels)]
        
        dispense(ham_int, dispense_poss, vols, mixCycles = 1, mixVolume = 50, liquidClass = 'LowVolumeFilter_96COREHead_Water_DispenseSurface_Part' ) #change it to a liquid class that fits the low volume tipstips 
        tip_eject(ham_int)
        remaining_targets -= num_channels
    
        
#function that will be used for the washing steps  using the aspiration and dispension pyhamilton functions 
def add_water(source, target, num_targets, vol):
    remaining_targets = num_targets
    while remaining_targets > 0:
        num_channels = 8 if remaining_targets >= 8 else remaining_targets
        completed_targets = num_targets - remaining_targets
        
        tips_poss2 = tips2.get_tips(num_channels)
        tip_pick_up(ham_int, tips_poss2)

        aspirate_poss = [(source, idx) for idx in range(num_channels)]
        vols = [vol]*num_channels
        aspirate(ham_int, aspirate_poss, vols, liquidClass = 'StandardVolumeFilter_Water_DispenseJet_Part')
        
        dispense_poss = [(target, idx) for idx in range(completed_targets, completed_targets + num_channels)]
        
        dispense(ham_int, dispense_poss, vols, mixCycles = 1, mixVolume = 50, liquidClass = 'StandardVolumeFilter_Water_DispenseJet_Part' )
        tip_eject(ham_int, tips_poss2)
        remaining_targets -= num_channels
        
        
#this function allows for the MPE to activate the air pump and process both DNA and water through the filter columns      
def Activate_overpressure( mpe2_filter_plate_placed, mpe2_process_filter_to_waste_container, mpe2_filter_plate_removed):
        
        mpe2_filter_plate_placed(ham_int, mpe2_id, 16, 39)
        
        mpe2_process_filter_to_waste_container(ham_int, mpe2_id, control_points, return_plate_to_integration_area='', waste_container_id='', disable_vacuum_check='')
        
        mpe2_filter_plate_removed(ham_int, mpe2_id)
  
#this is the last automated step of the protocol, after shaking you can retrieve the plate and manually take the DNA back      
def shake_samples(device_num, hhs_begin_monitoring, hhs_start_shaker,hhs_start_shaker_timed, hhs_start_temp_ctrl, hhs_stop_shaker, hhs_stop_temp_ctrl, hhs_wait_for_shaker, hhs_wait_for_temp_ctrl, hhs_terminate):    
    
       device_num = hhs_create_star_device(ham_int, used_node=1)

       device_num=1
       
       hhs_begin_monitoring(ham_int, device_num, 10, 5, 0)#correct parameters
       
       # heatershaker_start_all_shaker_timed

       hhs_start_shaker(ham_int, device_num, 500)#correct number and parameters

       hhs_start_shaker_timed(ham_int, device_num, 500, 5)#correct parameters

       hhs_start_temp_ctrl(ham_int, device_num, 50, 0)#correct parameters

       # heatershaker_stop_all_shakers

       hhs_stop_shaker(ham_int, device_num)

       hhs_stop_temp_ctrl(ham_int, device_num)

       # heatershaker_terminate

       hhs_wait_for_shaker(ham_int, device_num)

       hhs_wait_for_temp_ctrl(ham_int, device_num)

       hhs_terminate(ham_int)

#this is the final function, the actual recipe/protocol we want to execute. here we will call all python commands, functions, classes and objects nece
if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        device_num = hhs_create_star_device(ham_int, used_node=1)
        mpe2_id = mpe2_connect_com(ham_int, 12, 921600, simulation_mode =False, options = 0)
        mpe2_id.return_data[0]
        mpe2_id = int(mpe2_id.return_data[0])
        print(mpe2_id)
        
        
        #calling final functions with input robot commands
        add_DNA(DNA_plate, sample_plate, num_targets = 30, vol= 20)
        
        Activate_overpressure( mpe2_filter_plate_placed, mpe2_process_filter_to_waste_container, mpe2_filter_plate_removed)
        
        add_water(water_plate, sample_plate, num_targets = 30, vol = 200)
        
        Activate_overpressure( mpe2_filter_plate_placed, mpe2_process_filter_to_waste_container, mpe2_filter_plate_removed)
        
        add_water(water_plate, sample_plate, num_targets = 30, vol = 200)
        
        Activate_overpressure( mpe2_filter_plate_placed, mpe2_process_filter_to_waste_container, mpe2_filter_plate_removed)
        
        add_water(water_plate, sample_plate, num_targets = 30, vol = 100)

        move_plate(ham_int, sample_plate, Heater_shaker)
        
        shake_samples(device_num = 1, hhs_begin_monitoring, hhs_start_shaker,hhs_start_shaker_timed, hhs_start_temp_ctrl, hhs_stop_shaker, hhs_stop_temp_ctrl, hhs_wait_for_shaker, hhs_wait_for_temp_ctrl, hhs_terminate)


   
