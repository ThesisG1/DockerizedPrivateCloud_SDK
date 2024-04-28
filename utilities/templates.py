# TODO: Write the lines of codes from the generator files into variables and functions
# Example:
class FileWriter:
    def __init__(self, file):
        self.file = file

    def callback_function(self, subscribers):
        for sub in subscribers:
            name = subscribers[sub]["name"]
            callback = name + "_callback"
            self.file.write(
                f"""def {callback}(data):
    print('IMPLEMENT CALLBACK {callback}')\n"""
            )
            self.file.write("\n")

    # return callback

    def write_imports(self, imports, types):
        self.file.write(f"""import rospy\n""")
        # write imports based on the parsed types
        for imp in imports:
            self.file.write(f"""from {imp}.msg import {', '.join(types[imp])}\n""")
        self.file.write("\n")

    def init_node(self, node_name):
        self.file.write(f"""rospy.init_node('{node_name}')\n""")
        self.file.write("\n")

    def write_publishers(self, publishers):
        for pub in publishers:
            name = publishers[pub]["name"]
            type = publishers[pub]["type"]
            self.file.write(
                f"""
{name}_pub = rospy.Publisher('/{name}', {type.split("/")[-1]}, queue_size=10)\n"""
            )

    def write_subscribers(self, subscribers):
        for sub in subscribers:
            name = subscribers[sub]["name"]
            type = subscribers[sub]["type"]
            callback = name + "_callback"
            self.file.write(
                f"""
{name}_sub = rospy.Subscriber('/{name}',{type.split("/")[-1]},{callback})
            """
            )
    def write_namespaces(self, namespace):
        self.file.write(f"""
sio = socketio.Client()
@sio.event(namespace='/{namespace}')
def connect(): 
    print('Successfully connected to the server')

@sio.event(namespace='/{namespace}')
def connect_error(): 
    print('Failed to connect to the server')

@sio.event(namespace='/{namespace}')
def disconnect(): 
    print('Disconnected from the server')

#Add the definition of your functions here as follows
#@sio.event(namespace='/{namespace}')
#def fn(data): 
    #print('data')\n\n""")

    def write_middleware_main(self, namespace):
        self.file.write(f"""
if __name__ == '__main__':
    sio.connect(os.path.expandvars('http://$HOST_IP:8000/{namespace}'))\n
    rospy.spin()""")
        self.file.write("\n")   

    def write_sio_web(self, name):
        self.file.write(f"""
@sio.on('connect', namespace='/web')
def connect_web(sid, data):
print('[INFO] Web client connected: {{}}'.format(sid))

@sio.on('disconnect', namespace='/web')
def disconnect_web(sid):
print('[INFO] Web client disconnected: {{}}'.format(sid))

@sio.on('new_data', namespace='/web')
#Add the definition of your functions here as follows use the fn you created in Middleware
#def newData(sid, data):
sio.emit('#fn', data, namespace='/{name}_namespace')\n\n""")
        
        
    def write_sio_cv(self):
        self.file.write(f"""
@sio.on('connect', namespace='/cv')
def connect_cv(sid, data):
    print('[INFO] CV client connected: {{}}'.format(sid))



@sio.on('disconnect', namespace='/cv')
def disconnect_cv(sid):
    print('[INFO] CV client disconnected: {{}}'.format(sid))


@sio.on('cv2server',namespace='/cv')
def handle_cv_message(sid,message):
    sio.emit('server2web', message, namespace='/web')\n\n""")


# def write_sio_dashboard(self, name):
#         self.file.write(f"""
# @sio.on('connect', namespace='/dashboard')
# def connect_dashboard(sid, data):
#     print('[INFO] dashboard connected: {{}}'.format(sid))
    

# @sio.on('disconnect', namespace='/dashboard')
# def disconnect_dashboard(sid):
#     print('[INFO] dashboard disconnected: {{}}'.format(sid))


# @sio.on('sensedData',namespace='/dashboard')
# def handle_sensed_data(sid,message):
#     sio.emit('sensedData', message, namespace='/web')\n\n""")
        
    def write_sio_database(self):
        self.file.write(f"""
@@sio.on('connect', namespace='/dynamicDB')
def connect_QT(sid,data):
    print("Hi from".format(sid))
    print('[INFO] Create_DynamicDB connected: {{}}'.format(sid))\n\n""")
        
    def write_update_data(self):
        self.file.write(f"""
ef actuate_data(request):

    if request.is_ajax():
        speed = request.POST.get('speed_control')
        print("_____________________",speed)
        # actuate_DB(speed, 'control_speed')
    return render(request, "actuate/actuate_data.html", {'actuateData': json.dumps(actuateData())})
#
def steering_angle(request):
    if request.is_ajax():
        angle = request.POST.get('steering_angle')
        print("_____________________",angle)
        # actuate_DB(angle, 'steering_angle')
    return render(request, "actuate/actuate_data.html")

def direction(request):
    if request.is_ajax():
        direction = request.POST.get('direction')
        print("_____________________",direction)
        # actuate_DB(direction, 'direction')
    return render(request, "actuate/actuate_data.html")\n\n""")
        
        def write_socket_connect_json(self):
            self.file.write(f"""const socket = io('http://localhost:8000/web');
  console.log(socket)
  socket.on('connect', () => {{
      console.log(`connect ${{socket.id}}`);
  }});

  socket.on('disconnect', (data) => {{
      console.log(`disconnect ${{socket.id}}`);
  }});\n\n""")