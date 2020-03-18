from cam_server import PipelineClient
client = PipelineClient()

instance_id = "SARES11-SPEC125-M1_psen_db1"

# New parameters to set.
parameters = {
   "roi_signal": [0,2048,270, 60],
   "roi_background": [0, 2048, 200, 150]
}

client.set_instance_config(instance_id, parameters)


