import epics as ep
from time import sleep


# define PVs
PMOS_spectrum_name = 'SATOP31-PMOS132-2D:SPECTRUM_Y'
PMOS_e_axis_name = 'SATOP31-PMOS132-2D:SPECTRUM_X'
PMOS_focus_name = 'SLAAT-GSLENS1:SET_CTS_POWER'
MONO_r2_name = 'SATOP11-OSGM087:EXITARM'
PMOS_screen_y_name = 'SATOP31-PMOS132:MOT_Y.VAL'
MONO_status_name = 'SATOP11-OSGM087:STATUS'

PMOS_spectrum_PV = ep.PV(PMOS_spectrum_name)
PMOS_screen_y_PV = ep.PV(PMOS_screen_y_name)
PMOS_e_axis_PV = ep.PV(PMOS_e_axis_name)
PMOS_focus_PV = ep.PV(PMOS_focus_name)
MONO_r2_PV = ep.PV(MONO_r2_name)
MONO_status_PV = ep.PV(MONO_status_name)


# motion functions
def set_PMOS_screen_y(val):
    PMOS_screen_y_PV.put(val,wait=True)
    print('it worked')
    sleep(1)
    
def set_PMOS_focus(val):
    PMOS_focus_PV.put(val,wait=True)
    sleep(1)  

def set_MONO_r2(val):
    MONO_r2_PV.put(val,wait=True)
    while MONO_status_PV.get() == 1:
        sleep(1)
    