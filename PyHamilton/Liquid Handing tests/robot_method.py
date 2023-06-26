# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 16:46:24 2023

"""
import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, move_plate,
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging,
 ResourceType)


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


num_targets = 30

lmgr = LayoutManager('deck_.lay')
tips_res = lmgr.assign_unused_resource(ResourceType(Tip96, 'STF_L_0001'))
sample_plate = lmgr.assign_unused_resource(ResourceType(Plate96, 'Mrx_96_DW_0002'))
reagent_plate = lmgr.assign_unused_resource(ResourceType(Plate96, 'Mrx_96_DW_0001'))

tips = TipRack(tips_res)
 

def add_water(source, target, num_targets, vol):
    remaining_targets = num_targets
    while remaining_targets > 0:
        num_channels = 8 if remaining_targets >= 8 else remaining_targets
        completed_targets = num_targets - remaining_targets
        
        tips_poss = tips.get_tips(num_channels)
        tip_pick_up(ham_int, tips_poss)

        aspirate_poss = [(source, idx) for idx in range(num_channels)]
        vols = [vol]*num_channels
        aspirate(ham_int, aspirate_poss, vols, liquidClass = liq_class)
        
        dispense_poss = [(target, idx) for idx in range(completed_targets, completed_targets + num_channels)]
        
        dispense(ham_int, dispense_poss, vols, mixCycles = 3, mixVolume = 100, liquidClass = liq_class)
        tip_eject(ham_int)
        remaining_targets -= num_channels
        

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Part'


if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        add_water( reagent_plate, sample_plate, num_targets = 30, vol = 200)
   