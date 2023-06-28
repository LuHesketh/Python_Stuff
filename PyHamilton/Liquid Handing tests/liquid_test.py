# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
""
"""


import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, Plate96, Tip96, initialize, tip_pick_up, 
                        tip_eject, oemerr, aspirate, dispense, resource_list_with_prefix, normal_logging, ResourceType)

#the layout manager allows you to acces the labware ID on venus so you can attatch it to the liquid handling commands
lmgr = LayoutManager('deck_.lay')


tips = resource_list_with_prefix(lmgr, 'STF_L_0001', Tip96, 1)
reagent_container = resource_list_with_prefix(lmgr, 'Mrx_96_DW_0001', Plate96, 1)
destination_plate = resource_list_with_prefix(lmgr, 'Mrx_96_DW_0002', Plate96, 1)

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Part'



aspiration_poss = [(reagent_container[0], x) for x in range(8)]		
dispense_poss = [(destination_plate[0], x) for x in range(8)]
vols_list = [200]*8


tips_poss = [(tips[0], x) for x in range(8)]

 
if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        tip_pick_up(ham_int, tips_poss)
        aspirate(ham_int, aspiration_poss, vols_list, liquidClass = liq_class)
        dispense(ham_int, dispense_poss, vols_list, liquidClass = liq_class)
        tip_eject(ham_int, tips_poss)    
	
	

	


