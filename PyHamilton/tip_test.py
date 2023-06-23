# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
""
"""
<<<<<<< HEAD


import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, Plate96, Tip96, initialize, tip_pick_up, tip_eject,  oemerr, resource_list_with_prefix, normal_logging, ResourceType)


lmgr = LayoutManager('deck.lay')
tips = resource_list_with_prefix(lmgr, 'STF_L_0001', Tip96, 1)
liq_class = 'StandardVolumeFilter_Water_DispenseJet_Part'
		
tips_poss = [(tips[0], x) for x in range(1)]

=======

import os
import pyhamilton

from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, 
 aspirate, dispense,  oemerr, resource_list_with_prefix)

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


lmgr = LayoutManager('deck.lay')
tips_res = lmgr.assign_unused_resource(ResourceType(Tip96, 'tips_96'))
liq_class = 'StandardVolumeFilter_Water_DispenseJet_Empty'

tips = TipRack(tips_res)

tips_poss = tips.get_tips(num_channels)
        tip_pick_up(ham_int, tips_poss)
>>>>>>> 780008592c60c8f2b19579fd0b1be72cdbba4211

 
if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        normal_logging(ham_int, os.getcwd())
        initialize(ham_int)
        tip_pick_up(ham_int, tips_poss)
<<<<<<< HEAD
        tip_eject(ham_int, tips_poss)    
	
	
'0x129290eb3fe5'
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
  File "C:\Program Files (x86)\Python39-32\lib\site-packages\pyhamilton\liquid_handling_wrappers.py", line 156, in tip_pick_up
    ham_int.wait_on_response(ham_int.send_command(PICKUP,
  File "C:\Program Files (x86)\Python39-32\lib\site-packages\pyhamilton\interface.py", line 653, in wait_on_response
    return self.parse_response(server_response, raise_first_exception, return_data)
  File "C:\Program Files (x86)\Python39-32\lib\site-packages\pyhamilton\interface.py", line 672, in parse_response
    hamiltonResponse.raise_first_exception()
  File "C:\Program Files (x86)\Python39-32\lib\site-packages\pyhamilton\interface.py", line 418, in raise_first_exception
    raise HAMILTON_ERROR_MAP[firstErrorCode]()
pyhamilton.oemerr.NoTipError
	




=======
        tip_eject(ham_int, tips_poss)
        
       
>>>>>>> 780008592c60c8f2b19579fd0b1be72cdbba4211
