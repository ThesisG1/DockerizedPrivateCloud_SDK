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
