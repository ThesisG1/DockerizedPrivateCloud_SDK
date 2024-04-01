import yaml
import ros_level.ros_node as node
import sys

sys.path.append("..")
import middleware.middleware_gen as mw


class RosNodeGen:
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

            node_info = node.ROSNodeInfo(
                node_name=self.node_name,
                node_publishers=self.publish_topics,
                node_subscribers=self.subscribe_topics,
            )
            n = node.Node(node_info)
            middleware = mw.Middleware(node_info)


if __name__ == "__main__":
    gen = RosNodeGen("node_config.yml")
