from Startuptools import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("DeviceName", type=str)
# add more params here

args = parser.parse_args()

DeviceName = args.DeviceName
print('Screen selected '+ DeviceName)

# Move screen in
# screen_select(DeviceName,1)

# Take images

DataOut = get_image(DeviceName,10)

# Display images

display_images(DataOut)

