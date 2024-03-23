# TODO: Write the lines of codes from the generator files into variables and functions
# Example:
class FileWriter:
    def __init__(self, file):
        self.file = file

    def callback_function(self, subscribers):
        for i in range(len(subscribers)):
            name = subscribers[f"topic_{i+1}"]["name"]
            callback = subscribers[f"topic_{i+1}"]["callback"]
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
        for i in range(len(publishers)):
            name = publishers[f"topic_{i+1}"]["name"]
            type = publishers[f"topic_{i+1}"]["type"]
            self.file.write(
                f"""{name}_pub = rospy.Publisher('/{name}', {type.split("/")[-1]}, queue_size=10)\n"""
            )

    def write_subscribers(self, subscribers):
        for i in range(len(subscribers)):
            name = subscribers[f"topic_{i+1}"]["name"]
            type = subscribers[f"topic_{i+1}"]["type"]
            callback = subscribers[f"topic_{i+1}"]["callback"]
            self.file.write(
                f"""
{name}_sub = rospy.Subscriber('/{name}',{type.split("/")[-1]},{callback})
            """
            )

        self.file.write(
            """
rospy.spin()
                    """
        )
