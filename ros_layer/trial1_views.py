from __future__ import unicode_literals
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
# sio = socketio.Server(async_mode='eventlet',cors_allowed_origins=['http://127.0.0.1:8000','http://localhost:8000','http://0.0.0.0:8000'])\n
                       
def connectionState(state):
    if state == 0:
        global isConnected
        isConnected = False
    elif state == 1:
        isConnected = True

connectionState(0) #setting connection with QT at first with false to render page without charts

def main(request):
    return render(request, "home/dashboard_layout.html")


@sio.on('connect', namespace='/web')
def connect_web(sid, data):
    print('[INFO] Web client connected: {}'.format(sid))

@sio.on('disconnect', namespace='/web')
def disconnect_web(sid):
    print('[INFO] Web client disconnected: {}'.format(sid))

@sio.on('new_data', namespace='/web')
#Add the definition of your functions here as follows use the fn you created in Middleware
#def newData(sid, data):
    #sio.emit('#fn', data, namespace='/trial1_namespace')


@sio.on('connect', namespace='/cv')
def connect_cv(sid, data):
    print('[INFO] CV client connected: {}'.format(sid))

@sio.on('disconnect', namespace='/cv')
def disconnect_cv(sid):
    print('[INFO] CV client disconnected: {}'.format(sid))

@sio.on('cv2server',namespace='/cv')
def handle_cv_message(sid,message):
    sio.emit('server2web', message, namespace='/web')


@sio.on('connect', namespace='/dynamicDB')
def connect_QT(sid,data):
    print("Hi from".format(sid))
    print('[INFO] Create_DynamicDB connected: {}'.format(sid))


def render_data_fn(request):
    if request.is_ajax():
        #data = request.POST.get('data')
        #Implement the rest of your function here
        return render(request, "template")         #Add your own template e.g. "sense/historicaldata.html"

