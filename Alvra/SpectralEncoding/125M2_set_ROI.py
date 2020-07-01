from cam_server import PipelineClient
client = PipelineClient()

instance_id = "SARES11-SPEC125-M2_psen_db1"

# New parameters to set.

# [offset_x, size_x, offset_y, size_y] - the offsets are calculated from the top left corner of the image.

parameters = {
   "roi_signal":[0, 2047, 1150, 400],
   "roi_background": [0, 2047, 500, 400],
}

client.set_instance_config(instance_id, parameters)


