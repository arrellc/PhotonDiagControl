from cam_server import PipelineClient
from cam_server.utils import get_host_port_from_stream_address
from bsread import source, SUB
import numpy as np
import epics as ep
import matplotlib.pyplot as plt
from datetime import datetime
import h5py as h5

def device_param(deviceName):
    if deviceName == '053':
        FullName = 'SARFE10-PPRM053'
        BitDepth = 10
    if deviceName == '064':
        FullName = 'SARFE10-PPRM064'
        BitDepth = 12
    if deviceName == '078':
        FullName = 'SAROP11-PPRM078'
        BitDepth = 12
    if deviceName == '094':
        FullName = 'SAROP21-PPRM094'
        BitDepth = 12
    if deviceName == '097':
        FullName = 'SAROP21-PSCR097'
        BitDepth = 12
    if deviceName == '102':
        FullName = 'SAROP21-PPRM102'
        BitDepth = 12

    if deviceName == '110':
        FullName = 'SAROP11-PPRM110'
        BitDepth = 12
    if deviceName == '117':
        FullName = 'SAROP11-PPRM117'
        BitDepth = 12
    if deviceName == '122':
        FullName = 'SAROP11-PPRM122'
        BitDepth = 12
    else:
        print('Incorrect device name, use only last 3 digits, i.e for SARFE10-PPRM053 use 053')
        
    paramout ={
        'FullName': FullName,
        'BitDepth': BitDepth
    }
    return paramout

def get_image(Device_params, numImg, angle=None):
    if angle == None:
        angle =0
    pipeline_client = PipelineClient()
    # pipeline_config = {"camera_name": camName, "image_region_of_interest": ROI}
    pipeline_config = {"camera_name":Device_params['FullName'],"rotation":angle}

    instance_id, pipeline_stream_address = pipeline_client.create_instance_from_config(pipeline_config)
    pipeline_host, pipeline_port = get_host_port_from_stream_address(pipeline_stream_address)
    img = []
    x_profile = []
    y_profile = []
    x_fit_gauss_function = []
    y_fit_gauss_function = []
    x_fit_mean = []
    y_fit_mean = []
    x_fit_standard_deviation = []    
    y_fit_standard_deviation = []               
    x_fwhm = []
    y_fwhm = []
    x_center_of_mass = []
    y_center_of_mass = []
    intensity = []
    max_value = []
    width = []
    height = []
    with source(host=pipeline_host, port=pipeline_port, mode=SUB) as stream:
        for i in range(0,numImg):
            data = stream.receive()
            img.append(data.data.data["image"].value)
            x_profile.append(data.data.data["x_profile"].value)
            y_profile.append(data.data.data["y_profile"].value)
            x_fit_gauss_function.append(data.data.data["x_fit_gauss_function"].value)
            y_fit_gauss_function.append(data.data.data["y_fit_gauss_function"].value)
            x_fwhm.append(data.data.data["x_fwhm"].value)
            y_fwhm.append(data.data.data["y_fwhm"].value)
            x_center_of_mass.append(data.data.data["x_center_of_mass"].value)
            y_center_of_mass.append(data.data.data["y_center_of_mass"].value)
            x_fit_mean.append(data.data.data["x_fit_mean"].value)
            y_fit_mean.append(data.data.data["y_fit_mean"].value)
            x_fit_standard_deviation.append(data.data.data["x_fit_standard_deviation"].value)
            y_fit_standard_deviation.append(data.data.data["y_fit_standard_deviation"].value)
            intensity.append(data.data.data["intensity"].value)
            width.append(data.data.data["width"].value)
            height.append(data.data.data["height"].value)
            max_value.append(data.data.data["max_value"].value)

    print(list(data.data.data.keys()))
    img = np.asarray(img)
    # Take metedata
    PhotonEnergy = ep.caget('SARUN08-UIND030:FELPHOTENE.VAL')
    PulseEnergy = ep.caget('SARFE10-PBPG050:PHOTON-ENERGY-PER-PULSE-US')
    ATT053 = ep.caget('SARFE10-OATT053:TRANS_RB')
    APU044_x_pos = ep.caget('SARFE10-OAPU044:MOTOR_X.RBV')
    APU044_y_pos = ep.caget('SARFE10-OAPU044:MOTOR_Y.RBV') 
    APU044_w_pos = ep.caget('SARFE10-OAPU044:MOTOR_W.RBV')
    APU044_h_pos = ep.caget('SARFE10-OAPU044:MOTOR_H.RBV')

    dataout = {
        "mean": img.mean(axis=0),
        "image":img,
        "x_profile":x_profile,
        "y_profile":y_profile,
        "x_fwhm":x_fwhm,
        "y_fwhm":y_fwhm,
        "x_center_of_mass":x_center_of_mass,
        "y_center_of_mass":y_center_of_mass,
        "intensity":intensity,
        "max_value":max_value,
        "width":width,
        "height":height,
        "camera_name": Device_params['FullName'],
        "Bit_depth":Device_params['BitDepth'],
        "PhotonEnergy": PhotonEnergy,
        "PulseEnergy": PulseEnergy,
        "x_fit_gauss_function":x_fit_gauss_function,
        "y_fit_gauss_function":y_fit_gauss_function,
        "x_fit_mean":x_fit_mean,
        "y_fit_mean":y_fit_mean,
        "x_fit_standard_deviation":x_fit_standard_deviation,
        "y_fit_standard_deviation":y_fit_standard_deviation,
        "x_axis":data.data.data["x_axis"].value,
        "y_axis":data.data.data["y_axis"].value,
        "APU044_x_pos":APU044_x_pos,
        "APU044_y_pos":APU044_y_pos,
        "APU044_w_pos":APU044_w_pos,
        "APU044_h_pos":APU044_h_pos,
        "ATT053":ATT053
    }
    return dataout

def screen_select(Device_params, pos):
    print(Device_params['FullName'])
    screenPV= Device_params['FullName']+':PROBE_SP'
    ep.caput(screenPV, pos)

def norm(DataIn):
    return(DataIn/np.max(DataIn))

def display_images(DataOut, figN):
    # check if saturated
    maxValue = np.max(DataOut['max_value'])
    if maxValue>2**DataOut['Bit_depth']*.95:
        saturated = True
    else:
        saturated = False
    # set figure title
    if saturated:
        titleStr = DataOut['camera_name']+' SATURATED IMAGE'+'\n%.3f [keV], %.1f [uJ]'%(DataOut['PhotonEnergy'],DataOut['PulseEnergy'])
    else:
        titleStr = DataOut['camera_name']+'\n%.3f [keV], %.1f [uJ]'%(DataOut['PhotonEnergy'],DataOut['PulseEnergy'])
    
    # Set display text
    intensity_jitter = np.std(DataOut['intensity'])/np.mean(DataOut['intensity'])
    x_pos_jitter = np.std(DataOut['x_fit_mean'])/np.abs(np.mean(DataOut['x_fit_mean']))
    y_pos_jitter = np.std(DataOut['y_fit_mean'])/np.abs(np.mean(DataOut['y_fit_mean']))
    ATT053 = '\nATT053: %.3f'%DataOut['ATT053']
    APU044 = 'x: '+str(DataOut['APU044_x_pos'])+',y: '+str(DataOut['APU044_y_pos'])+',w: '+str(DataOut['APU044_w_pos'])+',h: '+str(DataOut['APU044_h_pos'])
    textStr = datetime.today().strftime('%Y-%m-%d,%H:%M')+'\nframes: %.1f'%len(DataOut['y_profile'])+'\nMax count: %.1f'%maxValue+'\nIntensity jitter std: %.4f'%intensity_jitter+'\nHoriz jitter std: %.4f'%x_pos_jitter+'\nVertical jitter std: %.4f'%y_pos_jitter+ATT053+'\nAPU044: '+APU044
    fileStr = 'Data saved: '+figN
    
    # max figure
    fig, axs = plt.subplots(2,4,figsize = [20,10])
    if saturated:
        plt.suptitle(titleStr, color= 'r')
    else:
        plt.suptitle(titleStr)
    # figure limits
    xlims = [np.mean(DataOut['x_fit_mean'])-4*np.mean(DataOut['x_fit_standard_deviation']),np.mean(DataOut['x_fit_mean'])+4*np.mean(DataOut['x_fit_standard_deviation'])]
    ylims = [np.mean(DataOut['y_fit_mean'])-4*np.mean(DataOut['y_fit_standard_deviation']),np.mean(DataOut['y_fit_mean'])+4*np.mean(DataOut['y_fit_standard_deviation'])]

    # populate plots
    axs[0,1].pcolormesh(DataOut['x_axis'], DataOut['y_axis'],DataOut['mean'], cmap='inferno')
    axs[0,1].set_xlim(xlims)
    axs[0,1].set_ylim(ylims)
    axs[0,1].set_yticks([])
    axs[0,1].set_xticks([])
    axs[0,1].set_title('Averaged frames: %.1f'%len(DataOut['y_profile']))

    axs[0,0].fill_betweenx(DataOut['y_axis'],np.mean(DataOut['y_profile'], axis =0)-np.std(DataOut['y_profile'], axis =0),np.mean(DataOut['y_profile'], axis =0)+np.std(DataOut['y_profile'], axis =0),alpha = 0.5)
    axs[0,0].plot(np.mean(DataOut['y_profile'], axis =0),DataOut['y_axis'])
    axs[0,0].plot(np.mean(DataOut['y_fit_gauss_function'], axis =0),DataOut['y_axis'])    
    axs[0,0].grid(True)
    axs[0,0].set_title('FWHM: %.1f [um], Fit mean: %.1f [um]'%(2.3*np.mean(DataOut['y_fit_standard_deviation']),np.mean(DataOut['y_fit_mean'])))
    axs[0,0].set_xticks([])
    axs[0,0].set_ylim(ylims)
    axs[0,0].set_ylabel('[um]')
    axs[0,0].invert_xaxis()
    
    axs[1,1].fill_between(DataOut['x_axis'],np.mean(DataOut['x_profile'], axis =0)-np.std(DataOut['x_profile'], axis =0),np.mean(DataOut['x_profile'], axis =0)+np.std(DataOut['x_profile'], axis =0),alpha = 0.5)
    axs[1,1].plot(DataOut['x_axis'],np.mean(DataOut['x_profile'], axis =0))
    axs[1,1].plot(DataOut['x_axis'],np.mean(DataOut['x_fit_gauss_function'], axis =0))
    axs[1,1].set_yticks([])
    axs[1,1].grid(True)
    axs[1,1].set_title('FWHM: %.1f [um], Fit mean: %.1f [um]'%(2.3*np.mean(DataOut['x_fit_standard_deviation']),np.mean(DataOut['x_fit_mean'])))
    axs[1,1].set_xlim(xlims)
    axs[1,1].set_xlabel('[um]')
    
    axs[1,0].hist(DataOut['intensity']/np.mean(DataOut['intensity']),100)
    axs[1,0].set_title('Intensity jitter')
    axs[1,0].set_xlabel('%')
    axs[1,0].grid(True)

    axs[0,2].hist(DataOut['x_fit_mean']/np.mean(DataOut['x_fit_mean']),100)
    axs[0,2].set_title('Horizontal jitter')
    axs[0,2].set_xlabel('%')
    axs[0,2].grid(True)

    axs[1,2].hist(DataOut['y_fit_mean']/np.mean(DataOut['y_fit_mean']),100)
    axs[1,2].set_title('Vertical jitter')
    axs[1,2].set_xlabel('%')
    axs[1,2].grid(True)

    axs[1,3].text(0.05,0.95,textStr, fontsize= 14, verticalalignment ='top', bbox = dict(boxstyle = 'round', facecolor = 'r', alpha = 0.5))
    axs[1,3].text(0.05,0.2,fileStr, fontsize =6,bbox = dict(boxstyle = 'round', facecolor = 'r', alpha = 0.5))

    axs[1,3].axis('off')
    
    axs[0,3].pcolormesh(DataOut['x_axis'], DataOut['y_axis'],DataOut['image'][0,:,:], cmap='inferno')
    axs[0,3].set_xlim(xlims)
    axs[0,3].set_ylim(ylims)
    axs[0,3].set_yticks([])
    axs[0,3].set_xticks([])
    axs[0,3].set_title('Single frame')
    
    plt.savefig(figN,dpi = 300)
    plt.show()

def save_data(fN,DataIn):
    with h5.File(fN,'w-') as fh:
        for k,v in DataIn.items():
            fh[k] = v
