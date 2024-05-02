import yaml
import ros_node as node
import sys

sys.path.append("..")
import middlewaree.middleware_generator as mw
import namespace.generate_views as views
import database.query_generator as db


class RosNodeGenerator:
    def __init__(self, yml_file):
        """
        This function parses the YAML file to generate the ROS node.
        """

        with open(yml_file, "r") as file:
            parser = yaml.safe_load(file)
        if "ros_node" in parser:
            print("Valid YAML file")
            try:
                self.node_name = parser["ros_node"]["name"]
                self.flow_flag = parser["ros_node"]["flow_flag"]
                print("flag: ", self.flow_flag)
            except KeyError:
                print("Node name not found. Please name the node.")
            try:
                topic = parser["ros_node"]["topics"]
                if "publish" in parser["ros_node"]["topics"]:
                    self.publish_topics = parser["ros_node"]["topics"]["publish"]
                if "subscribe" in parser["ros_node"]["topics"]:
                    self.subscribe_topics = parser["ros_node"]["topics"]["subscribe"]
            except KeyError:
                print("Topics not found. Please specify the topics.")

        
            node_info = node.ROSNodeInformation(
                node_name=self.node_name,
                flow_flag=self.flow_flag,
                node_publishers=self.publish_topics,
                node_subscribers=self.subscribe_topics,
            )
            n = node.Node(node_info)
            middleware = mw.Middleware(node_info)
            actuate_views = views.Views(node_info)
            database = db.Database(node_info)


if __name__ == "__main__":
    gen = RosNodeGenerator("node_config.yml")
