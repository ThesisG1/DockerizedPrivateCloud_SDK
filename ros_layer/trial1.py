import rospy
from std_msgs.msg import String

def control_callback(data):
    print('IMPLEMENT CALLBACK control_callback')
rospy.init_node('trial1')


mariam_pub = rospy.Publisher('/mariam', String, queue_size=10)


control_sub = rospy.Subscriber('/control',String,control_callback)
            
if __name__ == '__main__':
    rospy.spin()