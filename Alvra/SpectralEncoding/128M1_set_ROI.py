from cam_server import PipelineClient
client = PipelineClient()

instance_id = "SARES12-CAMS128-M1_psen_db1"

# New parameters to set.

# [offset_x, size_x, offset_y, size_y] - the offsets are calculated from the top left corner of the image.

parameters = {
   "roi_background":[800, 450, 1300, 450],
   "roi_signal": [800, 450, 700, 450],
}

client.set_instance_config(instance_id, parameters)


