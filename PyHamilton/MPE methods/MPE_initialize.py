# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 21:12:47 2022

@author: 
"""
import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager,  initialize, tip_pick_up, tip_eject, 
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging)

from pyhamilton import ( mpe2_connect_com, mpe2_initialize)

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Part'



lmgr = LayoutManager('MPEdeck.lay')


if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        mpe2_id = mpe2_connect_com(ham_int, 12, 921600, simulation_mode =False, options = 0)
        mpe2_id.return_data[0]
        mpe2_id = int(mpe2_id.return_data[0])
        print(mpe2_id)
        mpe2_initialize(ham_int, mpe2_id)
       
