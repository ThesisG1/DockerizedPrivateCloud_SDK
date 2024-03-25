import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist


def key_callback(data):
    print("IMPLEMENT CALLBACK key_callback")


def c_move(data):
    print("IMPLEMENT CALLBACK c_move")


def manga_cb(data):
    print("IMPLEMENT CALLBACK manga_cb")


rospy.init_node("test")


control_sub = rospy.Subscriber("/control", String, key_callback)

metric_sub = rospy.Subscriber("/metric", String, c_move)

manga_sub = rospy.Subscriber("/manga", Twist, manga_cb)

cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
