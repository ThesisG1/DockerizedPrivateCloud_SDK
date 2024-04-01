import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String, String

import socketio
import os

def cmd_vel_callback(data):
    print('IMPLEMENT CALLBACK cmd_vel_callback')


sio = socketio.Client()
@sio.event(namespace='/mariam_namespace')
def connect(): 
    print('Successfully connected to the server')

@sio.event(namespace='/mariam_namespace')
def connect_error(): 
    print('Failed to connect to the server')

@sio.event(namespace='/mariam_namespace')
def disconnect(): 
    print('Disconnected from the server')

#Add the definition of your functions here as follows
#@sio.event(namespace='/mariam_namespace')
#def fn(data): 
    #print('data')

rospy.init_node('test')


cmd_vel_sub = rospy.Subscriber('/cmd_vel',Twist,cmd_vel_callback)
            
control_pub = rospy.Publisher('/control', String, queue_size=10)

metric_pub = rospy.Publisher('/metric', String, queue_size=10)

manga_pub = rospy.Publisher('/manga', Twist, queue_size=10)

if __name__ == '__main__':
    sio.connect(os.path.expandvars('http://$HOST_IP:8000/mariam_namespace'))

    rospy.spin()
