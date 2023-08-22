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
    mpe2_filter_plate_placed,
    mpe2_clamp_filter_plate,
    mpe2_process_filter_to_waste_container,
    mpe2_filter_plate_removed,mpe2_disconnect
)

liq_class = "StandardVolumeFilter_Water_DispenseJet_Part"

com_port = "12"
baud_rate = "921600"
control_points = "pressure, 0, 5;pressure, 10, 5;pressure, 15, 5;pressure, 20, 5;pressure, 30, 5;pressure, 40, 5;pressure, 50, 5; pressure, 60, 5"
filter_height = "14.9"
nozzle_height = "14.9"
lmgr = LayoutManager("MPEdeck.lay")

if __name__ == "__main__":
    with HamiltonInterface(simulate=False) as ham_int:
        initialize(ham_int)

        mpe2_id = mpe2_connect_com(ham_int, com_port, baud_rate, simulation_mode=True, options=0)

        mpe2_id = int(mpe2_id.return_data[0])

        mpe2_initialize(ham_int, mpe2_id)
        mpe2_filter_plate_placed(ham_int,mpe2_id, filter_height, nozzle_height)
        mpe2_clamp_filter_plate(ham_int,mpe2_id)
        mpe2_filter_plate_placed(ham_int,mpe2_id, filter_height, nozzle_height)
        mpe2_process_filter_to_waste_container(ham_int,mpe2_id,control_points = control_points,return_plate_to_integration_area="1",waste_container_id="0",disable_vacuum_check="1")
        mpe2_filter_plate_removed(ham_int, mpe2_id)
        mpe2_disconnect(ham_int, mpe2_id)
