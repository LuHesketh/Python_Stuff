# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 21:12:47 2022

@author: 
"""

import json  
from json import JSONEncoder
import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, 
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging)



from pyhamilton import (mpe2_connect_com, mpe2_filter_plate_placed, mpe2_process_filter_to_waste_container, mpe2_filter_plate_removed)



lmgr = LayoutManager('MPEdeck.lay')

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Part'


def Activate_overpressure(mpe2_filter_plate_placed, mpe2_process_filter_to_waste_container, mpe2_filter_plate_removed):
        
        mpe2_filter_plate_placed(ham_int, mpe2_id, 15, 15)
        
        mpe2_process_filter_to_waste_container(ham_int, mpe2_id, control_points, return_plate_to_integration_area='', waste_container_id='', disable_vacuum_check='')
        
        mpe2_filter_plate_removed(ham_int, mpe2_id)


        
if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        mpe2_id = mpe2_connect_com(ham_int, 12, 921600, simulation_mode =False, options = 0)
        mpe2_id.return_data[0]
        mpe2_id = int(mpe2_id.return_data[0])
        print(mpe2_id)
        mpe2_filter_plate_placed(ham_int, mpe2_id, 15, 15)
        mpe2_clamp_filter_plate(ham, mpe2_id)



   

        


  