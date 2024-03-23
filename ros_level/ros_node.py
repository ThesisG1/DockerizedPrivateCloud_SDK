import rospy
from geometry_msgs.msg import Twist
import sys, select, os
from std_msgs.msg import String
import sys

sys.path.append("..")
print("PATH: ", sys.path)
import utilities.templates as templates


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
            # parse imports types
            writer = templates.FileWriter(file=file)
            imports, types = self.parse_types(ros_node_info)
            # funciton to write the imports in the file
            writer.write_imports(imports, types)

            print(ros_node_info.node_subscribers)
            writer.callback_function(ros_node_info.node_subscribers)

            writer.init_node(ros_node_info.node_name)

            writer.write_publishers(ros_node_info.node_publishers)
            writer.write_subscribers(ros_node_info.node_subscribers)
        parse = self.parse_types(ros_node_info)

    # Parse the types found in the ['type'] field of the node_publishers and node_subscribers
    def parse_types(self, ros_node_info):
        imports = set()
        types = {}
        for i in range(len(ros_node_info.node_publishers)):
            type = ros_node_info.node_publishers[f"topic_{i+1}"]["type"]
            if "/" in type:
                import_type, type_name = type.split("/")
                imports.add(import_type)
                if import_type in types:
                    types[import_type].append(type_name)
                else:
                    types[import_type] = [type_name]

        for i in range(len(ros_node_info.node_subscribers)):
            type = ros_node_info.node_subscribers[f"topic_{i+1}"]["type"]

            if "/" in type:
                import_type, type_name = type.split("/")
                imports.add(import_type)
                if type in types:
                    types[import_type].append(type_name)
                else:
                    types[import_type] = [type_name]
        return imports, types
