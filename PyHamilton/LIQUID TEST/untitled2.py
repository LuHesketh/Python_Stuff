# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:55:47 2023

@author: Luiza
"""
import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, 
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging)

from pyhamilton import (mpe2_connect_ip, mpe2_connect_com, mpe2_initialize)

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Empty'



lmgr = LayoutManager('deck.lay')

mpe2_filter_plate_placed(ham,  mpe2_id , filter_height, nozzle_height)


if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        normal_logging(ham_int, os.getcwd())
        initialize(ham_int)
        mpe2_id = mpe2_connect_ip(ham_int, '192.168.100.100', 2000, simulation_mode = True, options = 0)
        print(mpe2_id)
        mpe2_initialize(ham_int, mpe2_id)
        mpe2_process_filter_to_waste_container(ham_int, mpe2_id, control_points, return_plate_to_integration_area='', waste_container_id='', disable_vacuum_check='')