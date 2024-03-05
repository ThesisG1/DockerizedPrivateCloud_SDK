 
import rospy
from geometry_msgs.msg import Twist
import sys, select, os
from std_msgs.msg import String

def key_callback(data):
    print('IMPLEMENT CALLBACK key_callback')


def c_move(data):
    print('IMPLEMENT CALLBACK c_move')


def manga_cb(data):
    print('IMPLEMENT CALLBACK manga_cb')


rospy.init_node('leithy')
        
                
pub_1 = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
                
sub_1 = rospy.Subscriber('/control',String,key_callback)
                
sub_2 = rospy.Subscriber('/metric',String,c_move)
                
sub_3 = rospy.Subscriber('/manga',Twist,manga_cb)
                
rospy.spin()
                       