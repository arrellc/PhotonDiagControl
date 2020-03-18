from bsread import source
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime
# For PSEN Alvra

Camera_image = 'SARES11-SPEC125-M2:FPICTURE'
ROI_background = 'SARES11-SPEC125-M2.roi_background_x_profile'
ROI_signal = 'SARES11-SPEC125-M2.roi_signal_x_profile'
proc_para ='SARES11-SPEC125-M2.processing_parameters'

Channels = [Camera_image, ROI_background, ROI_signal, proc_para]
with source(channels=Channels) as stream:
    message = stream.receive()

exec('ProcPara='+message.data.data[proc_para].value)
imgShape =message.data.data[Camera_image].value.shape

plt.figure(figsize = [15,10])
plt.subplot(311)
plt.imshow(message.data.data[Camera_image].value)
plt.title(Camera_image+', pulse ID '+str(message.data.pulse_id)+'\n '+str(datetime.fromtimestamp(message.data.global_timestamp)))
Axis = plt.gca()
Axis.add_patch(Rectangle((ProcPara['roi_signal'][0],ProcPara['roi_signal'][2]),ProcPara['roi_signal'][1],ProcPara['roi_signal'][3], edgecolor = 'r', fill = False, linewidth = 3))
Axis.add_patch(Rectangle((ProcPara['roi_background'][0],ProcPara['roi_background'][2]),ProcPara['roi_background'][1],ProcPara['roi_background'][3], edgecolor = 'k', fill = False, linewidth = 3))


plt.subplot(312)
plt.plot(message.data.data[ROI_background].value, color = 'k')
plt.title('ROI background:'+str(ProcPara['roi_background']))
plt.grid(True)
plt.subplot(313)
plt.plot(message.data.data[ROI_signal].value, color = 'r')
plt.grid(True)
plt.title('ROI signal:'+str(ProcPara['roi_signal']))
plt.show()
