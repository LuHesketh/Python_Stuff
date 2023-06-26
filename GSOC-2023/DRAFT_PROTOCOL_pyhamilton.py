import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject,
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging,
 ResourceType)

lmgr = LayoutManager('deck_.lay')
tips_res = resource_list_with_prefix(lmgr, 'STF_L_0001', Tip96, 1)
reagent_container = resource_list_with_prefix(lmgr, 'Mrx_96_DW_0001', Plate96, 1)
destination_plate = resource_list_with_prefix(lmgr, 'Mrx_96_DW_0003', Plate96, 1)

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Part'

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
    
tips = TipRack(tips_res[0])

num_targets = 10



def add_ethanol(ham_int, source, target, num_targets, vols_list):
    remaining_targets = num_targets
    while remaining_targets > 0:
        num_channels = 8 if remaining_targets >= 8 else remaining_targets
        completed_targets = num_targets - remaining_targets
        
        tips_poss = tips.get_tips(num_channels)
        tip_pick_up(ham_int, tips_poss)

        aspirate_poss = [(source, x) for x in range(num_channels)]
        vols_list = [250]*num_channels
        aspirate(ham_int, aspirate_poss, vols_list, liquidClass = liq_class)
        
        dispense_poss = [(target, x) for x in range(completed_targets, completed_targets + num_channels)]
        
        dispense(ham_int, dispense_poss, vols_list, mixCycles = 3, mixVolume = 100, liquidClass = liq_class)
        tip_eject(ham_int)
        remaining_targets -= num_channels
        


if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int: 
        initialize(ham_int)
        add_ethanol(ham_int, source = reagent_container[0], target = destination_plate[0], num_targets = 10, vols_list = 250)
