<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 02:15:44 2023

@author: lUIZA
"""
import pyhamilton
import os
import csv
from pyhamilton import (HamiltonInterface, LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject,
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging,
 ResourceType)


lmgr = LayoutManager('deck_.lay')
tips_res = resource_list_with_prefix(lmgr, 'STF_L_0001', Tip96, 1)
source_plate = resource_list_with_prefix(lmgr, 'Mrx_96_DW_0001', Plate96, 1)
target_plate = resource_list_with_prefix(lmgr, 'Mrx_96_DW_0003', Plate96, 1)


liq_class = 'StandardVolumeFilter_Water_DispenseJet_Part'

plate_str_to_obj = {k.layout_name():k for k in source_plate}
plate_str_to_obj.update({'TargetPlate': target_plate})

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


def well_to_index_96(well: str):
    #split_str = list(well)
    letter = (ord(well[0]) - 65)
    number = (int(well[1:])-1)*8
    return letter + number

def worklist_96(file_path):

    target_dict = {}

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            target_plate = row[3]
            target_well = well_to_index_96(row[3])
            target_tuple = (plate_str_to_obj[target_plate], target_well)
            if target_tuple not in target_dict:
                target_dict.update({target_tuple:[]})

            source_plate = row[1]
            source_well = well_to_index_96(row[2])
            source_tuple = (plate_str_to_obj[source_plate], source_well)
            target_dict[target_tuple].append(source_tuple)

        return target_dict
        
def add_reagent(ham_int, source_well, target_well, vols_list):
    num_targets = target_well
    remaining_targets = num_targets
    while remaining_targets > 0:
        num_channels = 8 if remaining_targets >= 8 else remaining_targets
        completed_targets = num_targets - remaining_targets
        
        tips_poss = tips.get_tips(num_channels)
        tip_pick_up(ham_int, tips_poss)

        aspirate_poss = [(source_well, x) for x in range(num_channels)]
        vols_list = [250]*num_channels
        aspirate(ham_int, aspirate_poss, vols_list, liquidClass = liq_class)
        
        dispense_poss = [(target_well, x) for x in range(completed_targets, completed_targets + num_channels)]
        
        dispense(ham_int, dispense_poss, vols_list, mixCycles = 3, mixVolume = 100, liquidClass = liq_class)
        tip_eject(ham_int)
        remaining_targets -= num_channels
        



if __name__=='__main__':
    with HamiltonInterface(simulate=True) as ham_int: 
        initialize(ham_int)
        worklist_96('TEST_PY - WorkList - Copy(1).csv')
        add_reagent(ham_int, source_well = source_plate[0], target_well = target_plate[0], vols_list = 50)
=======
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 02:15:44 2023

@author: lUIZA
"""
import csv
from pyhamilton import (LayoutManager,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject,
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging,
 ResourceType)


lmgr = LayoutManager('deck_.lay')

source_plate = resource_list_with_prefix(lmgr, 'Mrx_96_DW_0001', Plate96, 1)
target_plate = resource_list_with_prefix(lmgr, 'Mrx_96_DW_0003', Plate96, 1)

plate_str_to_obj = {k.layout_name():k for k in source_plate}
plate_str_to_obj.update({'TargetPlate': target_plate})

def well_to_index_96(well: str):
    #split_str = list(well)
    letter = (ord(well[0]) - 65)
    number = (int(well[1:])-1)*8
    return letter + number

def worklist_96(file_path):

    target_dict = {}

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            target_plate = row[1]
            target_well = well_to_index_96(row[1])
            target_tuple = (plate_str_to_obj[target_plate], target_well)
            if target_tuple not in target_dict:
                target_dict.update({target_tuple:[]})

            source_plate = row[4]
            source_well = well_to_index_96(row[4])
            source_tuple = (plate_str_to_obj[source_plate], source_well)
            target_dict[target_tuple].append(source_tuple)

        return target_dict

if __name__=='__main__':
    a = worklist_96('TEST_PY - WorkList - Copy(1).csv')
>>>>>>> 780008592c60c8f2b19579fd0b1be72cdbba4211
