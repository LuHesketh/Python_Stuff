import os

import pyhamilton 

from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, 
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging)

from pyhamilton import (mpe2_connect_ip, mpe2_connect_com, mpe2_initialize, mpe2_filter_plate_placed,   mpe2_process_filter_to_waste_container,  mpe2_retrieve_filter_plate)

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Empty'

#

lmgr = LayoutManager('deck.lay')


if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        normal_logging(ham_int, os.getcwd())
        initialize(ham_int)
        mpe2_id = mpe2_connect_com(ham_int,  com_port, baud_rate, simulation_mode = True, options = 0)
        print(mpe2_id)
        mpe2_initialize(ham_int, mpe2_id)
