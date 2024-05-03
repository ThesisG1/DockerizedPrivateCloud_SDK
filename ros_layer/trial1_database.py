#___python lib__
from django.shortcuts import resolve_url
import requests
import json
from datetime import datetime
import mysql.connector
import random
#___src___
from django.db import connections

def dbInit(db_host,db_user,db_password,data_base,server_addr):
    server_addr = server_addr
    server_port = 8000
    mydb = mysql.connector.connect(
    host=db_host,
    user= db_user,
    password=db_password,
    database=data_base,
    autocommit=True,
    port = 3306
    )
    cursor = mydb.cursor()
    print('[INFO] Connecting to server http://{}:{}...'.format(server_addr, server_port))
    return cursor, mydb

def create_DB():
    cursor = connections["default"].cursor()
    create_trial1_table = """
        CREATE TABLE IF NOT EXISTS `trial1_table` (
            `col_1` date_type1,
            `col_2` date_type2,
            `col_3` date_type3,
            PRIMARY KEY (key) 
        )
    """
    cursor.execute(create_trial1_table)
    #Create the rest of the tables in the same way 

def insert_data():
    cursor = connections["default"].cursor()
    sql_statement = f"""INSERT INTO  `trial1_table`
                ( `time`,
                `value`)
                VALUES
                (%s,%s,%s), (%s,%s,%s);
                """
    cursor.execute(sql_statement)

def select_data():
    cursor = connections["default"].cursor()
                        
    # data to be sent to frontend
    historical_data = {}
                        
    # initializing sql_statement to be executed
    sql_statement = ""
                        
    #Add checks for your data here
    cursor.execute("Show tables;")
    tables = cursor.fetchall()
                        
    # conversting tuple to list
    all_tables = ([a_tuple[0] for a_tuple in all_tables])

    # neglecting django.migration table
    all_tables.remove("django_migrations")
                        
    # get time values from the first table in database
    cursor.execute(f"""SELECT time FROM {all_tables[1]}""" + sql_statement + ";")
    time = cursor.fetchall()
    time = ([a_tuple[0] for a_tuple in time])
    
    # add time data
    historical_data["time"] = time
                        
    # executing sql statements 
    for table in all_tables:
        # select value from tables 
        cursor.execute(f"""SELECT value FROM {table} """ + sql_statement)
        values = cursor.fetchall()
        # add all values 
        historical_data[table] = ([a_tuple[0] for a_tuple in values])
                        
    # try:
    #      cursor.execute(sql_statement)
    #       columns = [column[0] for column in cursor.description]
    #      for row in cursor.fetchall():
    #          data.append(dict(zip(columns, row)))
    # except Exception as e:
    #      print(e)   
                        
    return historical_data

