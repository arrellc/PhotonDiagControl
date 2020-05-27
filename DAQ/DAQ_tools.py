from cam_server import PipelineClient
from cam_server.utils import get_host_port_from_stream_address
from bsread import source, SUB
import numpy as np



def get_image(camName, ROI, numImg, angle):
    pipeline_client = PipelineClient()
    pipeline_config = {"camera_name": camName, "image_region_of_interest": ROI}
    pipeline_config = {"camera_name": camName,"rotation":angle}
    
    instance_id, pipeline_stream_address = pipeline_client.create_instance_from_config(pipeline_config)
    pipeline_host, pipeline_port = get_host_port_from_stream_address(pipeline_stream_address)
    img = []
    x_profile = []
    y_profile = []
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
            x_fwhm.append(data.data.data["x_fwhm"].value)
            y_fwhm.append(data.data.data["y_fwhm"].value)
            x_center_of_mass.append(data.data.data["x_center_of_mass"].value)
            intensity.append(data.data.data["intensity"].value)
            width.append(data.data.data["width"].value)
            height.append(data.data.data["height"].value)
    img = np.asarray(img)
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
        "height":height
    }
    return dataout
