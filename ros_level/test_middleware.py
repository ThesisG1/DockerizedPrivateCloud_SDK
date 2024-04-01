import rospy
from std_msgs.msg import String, String
from geometry_msgs.msg import Twist

def cmd_vel_callback(data):
    print('IMPLEMENT CALLBACK cmd_vel_callback')

rospy.init_node('test')


cmd_vel_sub = rospy.Subscriber('/cmd_vel',Twist,cmd_vel_callback)
            
control_pub = rospy.Publisher('/control', String, queue_size=10)

metric_pub = rospy.Publisher('/metric', String, queue_size=10)

manga_pub = rospy.Publisher('/manga', Twist, queue_size=10)
