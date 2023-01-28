# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 09:18:09 2023

@author: Luiza
"""
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, 
 aspirate, dispense,  oemerr, resource_list_with_prefix)

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Empty_with_transport_vol'


lmgr = LayoutManager('deckarray.lay')
plates = resource_list_with_prefix(lmgr, 'plate_', Plate96, 5)
tips = resource_list_with_prefix(lmgr, 'tips', Tip96, 5)


tips_poss = [(tips[0], x) for x in range(8)]


if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        tip_pick_up(ham_int, tips_poss)
        tip_eject(ham_int, tips_poss)
        
       