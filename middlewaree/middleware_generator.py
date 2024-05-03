import sys

sys.path.append("..")
import utilitiess.templates as templates
import utilitiess.parse as parser


class MiddlewareTopics:
    def __init__(self, publishers, subscribers):
        #node_publishers are the nodes that subscribe in the ros_layer
        #node_subscribers are the nodes that publish in the ros_layer
        self.node_publishers = subscribers
        self.node_subscribers = publishers


class Middleware:
    def __init__(self, node_info):
        self.node_info = node_info
        publisher_topics = {}
        subscriber_topics = {}
        for topic in self.node_info.node_publishers:
            if self.node_info.node_publishers[topic]["middleware_flag"] != 0:
                publisher_topics[topic] = self.node_info.node_publishers[topic]

        for topic in self.node_info.node_subscribers:
            if self.node_info.node_subscribers[topic]["middleware_flag"] != 0:
                subscriber_topics[topic] = self.node_info.node_subscribers[topic]

        # change it to check on created arrays
        if publisher_topics or subscriber_topics:
            mw = MiddlewareTopics(publisher_topics, subscriber_topics)
            with open(f"{self.node_info.node_name}_middleware.py", "w") as file:
                writer = templates.FileWriterr(file=file)
                imports, types = parser.Parser.parse_types(mw)
                writer.write_imports(imports, types)
                file.write(f"""import socketio\nimport os\n\n""")
                writer.callback_function(mw.node_subscribers)
                #check the flow. if bottom-up then we emit to a namespace
                if (self.node_info.flow_flag != 0):
                    file.write(f""" 
    #emit your data on the dashboard namespace
    #sio.emit('Data', {{data}} ,namespace='/{self.node_info.node_name}_namespace')\n"""  )
                writer.write_namespaces(namespace = self.node_info.node_name + "_namespace")
                writer.init_node(node_name=self.node_info.node_name + "_mw")
                writer.write_subscribers(mw.node_subscribers)
                writer.write_publishers(mw.node_publishers)
                writer.write_middleware_main(namespace = self.node_info.node_name + "_namespace")
        # TODO: Generate Namespaces and handle the templates neccessary for it
