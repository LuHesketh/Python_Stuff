import os

from pyhamilton import (
    HamiltonInterface,
    LayoutManager,
    Plate96,
    Tip96,
    initialize,
    oemerr,
    normal_logging,
)

from pyhamilton import (
    mpe2_connect_com,mpe2_initialize,
    mpe2_stop_vacuum,
    mpe2_filter_plate_placed,
    mpe2_clamp_filter_plate,
    mpe2_process_filter_to_waste_container,
    mpe2_filter_plate_removed,mpe2_start_mpe_vacuum
)

liq_class = "StandardVolumeFilter_Water_DispenseJet_Part"


control_points = "pressure, 0, 0; pressure, 10, 5; pressure, 15, 5; pressure, 20, 5; pressure, 30, 5; pressure, 40, 5; pressure, 50, 5;  pressure, 60, 5"


lmgr = LayoutManager("MPEdeck.lay")

if __name__ == "__main__":
    with HamiltonInterface(simulate=True) as ham_int:
        initialize(ham_int)

        mpe2_id = mpe2_connect_com(ham_int, 12, 921600, simulation_mode=True, options=0)

        mpe2_id = int(mpe2_id.return_data[0])

        mpe2_initialize(ham_int, mpe2_id)

        mpe2_filter_plate_placed(ham_int,mpe2_id, 15, 15)
        mpe2_clamp_filter_plate(ham_int,mpe2_id)
        mpe2_start_mpe_vacuum(ham_int,mpe2_id, waste_container_id="", disable_vacuum_check="")
        mpe2_process_filter_to_waste_container(ham_int,mpe2_id,control_points = control_points,return_plate_to_integration_area="",waste_container_id="",disable_vacuum_check="")
        mpe2_stop_vacuum(ham_int, mpe2_id)
        mpe2_filter_plate_removed(ham_int, mpe2_id)

