# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
""
"""


import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, Plate96, Tip96, initialize, tip_pick_up, tip_eject,  oemerr, resource_list_with_prefix, normal_logging, ResourceType)


lmgr = LayoutManager('deck.lay')
tips = resource_list_with_prefix(lmgr, 'VER_HT_0001', Tip96, 1)
liq_class = 'HighVolume_Water_DispenseSurface_Part'
		
tips_poss = [(tips[0], x) for x in range(1)]


 
if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        tip_pick_up(ham_int, tips_poss)
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
	



