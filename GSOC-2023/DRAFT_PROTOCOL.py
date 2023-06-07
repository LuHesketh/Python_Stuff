import argparse
import json
import os
import shutil
import subprocess
import sys

import sbol3
from tyto import OM



def generate_protocol():
    import labop

    doc = sbol3.Document()
    sbol3.set_namespace(NAMESPACE)

    #############################################
    # Import the primitive libraries
    # print("Importing libraries")
    labop.import_library("liquid_handling")
    # print("... Imported liquid handling")
    labop.import_library("plate_handling")
    # print("... Imported plate handling")
    labop.import_library("spectrophotometry")
    # print("... Imported spectrophotometry")
    labop.import_library("sample_arrays")
    # print("... Imported sample arrays")

    # create the materials to be provisioned
    PLASMID = sbol3.Component(
        "ddH2O", "https://identifiers.org/pubchem.substance:24901740"
    )
    PLASMID.name = "DNA TO BE PURIFIEd"

   Ethanol = sbol3.Component(
        "silica_beads",
        "https://nanocym.com/wp-content/uploads/2018/07/NanoCym-All-Datasheets-.pdf",
    )
    Ethanol.name = "Ethanol 70%, ideal for PCR/PLASMID PUTIFICATION"
    

    

    doc.add(PLASMID)
    doc.add(Ethanol)
    

    protocol = labop.Protocol(PROTOCOL_NAME)
    protocol.name = PROTOCOL_LONG_NAME
    protocol.version = "1.2"
    protocol.description = """
Protocol for PCR putification using a Hamilton and a MPE2 pressure pump module for ethanol washes
    """
    doc.add(protocol)

 provision = protocol.primitive_step(
        "Provision",
        resource=PLASMID,
        destination=PLASMID_container.output_pin("samples"),
        amount=sbol3.Measure(5000, OM.microliter),
    )

    provision = protocol.primitive_step(
        "Provision",
        resource=Ethanol,
        destination=Ethanol_container.output_pin("samples"),
        amount=sbol3.Measure(5000, OM.microliter),
    )


 ### Transfer DNA from source plate to MPE2 plate
    transfer1 = protocol.primitive_step(
        "Transfer",
        source=PLASMID_container.output_pin("samples"),
        destination=MPE2_wells_A1.output_pin("samples"),
        amount=sbol3.Measure(200, OM.microlitre),


     ### Transfer Ethanol from source plate to MPE2 plate for Ethanol washes

    )
    transfer2 = protocol.primitive_step(
        "Transfer",
        source=Ethanol_container.output_pin("samples"),
        destination=MPE2_wells_A1.output_pin("samples"),
        amount=sbol3.Measure(200, OM.microlitre),
    )