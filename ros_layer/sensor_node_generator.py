# import rospy
# from geometry_msgs.msg import Twist
# import sys, select, os
# from std_msgs.msg import String
# import sys

# sys.path.append("..")
# print("PATH: ", sys.path)
# import utilitiess.templates as templates
# import utilitiess.parse as parser


# class ROSNodeInformation:
#     def __init__(self, node_name, node_subscribers, node_publishers, flow_flag):
#         self.node_name = node_name
#         self.flow_flag = flow_flag
#         self.node_subscribers = node_subscribers
#         self.node_publishers = node_publishers


# class Node:
#     def __init__(self, ros_node_info):  # Constructor
#         with open(f"{ros_node_info.node_name}.py", "w") as file:
#             pass  # Using pass statement since we don't need to write anything
#         self.nodeInfo = ros_node_info
#         with open(f"{ros_node_info.node_name}.py", "a") as file:
#             # parse imports types
#             writer = templates.FileWriterr(file=file)
#             imports, types = parser.Parser.parse_types(ros_node_info)
#             # funciton to write the imports in the file
#             writer.write_imports(imports, types)

#             print(ros_node_info.node_subscribers)
#             #writer.callback_function(ros_node_info.node_subscribers)
#             file.write(f"""
# from pickle import NONE
# import rospy
# from std_msgs.msg import String
# from geometry_msgs.msg import Twist
# from sensor_msgs.msg import Imu,NavSatFix
# from nav_msgs.msg import Odometry
# import json
# import time

# last_speed=0
# last_acceleration=0

# def send_dictionary(dictionary,topic):
#     pub = rospy.Publisher(topic, String, queue_size=50)
#     rate = rospy.Rate(10) # 10hz
#     encoded_data_string = json.dumps(dictionary)
#     pub.publish(encoded_data_string)    
#     rate.sleep()

# def cmd_vel_callback(msg):
#     speed_dict = {{}}
#     global last_speed
#     speed_dict['sensor_name'] = 'Speed_Digital1'
#     # speed_dict['linear_x'] = msg.linear.x
#     # speed_dict['linear_y'] = msg.linear.y
#     # speed_dict['linear_z'] = msg.linear.z
#     # speed_dict['angular_x'] = msg.angular.x
#     # speed_dict['angular_y'] = msg.angular.y
#     # speed_dict['angular_z'] = msg.angular.z
#     speed_dict['magnitude'] = (((msg.linear.x)**2 + (msg.linear.y)**2)**0.5)*10
#     if(speed_dict['magnitude']==last_speed):
#         return
#     else:
#         last_speed=speed_dict['magnitude']
#         # print (speed_dict['magnitude'])

#         send_dictionary(speed_dict,'metric')

# def pose_callback(msg):
#     position_dict = {{}}
#     position_dict['sensor_name'] = 'Position_Digital_1'
#     # position_dict['position_x'] = msg.pose.pose.position.x
#     # position_dict['position_y'] = msg.pose.pose.position.y
#     # position_dict['position_z'] = msg.pose.pose.position.z
#     position_dict['magnitude'] = msg.latitude
#     position_dict['position_y'] = msg.longitude
#     position_dict['position_z'] = msg.altitude
#     print (position_dict['magnitude'])
#     # encoded_data_string = json.dumps(position_dict)
#     # print('json',encoded_data_string)
#     send_dictionary(position_dict,'metric')
#     # loaded_dictionary = json.loads(encoded_data_string)
#     # print('dict',loaded_dictionary)



# n = 0
# linear_acc_x = 0
# linear_acc_y = 0
# linear_acc_z = 0
# def acc_callback(msg):
#     acc_dict = {{}}
#     global linear_acc_x,linear_acc_y,linear_acc_z,n,last_acceleration
#     linear_acc_x += msg.linear_acceleration.x
#     linear_acc_y += msg.linear_acceleration.y
#     linear_acc_z += msg.linear_acceleration.z
#     n+=1
#     acc_dict['sensor_name'] = 'Accelerometer_Digital1'
#     # acc_dict['linear_acceleration_x'] = linear_acc_x / n
#     # acc_dict['linear_acceleration_y'] = linear_acc_y / n
#     # acc_dict['linear_acceleration_z'] = linear_acc_z / n
#     acc_dict['magnitude'] = int((linear_acc_x*10000))
    
#     dif = abs(acc_dict['magnitude'] - last_acceleration)
#     #print(dif)
#     # acc_dict['magnitude'] = int((((linear_acc_x/n)**2 + (linear_acc_y/n)**2)**0.5)*100000)
#     if(acc_dict['magnitude']==last_acceleration or dif<100 or n<40): 
#         return
    
#     else:
#         last_acceleration=acc_dict['magnitude']
#         send_dictionary(acc_dict,'metric')
#         # print (acc_dict['magnitude'])
    

#     if n == 30:
#         linear_acc_x = linear_acc_y = linear_acc_z = n = 0 \n\n""")

#             writer.init_node(ros_node_info.node_name)
#             writer.write_publishers(ros_node_info.node_publishers)
#             writer.write_subscribers(ros_node_info.node_subscribers)
#             file.write(f"""if __name__ == '__main__':\n""")  
#             file.write(f"""    rospy.spin()""")
#         parse = parser.Parser.parse_types(ros_node_info)
