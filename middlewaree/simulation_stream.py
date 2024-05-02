import sys, os
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


def airsim_fetch():
    # IMPLEMENT YOUR FUNCTION HERE
    pass


class CVClient(object):
    def __init__(self, server_addr, stream_fps):
        self.server_addr = server_addr
        self.server_port = 8000
        self._stream_fps = stream_fps
        self._last_update_t = time.time()
        self._wait_t = 1 / self._stream_fps

    def _convert_image_to_jpeg(self, image):

        # frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Encode frame as jpeg
        frame = cv2.imencode(".jpg", image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        frame = base64.b64encode(frame).decode("utf-8")
        return "data:image/jpeg;base64,{}".format(frame)

    def send_data(self, frame):
        cur_t = time.time()
        if cur_t - self._last_update_t > self._wait_t:
            self._last_update_t = cur_t
            sio.emit(
                "cv2server",
                {
                    "image": self._convert_image_to_jpeg(frame),
                },
                namespace="/cv",
            )

    def close(self):
        sio.disconnect()


sio = socketio.Client()


def convert_image_to_jpeg(image):
    # Encode frame as jpeg
    frame = cv2.imencode(".jpg", image)[1].tobytes()
    # Encode frame in base64 representation and remove
    # utf-8 encoding
    frame = base64.b64encode(frame).decode("utf-8")
    return "data:image/jpeg;base64,{}".format(frame)


@sio.event(namespace="/cv")
def connect():
    global streamer
    streamer = CVClient("0.0.0.0", 5.0)
    print("[INFO] Successfully connected to server.")


@sio.event(namespace="/cv")
def connect_error():
    print("[INFO] Failed to connect to server.")


@sio.event(namespace="/cv")
def disconnect():
    print("[INFO] Disconnected from server.")


if __name__ == "__main__":
    sio.connect(os.path.expandvars("http://$HOST_IP:8000"))

    #Change the client here to be relevant to the simulator you are using
    client = airsim_VehicleClient()
    airsim_fetch()
