# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:09:19 2023

@author: Hamilton
"""

import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, 
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging)

from pyhamilton import (mpe2_connect_com, mpe2_filter_plate_placed, mpe2_initialize, mpe2_clamp_filter_plate, mpe2_retrieve_filter_plate, mpe2_filter_plate_removed)

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Part'



lmgr = LayoutManager('MPEdeck.lay')


        
if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        mpe2_id = mpe2_connect_com(ham_int, 12, 921600, simulation_mode =False, options = 0)
        mpe2_id.return_data[0]
        mpe2_id = int(mpe2_id.return_data[0])
        print(mpe2_id)
        mpe2_filter_plate_placed(ham_int, mpe2_id, 16, 39)
        mpe2_clamp_filter_plate(ham_int, mpe2_id)
        mpe2_retrieve_filter_plate(ham_int, mpe2_id)
        
        
        
        
        mpe2_filter_plate_removed(ham_int, mpe2_id)

        
 
