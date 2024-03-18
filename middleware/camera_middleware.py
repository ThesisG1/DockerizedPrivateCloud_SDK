# from ..ROS_Level import gen_node as node
import sys

sys.path.append("/home/g1/SDK/DockerizedPrivateCloud_SDK")
import ROS_Level.gen_node as node


class Namespace:
    def __init__(self, name, functions):
        self.namespace_name = name
        self.functions = functions

    # def generate_namespace(self, yaml):
    #     # Load YAML skeleton from file
    #     with open(yaml, 'r') as file:
    #         namespace = yaml.safe_load(file)

    #     self.namespace_name = namespace_info['namespace']['name']
    #     self.function_name = namespace_info['namespace']['functions']
    #     namespace_info = Namespace(name = self.namespace_name, functions = self.function_name)
    #     return namespace_info


class Middleware:

    def simulation_control(self, yml_file):
        gen_node = node.RosNodeGen()
        # this generates the ros nodes in the middleware
        node_name = gen_node.generate_node(yml_file)

    #         with open(f"{node_name}.py", "w") as file:
    #             file.write(f'''
    # import rospy
    # import json
    # import socketio
    # import os
    # ''')

    def camera_stream(self, sim_client, sim_stream):
        with open("simulation_stream.py", "w") as file:
            file.write(
                f"""import sys, os
from matplotlib import image
# import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
import socketio
import base64
import time


######
# Import any other necessary libraries
######
"""
            )

            file.write(
                f"""
def {sim_stream}():
   # IMPLEMENT YOUR FUNCTION HERE
   pass"""
            )
            file.write(
                f"""
class CVClient(object):
    def __init__(self, server_addr, stream_fps):
        self.server_addr = server_addr
        self.server_port = 8000
        self._stream_fps = stream_fps
        self._last_update_t = time.time()
        self._wait_t = (1/self._stream_fps)

    def _convert_image_to_jpeg(self, image):
        
        #frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{{}}".format(frame)

    def send_data(self, frame):
        cur_t = time.time()
        if cur_t - self._last_update_t > self._wait_t:
            self._last_update_t = cur_t
            sio.emit(
                    'cv2server',
                    {{
                        'image': self._convert_image_to_jpeg(frame),
                    }},namespace='/cv')

    def close(self):
        sio.disconnect()


sio = socketio.Client()


def convert_image_to_jpeg(image):
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{{}}".format(frame)

@sio.event(namespace='/cv')
def connect():
    global streamer
    streamer = CVClient('0.0.0.0', 5.0)
    print('[INFO] Successfully connected to server.')


@sio.event(namespace='/cv')
def connect_error():
    print('[INFO] Failed to connect to server.')


@sio.event(namespace='/cv')
def disconnect():
    print('[INFO] Disconnected from server.')
	
	
if __name__ == '__main__':
    sio.connect(os.path.expandvars('http://$HOST_IP:8000'))

    client = {sim_client}()
    {sim_stream}()
            """
            )
        file.close()


if __name__ == "__main__":
    middleware = Middleware()
    # g = airsim.VehicleClient()
    # middleware.camera_stream("airsim_VehicleClient","airsim_fetch")
    middleware.simulation_control("middleware_node.yml")
