# TODO: Write the lines of codes from the generator files into variables and functions
# Example:
class FileWriterr:
    def __init__(self, file):
        self.file = file
        
    def callback_function(self, subscribers):
        for sub in subscribers:
            name = subscribers[sub]["name"]
            callback = name + "_callback"
            self.file.write(
                f"""def {callback}(data):
    print('IMPLEMENT CALLBACK {callback}')"""
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
        self.file.write("\n")
        
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
        self.file.write("\n")
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


    def write_sio_web(self, node_name):
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
    #sio.emit('#fn', data, namespace='/{node_name}_namespace')\n""")
        self.file.write("\n")

    def write_middleware_main(self, namespace):
        self.file.write(f"""
if __name__ == '__main__':
    sio.connect(os.path.expandvars('http://$HOST_IP:8000/{namespace}'))\n
    rospy.spin()""")
        self.file.write("\n")
        
    def write_sio_database(self):
        self.file.write(f"""
@sio.on('connect', namespace='/dynamicDB')
def connect_QT(sid,data):
    print("Hi from".format(sid))
    print('[INFO] Create_DynamicDB connected: {{}}'.format(sid))\n\n""")
        
    def write_update_data(self):
        self.file.write(f"""
def render_data_fn(request):
    if request.is_ajax():
        #data = request.POST.get('data')
        #Implement the rest of your function here
        return render(request, "template")         #Add your own template e.g. "sense/historicaldata.html"\n\n""") 
        
    def write_sio_dashboard(self):
        self.file.write(f"""
@sio.on('connect', namespace='/dashboard')
def connect_dashboard(sid, data):
    print('[INFO] dashboard connected: {{}}'.format(sid))
    
@sio.on('disconnect', namespace='/dashboard')
def disconnect_dashboard(sid):
    print('[INFO] dashboard disconnected: {{}}'.format(sid))

@sio.on('sensedData',namespace='/dashboard')
def handle_sensed_data(sid,message):
    sio.emit('sensedData', message, namespace='/web')\n\n""")
        
    def write_table_create(self, node_name):
        self.file.write(f"""def create_DB():
    cursor = connections["default"].cursor()
    create_{node_name} = \"\"\"
        CREATE TABLE IF NOT EXISTS `{node_name}` (
            `col_1` date_type1,
            `col_2` date_type2,
            `col_3` date_type3,
            PRIMARY KEY (key) 
        )
    \"\"\"
    cursor.execute(create_{node_name})
    #Create the rest of the tables in the same way \n\n""")
        
    def write_table_search(self):
        self.file.write(f"""def select_data():
    cursor = connections["default"].cursor()
                        
    # data to be sent to frontend
    historical_data = {{}}
                        
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
    cursor.execute(f\"\"\"SELECT time FROM {{all_tables[1]}}\"\"\" + sql_statement + ";")
    time = cursor.fetchall()
    time = ([a_tuple[0] for a_tuple in time])
    
    # add time data
    historical_data["time"] = time
                        
    # executing sql statements 
    for table in all_tables:
        # select value from tables 
        cursor.execute(f\"\"\"SELECT value FROM {{table}} \"\"\" + sql_statement)
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
                        
    return historical_data\n\n""")
        
    def establish_DB_connection(self):
        self.file.write(f"""def dbInit(db_host,db_user,db_password,data_base,server_addr):
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
    print('[INFO] Connecting to server http://{{}}:{{}}...'.format(server_addr, server_port))
    return cursor, mydb\n\n""")
        
    def write_table_insert(self, node_name):
        self.file.write(f"""def insert_data():
    cursor = connections["default"].cursor()
    sql_statement = f\"\"\"INSERT INTO  `{node_name}`
                ( `time`,
                `value`)
                VALUES
                (%s,%s,%s), (%s,%s,%s);
                \"\"\"
    cursor.execute(sql_statement)\n\n""")
        

        
    


