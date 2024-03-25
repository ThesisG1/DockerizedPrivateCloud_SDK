import sys

sys.path.append("..")
import utilities.templates as templates
import utilities.parse as parser


class MiddlewareTopics:
    def __init__(self, publishers, subscribers):
        self.node_publishers = publishers
        self.node_subscribers = subscribers


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
                writer = templates.FileWriter(file=file)
                imports, types = parser.Parser.parse_types(mw)
                writer.write_imports(imports, types)
                writer.callback_function(mw.node_subscribers)
                writer.init_node(node_name=self.node_info.node_name)
                writer.write_subscribers(mw.node_subscribers)
                writer.write_publishers(mw.node_publishers)

        # TODO: Generate Namespaces and handle the templates neccessary for it
