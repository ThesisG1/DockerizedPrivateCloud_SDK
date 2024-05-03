import rospy
from std_msgs.msg import String

import socketio
import os

def mariam_callback(data):
    print('IMPLEMENT CALLBACK mariam_callback')
 
    #emit your data on the dashboard namespace
    #sio.emit('Data', {data} ,namespace='/trial1_namespace')

sio = socketio.Client()
@sio.event(namespace='/trial1_namespace')
def connect(): 
    print('Successfully connected to the server')

@sio.event(namespace='/trial1_namespace')
def connect_error(): 
    print('Failed to connect to the server')

@sio.event(namespace='/trial1_namespace')
def disconnect(): 
    print('Disconnected from the server')

#Add the definition of your functions here as follows
#@sio.event(namespace='/trial1_namespace')
#def fn(data):
    #print('data')

rospy.init_node('trial1_mw')


mariam_sub = rospy.Subscriber('/mariam',String,mariam_callback)
            

control_pub = rospy.Publisher('/control', String, queue_size=10)


if __name__ == '__main__':
    sio.connect(os.path.expandvars('http://$HOST_IP:8000/trial1_namespace'))

    rospy.spin()
