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
    from labop_convert import DefaultBehaviorSpecialization

    doc = sbol3.Document()
    sbol3.set_namespace("http://labop.io/")

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
    
    PROTOCOL_NAME = "simple_transfer"
    PROTOCOL_LONG_NAME="simple_transfer"
    protocol = labop.Protocol(PROTOCOL_NAME)
    protocol.name = PROTOCOL_LONG_NAME
    protocol.version = "1.2"
    protocol.description = """
 protocol to transfer plasmid and ethanol to a MPE container
    """
    doc.add(protocol)
    
    
    PLASMID_container = protocol.primitive_step(
        "EmptyContainer",
        specification=labop.ContainerSpec(
            "PLASMID",
            name="PLASMID",
            queryString="cont:StockReagent",
            prefixMap={
                "cont": "https://sift.net/container-ontology/container-ontology#"
            },
        ),
    )


    Ethanol_container = protocol.primitive_step(
        "EmptyContainer",
        specification=labop.ContainerSpec(
            "sulforhodamine_calibrant",
            name="Sulforhodamine 101 calibrant",
            queryString="cont:StockReagent",
            prefixMap={
                "cont": "https://sift.net/container-ontology/container-ontology#"
            },
        ),
    )

        
        
    MPE_container = protocol.primitive_step(
        "EmptyContainer",
        specification=labop.ContainerSpec(
            "PLASMID_container",
            name="LASMID_container",
            queryString="cont:StockReagent",
            prefixMap={
                "cont": "https://sift.net/container-ontology/container-ontology#"
            },
        ),
    )
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
    MPE2_wells_A1 = protocol.primitive_step(
        "PlateCoordinates",
        source=MPE_container.output_pin("samples"),
        coordinates="A1",
    )

    ### Transfer PLASMID from source plate to MPE2 plate
    transfer_PLASMID = protocol.primitive_step(
        "Transfer",
        source=PLASMID_container.output_pin("samples"),
        destination=MPE2_wells_A1.output_pin("samples"),
        amount=sbol3.Measure(20, OM.microlitre),


    ### Transfer Ethanol from source plate to MPE2 plate for Ethanol washes

    )
    transfer_ethanol = protocol.primitive_step(
        "Transfer",
        source=Ethanol_container.output_pin("samples"),
        destination=MPE2_wells_A1.output_pin("samples"),
        amount=sbol3.Measure(200, OM.microlitre),
    )

    protocol.to_dot().view()


    OUT_DIR="."
    ee = labop.ExecutionEngine(
        out_dir=OUT_DIR,
        failsafe=False,
        # specializations=[PyHamiltonSpecialization()]
        sample_format="xarray"
    )

    execution = ee.execute(
        protocol,
        sbol3.Agent("test_agent"),
        id="test_execution",
        parameter_values=[],
    )
    ee.prov_observer.to_dot().view()

if __name__ == "__main__":
    generate_protocol()
