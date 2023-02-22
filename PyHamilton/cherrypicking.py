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