# TODO: Write the lines of codes from the generator files into variables and functions
# Example:
class FileWriter:
    def __init__(self, file):
        self.file = file

    def callback_function(self, subscribers):
        for sub in subscribers:
            name = subscribers[sub]["name"]
            callback = subscribers[sub]["callback"]
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
            callback = subscribers[sub]["callback"]
            self.file.write(
                f"""
{name}_sub = rospy.Subscriber('/{name}',{type.split("/")[-1]},{callback})
            """
            )
