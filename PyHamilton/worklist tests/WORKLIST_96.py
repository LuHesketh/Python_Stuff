# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:40:22 2023

@author: Luiza
"""
import pyhamilton
from pyhamilton import (HamiltonInterface, initialize, tip_pick_up, 
                        LayoutManager, resource_list_with_prefix, Tip96, 
                        Plate96, ResourceType, aspirate, dispense, tip_eject)

from WORKLIST96_extra_necessities.py import (worklist_96, target_plate, source_plates, lmgr)
import sys
from functools import partial
from collections import OrderedDict
import time
from tabulate import tabulate
from prettytable import PrettyTable


def debug_print_disp(ad_tuple):
    table = [[(ad_tuple[0][x][0].layout_name(),ad_tuple[0][x][1]),(ad_tuple[1][x][0].layout_name(),ad_tuple[1][x][1])] for x in range(len(ad_tuple[0]))]
    print(tabulate(table, headers=['Aspirations', 'Dispense']))

def debug_print_cols(cols_2_tuple, headers):
    table = [[cols_2_tuple[0][x], cols_2_tuple[1][x]] for x in range(len(cols_2_tuple[0]))]

def debug_print_wl_map(target_dict):
    a = {(k[0].layout_name(), k[1]):[(i[0].layout_name(), i[1]) for i in v] for (k,v) in target_dict.items()}
    print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in a.items()) + "}")


def get_96wp_columns(plate_list, start, end):
    cols_list = []
    for i in range(12):
        valid_cols = [(plate_list[plate_idx], j) for plate_idx in range(start, end) for j in range(i*8, (i+1)*8)]
        cols_list.append(valid_cols)
    return cols_list

def get_columns_from_deck(plate_list, carrier_max_plates):
    deck_columns = []
    num_plates = len(plate_list)
    for carrier_idx in range(num_plates//carrier_max_plates):
        plate_idx = carrier_idx*carrier_max_plates 
        deck_columns += get_96wp_columns(plate_list, plate_idx, plate_idx + carrier_max_plates)
    plate_idx = plate_idx + carrier_max_plates
    remainder_plate_idx =  plate_idx + num_plates%carrier_max_plates
    deck_columns += get_96wp_columns(plate_list, plate_idx, remainder_plate_idx )
    return deck_columns

def full_column_from_well(well, plate_list, carrier_max_plates):
    deck_columns = get_columns_from_deck(plate_list, carrier_max_plates)
    for col in deck_columns:
        if well in col:
            return col


def get_well_index(well_tup):
    return int(well_tup[0].layout_name()[-1])*96+int(well_tup[1])


def sort_wells_by_plate_idx(plate_list):
    plate_list = plate_list.sorted(key=get_well_index)
    return plate_list

def target_cols_from_dict(target_cols, current_target_dict):
    active_target_cols = []
    for target_col in target_cols:
        active_target_col = []
        for target_well in target_col:
            if target_well in current_target_dict:
                active_target_col.append(target_well)
        if len(active_target_col)>0:
            active_target_cols.append(active_target_col)
    return active_target_cols


def debug_print_target_map(well, tcol, wl_map):
    x = PrettyTable()
    x.field_names = ['Target Column']
    x.add_rows([[twell] if twell!=well else [twell, '\u001b[37m'] for twell in tcol])
    print(x)

def disp_poss_from_dict(active_target_dict, tcol):
    
    asp_poss = []
    disp_poss = []
    last_well_index = 0
    for well in tcol:
        if well in active_target_dict:
            tgt = well
            if len(active_target_dict[tgt])==0:
                active_target_dict.pop(well)
                continue
            src_col = sorted(active_target_dict[tgt], key = get_well_index)
            src_col = [well for well in src_col if get_well_index(well)>last_well_index]
            if len(src_col)==0:
                continue
            src = src_col[0]
            last_well_index = get_well_index(src)
            asp_poss.append(src)
            disp_poss.append(tgt)
            active_target_dict[well].remove(src)
            if len(active_target_dict[well]) == 0:
                active_target_dict.pop(well)
        if len(asp_poss) == 8:
            return active_target_dict, asp_poss, disp_poss
    return active_target_dict, asp_poss, disp_poss

def enum_disp_from_cols(col_target_dict, tcol):
    list_disps = []
    while len(col_target_dict)>0:
        print("Column-intersect worklist map")
        debug_print_wl_map(col_target_dict)
        col_target_dict, asp_poss, disp_poss = disp_poss_from_dict(col_target_dict, tcol)
        ad_2_tuple = [asp_poss, disp_poss]
        print('\n')
        print("Aspiration and dispense pairs")
        debug_print_disp(ad_2_tuple)
        print('\n')
        print('\n')
        list_disps.append(ad_2_tuple)
    return list_disps

def dispense_lists_from_wl(current_target_dict, target_cols, source_cols):
    list_of_dispense_lists = []
    for tcol in target_cols:
        tcol = set([well for well in current_target_dict]) & set(tcol)
        tcol = sorted(tcol, key = get_well_index)
        for scol in source_cols:
            col_target_dict = {well: list(set(current_target_dict[well]) & set(scol)) for well in tcol}
            list_disps = enum_disp_from_cols(col_target_dict, tcol)
            list_of_dispense_lists += list_disps
    return list_of_dispense_lists


lmgr = LayoutManager('deck_.lay')
wl = worklist_96('TEST_PY - WorkList - Copy(1).csv')
current_target_dict = wl.copy()
target_cols = get_96wp_columns([target_plate], 0, 1)

source_cols = get_columns_from_deck(source_plates)

dl = dispense_lists_from_wl(current_target_dict, target_cols, source_cols)


tips = lmgr.assign_unused_resource(ResourceType(Tip96, 'STF_L_0001'))
tips_list = [(tip_box, idx) for tip_box in tips for idx in range(96)]

def tips_list_iterator(asp_list, tips_list):
    asp_list =  asp_list + [None]*(8-len(asp_list))
    pickup_list = []
    for i in range(8):
        if asp_list[i]:
            first_tip = [tip for tip in tips_list if tip][0]
            tips_list[tips_list.index(first_tip)] = None
            pickup_list.append(first_tip)
        else:
            pickup_list.append(None)
    return pickup_list, tips_list



    
if __name__=='__main__':
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)
        for ad_2_tuple in dl:
            asp_list = ad_2_tuple[0]
            disp_list = ad_2_tuple[1]
            pickup_list, tips_list = tips_list_iterator(asp_list, tips_list)
            tip_pick_up(ham_int, pickup_list)
            vols = [25 for x in disp_list if x!=None]
            aspirate(ham_int, asp_list, vols, liquidClass = 'StandardVolumeFilter_Water_DispenseJet_Part')
            dispense(ham_int, disp_list, vols, liquidClass = 'StandardVolumeFilter_Water_DispenseJet_Part')
            time.sleep(5)
            tip_eject(ham_int)
            
            
            
            