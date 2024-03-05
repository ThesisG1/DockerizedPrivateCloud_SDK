import rospy
from geometry_msgs.msg import Twist
import sys, select, os
from std_msgs.msg import String


class ROSNodeInfo:
    def __init__(self, node_name, node_subscribers, node_publishers):
        self.node_name = node_name
        self.node_subscribers = node_subscribers
        self.node_publishers = node_publishers



class Node:
    def __init__(self, ros_node_info):  # Constructor
        with open(f"{ros_node_info.node_name}.py", "w") as file:
            pass  # Using pass statement since we don't need to write anything
        self.nodeInfo = ros_node_info
        with open(f"{ros_node_info.node_name}.py", "a") as file:

            file.write(

                f''' 
import rospy
from geometry_msgs.msg import Twist
import sys, select, os
from std_msgs.msg import String
''')
            print(ros_node_info.node_subscribers)
            for i in range(len(ros_node_info.node_subscribers)):
                name = ros_node_info.node_subscribers[f'topic_{i+1}']['name']
                callback = ros_node_info.node_subscribers[f'topic_{i+1}']['callback']
                file.write(f'''
def {callback}(data):
    print('IMPLEMENT CALLBACK {callback}')

''')
            file.write(f'''
rospy.init_node('{ros_node_info.node_name}')
        
                '''
            )

            for i in range(len(ros_node_info.node_publishers)): 
                name = ros_node_info.node_publishers[f'topic_{i+1}']['name']
                type = ros_node_info.node_publishers[f'topic_{i+1}']['type']
                file.write(

                f'''
pub_{i+1} = rospy.Publisher('{name}', {type}, queue_size=10)
                '''
            )
            
            for i in range(len(ros_node_info.node_subscribers)): 
                name = ros_node_info.node_subscribers[f'topic_{i+1}']['name']
                type = ros_node_info.node_subscribers[f'topic_{i+1}']['type']
                callback = ros_node_info.node_subscribers[f'topic_{i+1}']['callback']
                file.write(

                f'''
sub_{i+1} = rospy.Subscriber('{name}',{type},{callback})
                '''
            )
            
            file.write('''
rospy.spin()
                       ''')

        

   


