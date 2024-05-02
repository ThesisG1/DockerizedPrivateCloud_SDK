import sys
sys.path.append("..")
import utilitiess.templates as templates
import utilitiess.parse as parser


class Database:
    def __init__(self, node_info):
        self.node_info = node_info
        with open(f"{self.node_info.node_name}_database.py", "w") as file:
            writer = templates.FileWriterr(file=file)
            file.write("""#___python lib__
from django.shortcuts import resolve_url
import requests
import json
from datetime import datetime
import mysql.connector
import random
#___src___
from django.db import connections\n\n""")
            writer.establish_DB_connection()
            writer.write_table_create(node_name = self.node_info.node_name + "_table")
            writer.write_table_insert(node_name = self.node_info.node_name + "_table")
            writer.write_table_search()
            