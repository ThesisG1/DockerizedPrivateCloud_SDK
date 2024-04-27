import sys

sys.path.append("..")
import utilities.templates as templates
import utilities.parse as parser


class gen_actuate_views:
    def __init__(self, node_info):
        self.node_info = node_info
        with open(f"{self.node_info.node_name}_actuate_views.py", "w") as file:
            writer = templates.FileWriter(file=file)
            file.write(f"""from __future__ import unicode_literals
import socketio
import os


from django.shortcuts import redirect  # render ,
from django.template.response import TemplateResponse as render
from django.http import HttpResponse
from src.local_cloud.Query_Search import select_data, create_DB, actuate_DB
from src.local_cloud.qt_rcv import  rcv, actuateData
import json
from apps.home.views import sio


async_mode = None

basedir = os.path.dirname(os.path.realpath(__file__))
# sio = socketio.Server(async_mode='eventlet',cors_allowed_origins=['http://127.0.0.1:8000','http://localhost:8000','http://0.0.0.0:8000'])\\n\n""")

            writer.write_sio_web(name = self.node_info.node_name)
            writer.write_sio_cv(self)
            writer.write_sio_database(self)
            file.write(f"""def main(request):
    return render(request, "home/dashboard_layout.html")\n\n""")
            writer.write_update_data()
