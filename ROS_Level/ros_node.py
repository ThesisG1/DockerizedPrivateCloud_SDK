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
            #parse imports types
            imports, types = self.parse_types(ros_node_info)
#write all the imports to the file
            file.write(

                f''' 
import rospy

''')
            #write imports based on the parsed types
            for imp in imports:
                file.write(f"from {imp}.msg import {', '.join(types[imp])}\n")
            file.write("\n")
            
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
{name}_pub = rospy.Publisher('/{name}', {type.split("/")[-1]}, queue_size=10)
                '''
            )
            
            for i in range(len(ros_node_info.node_subscribers)): 
                name = ros_node_info.node_subscribers[f'topic_{i+1}']['name']
                type = ros_node_info.node_subscribers[f'topic_{i+1}']['type']
                callback = ros_node_info.node_subscribers[f'topic_{i+1}']['callback']
                file.write(

                f'''
{name}_sub = rospy.Subscriber('/{name}',{type.split("/")[-1]},{callback})
                '''
            )
            
            file.write('''
rospy.spin()
                       ''')
        parse = self.parse_types(ros_node_info)

    #Parse the ypes found in the ['type'] field of the node_publishers and node_subscribers
    def parse_types(self, ros_node_info):
        imports = set()
        types = {}
        for i in range(len(ros_node_info.node_publishers)):
            type = ros_node_info.node_publishers[f'topic_{i+1}']['type']
            if '/' in type:
                import_type, type_name = type.split('/')
                imports.add(import_type)
                if import_type in types:
                    types[import_type].append(type_name)
                else:
                    types[import_type] = [type_name]

        for i in range(len(ros_node_info.node_subscribers)):
            type = ros_node_info.node_subscribers[f'topic_{i+1}']['type']

            if '/' in type:
                import_type, type_name = type.split('/')
                imports.add(import_type)
                if type in types:
                    types[import_type].append(type_name)
                else:
                    types[import_type] = [type_name]
        return imports, types
    
        

   


