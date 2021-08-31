from Startuptools import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-dir", "--dirName", type=str)
parser.add_argument("-n", "--NumShots", type=int)
parser.add_argument("-d", "--ShortDeviceName", type=int)

args = parser.parse_args()

ShortDeviceName = str(args.ShortDeviceName)
NumShots = args.NumShots
dirName = args.dirName

#print('Device selected: '+ ShortDeviceName, +', number frames: %.1f'%NumShots + ', saving directory: ' +dirName)
print('Device selected: '+ ShortDeviceName)
#print('Device selected: '+ ShortDeviceName, +', number frames: %.1f'%NumShots)



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
