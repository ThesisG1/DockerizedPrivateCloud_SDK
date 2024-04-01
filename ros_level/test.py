import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

def control_callback(data):
    print('IMPLEMENT CALLBACK control_callback')

def metric_callback(data):
    print('IMPLEMENT CALLBACK metric_callback')

def manga_callback(data):
    print('IMPLEMENT CALLBACK manga_callback')

rospy.init_node('test')


cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

control_sub = rospy.Subscriber('/control',String,control_callback)
            
metric_sub = rospy.Subscriber('/metric',String,metric_callback)
            
manga_sub = rospy.Subscriber('/manga',Twist,manga_callback)
            