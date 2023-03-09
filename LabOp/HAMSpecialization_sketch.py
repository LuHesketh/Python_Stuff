# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 12:26:43 2023

@author: Luiza
"""
import os
import json
import logging
import abc
from typing import Dict
from labop_convert.plate_coordinates import get_aliquot_list
import xarray as xr


import sbol3
import tyto
import labop
import uml
from labop_convert.behavior_specialization import BehaviorSpecialization


import pyhamilton
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, move_plate,
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging,
 ResourceType)



lmgr = LayoutManager('deck_.lay')

tips_res = lmgr.assign_unused_resource(ResourceType(Tip96, 'STF_L_0001'))
 
reagent_plate = lmgr.assign_unused_resource(ResourceType(Plate96, 'Mrx_96_DW_0001'))



class PyHamiltonSpecialization(BehaviorSpecialization):
       
    def __init__(self, filename, resolutions: Dict[sbol3.Identified,str] = None) -> None:
        super().__init__()
        self.resolutions = resolutions
        self.var_to_entity = {}
        self.script = ''
        self.script_steps = []
        self.markdown = ''
        self.markdown_steps = []
        self.apilevel = '2.11'
        self.configuration = {}
        self.filename = filename
        

    
    
    def define_container(self, record: labop.ActivityNodeExecution, ex: labop.ProtocolExecution):
        call = record.call.lookup()
        parameter_value_map = call.parameter_value_map()

        spec = parameter_value_map["specification"]['value']
        samples = parameter_value_map["samples"]['value']
        
# reagent_plate = lmgr.assign_unused_resource(ResourceType(Plate96, 'Mrx_96_DW_0001')) - how do I provide this informations?

     def provision(self, record: labop.ActivityNodeExecution, ex: labop.ProtocolExecution):
        results = {}
        call = record.call.lookup()
        parameter_value_map = call.parameter_value_map()
        destination = parameter_value_map["destination"]["value"]
        value = parameter_value_map["amount"]["value"].value
        units = parameter_value_map["amount"]["value"].unit
        units = tyto.OM.get_term_by_uri(units)
        resource = parameter_value_map["resource"]["value"]
        amount = parameter_value_map["amount"]["value"]
        amount = measurement_to_text(amount)
        coords = ''
        coords = destination.get_parent().get_parent().token_source.lookup().node.lookup().input_pin('coordinates').value.value
        upstream_execution = get_token_source('destination', record)
        container = upstream_execution.call.lookup().parameter_value_map()['container']['value']

        behavior_type = get_behavior_type(upstream_execution)
        if behavior_type == 'LoadContainerInRack':
            coords = upstream_execution.call.lookup().parameter_value_map()['coordinates']['value']
            upstream_execution = get_token_source('slots', upstream_execution)
            rack = upstream_execution.call.lookup().parameter_value_map()['specification']['value']
        else:
            raise NotImplementedError(f'A "Provision" call cannot follow a "{behavior_type}" call')

        container_str = f'`{container.name}`' if container.name else container.queryString
        rack_str = f'`{rack.name}`' if rack.name else rack.queryString
        text = f'Fill {amount} of {resource.name} into {container_str} located in {coords} of {rack_str}'
        self.markdown_steps += [text]