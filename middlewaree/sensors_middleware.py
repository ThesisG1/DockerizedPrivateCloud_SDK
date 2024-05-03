from datetime import datetime
import rospy
from std_msgs.msg import String
from subprocess import call
import socketio
import json
import re
import math
import message_converter
import subprocess
#from django.db import connections
#import mysql.connector
import time
import os 
import subprocess
#Kinesis SDK
import boto3
import csv
import airsim



#Add your client here based on the simulator that you are using 
kinesis_client = airsim.VehicleClient()
#eg. kinesis_client = boto3.client('kinesis')


# data = {"sensor_name": "Accelerometer1",
# "linear_acceleartion_x": 1,
#  "linear_accelaration_y": 1,
#  "linear_acceleration_z": 1,
#  "magnitude": 7}

# data = {"sensor_name": "Speed1",
#   "linear_x" : 2,
# "linear_y" : 3,
# "linear_z" : 4,
# "angular_x" : 1,
# "angular_y" : 1,
# "angular_z" : 1,
# "magnitude": 0.2}

# data = { "sensor_name": "Position",
# "position_x":5000,
# "position_y":2000,
# "position_z":3000
# }


# def dbInit(db_host,db_user,db_password,data_base,server_addr):
#     server_addr = server_addr
#     server_port = 8000
#     mydb = mysql.connector.connect(
#     host=db_host,
#     user= db_user,
#     password=db_password,
#     database=data_base,
#     autocommit=True,
#     port = 3306
#     )
#     cursor = mydb.cursor()
#     print('[INFO] Connecting to server http://{}:{}...'.format(server_addr, server_port))
#     return cursor, mydb

# def dbSave(data):
#   cursor, mydb = dbInit("127.0.0.1","root","root","velanalytics","0.0.0.0")

  # cursor = connections["default"].cursor()
  # sql_statement = f"""INSERT INTO  {data["sensor_name"]}
  #               ( `time`,
  #               `value`)
  #               VALUES
  #               ({data["time"]},{data["magnitude"]});
  #               """
  # cursor.execute(sql_statement)

def callback(data):
  data = message_converter.convert_ros_message_to_dictionary(data)

  data = json.loads(data['data'])
  
  
  # cursor, mydb = dbInit("127.0.0.1","root","root","velanalytics","0.0.0.0")

  # cursor = connections["default"].cursor()
  # if "Position" in data["sensor_name"]:
  #   sql_statement = f"""INSERT INTO  {data["sensor_name"]}
  #                 ( `time`,
  #                 `lng`,
  #                 `lat`)
  #                 VALUES
  #                 ({data["time"]},{data["lng"]}, {data["lat"]});
  #                 """
  # else: 
  #   sql_statement = f"""INSERT INTO  {data["sensor_name"]}
  #                 ( `time`,
  #                 `value`)
  #                 VALUES
  #                 ({data["time"]},{data["magnitude"]});
  #                 """                    
  # cursor.execute(sql_statement)

  #timestamp here ----------------------


  # obj = time.gmtime(0)
  # epoch = time.asctime(obj)
  # print("The time is:",epoch)
  

  
  data = preprocessing(data)
  print(data)

  curr_time = round(time.time()*1000)
  print("Milliseconds since epoch:",curr_time)

  data["time"] = curr_time   
  #Send the data you got from sensors throgh ros node to the dashboard to update the graphs by emitting an event
  for i in range(5):
    sio.emit('sensedData', dict(data) ,namespace='/dashboard')

def preprocessing(data):
    global i 
    i+=1
    print(i)
    data["time"] = json.dumps(round(time.time()*1000), default=str)
    flag = False
    if(bool(re.search("^Accelerometer", data["sensor_name"]))):
      print("accelerometer")
      data = {"sensor_name" : data["sensor_name"],
            "magnitude" : data["magnitude"],
            "time": json.dumps(datetime.now(), default=str)
          }
      flag = True

      # dbSave(data)    

    elif(bool(re.search("^Speed", data["sensor_name"]))):
      print("speed")
      data = {"sensor_name" : data["sensor_name"],
              "magnitude" : data['magnitude'],
              "time": json.dumps(round(time.time()*1000), default=str),
              "y_axis_name" : "time"
            }
      flag = True
      

    if(bool(re.search("^Position", data["sensor_name"]))):
      print("position")
      data = {"sensor_name" : data["sensor_name"],
              "magnitude": data['magnitude'],
              "time": json.dumps(round(time.time()*1000), default=str)
            }
      flag = True

    else:  
      if(i==30):      
        # dbSave(data)
        i=0

    return data

def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/metric", String, callback) 
    rospy.spin()

sio = socketio.Client()


@sio.event(namespace='/dashboard')
def connect():
  print('[INFO] Successfully connected to server.')


@sio.event(namespace='/dashboard')
def connect_error():
  print('[INFO] Failed to connect to server.')


@sio.event(namespace='/dashboard')
def disconnect():
  print('[INFO] Disconnected from server.')

#new data recieved
@sio.event(namespace='/dashboard')
def data_Changed(data):
  print(data)

if __name__ == '__main__':
    sio.connect(os.path.expandvars('http://$HOST_IP:8000'))
    global i 
    i=0
    listener()