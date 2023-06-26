# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:33:39 2023

@author: Luiza


"""

import json


Controlpoints = [   
     {  
          "Type": "pressure",                     vvvvvvvvvvvvvvvvv                
          "Value": 0,
          "Duration": 5
     },
     {  
          "Type": "pressure",
          "Value": 0,
          "Duration": 5
     },
     {  
          "Type": "pressure",   
          "Value": 0,
          "Duration": 5
     },
     {  
          "Type": "pressure",   
          "Value": 0,
          "Duration": 5
     },
     {  
          "Type": "pressure",
          "Value": 0,
          "Duration": 5
     },
     {  
          "Type": "pressure",
          "Value": 0,
          "Duration": 5
     },
 
     
]

json_string = json.dumps(Controlpoints, indent = 2)
with open('mydata.json', 'w') as f:
    f.write(json_string)
 