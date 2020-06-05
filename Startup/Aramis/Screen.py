from Startuptools import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("ShortDeviceName", type=str)

# add more params here

args = parser.parse_args()

ShortDeviceName = args.ShortDeviceName
print('Device selected '+ ShortDeviceName)

########
# User inputs
dirName = '/sf/alvra/config/src/python/photodiag/PhotonDiagControl/Startup/Aramis/Data/040620'
NumShots = 100
# Get device parameters

Device_params = device_param(ShortDeviceName)
print(Device_params)

# Set file names

fN = dirName +'/'+Device_params['FullName']+'.h5'
figN =dirName +'/'+Device_params['FullName']+'.h5'
# Move screen in
screen_select(Device_params,1)

# Take images

DataOut = get_image(Device_params,NumShots)

# Display images

display_images(DataOut,figN[:-3])

# Save data

save_data(fN, DataOut)

# Move Screen out

screen_select(Device_params,0)
