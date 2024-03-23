import yaml
import ros_node as node
import sys

sys.path.append("..")
import middleware.camera_middleware as mw


class RosNodeGen:
    def __init__(self, yml_file):
        # TODO: Add an init function to initialize the class for better OOP
        # TODO: validation for [][] in topics
        # This function is going to be a universal function that generates
        # namespaces, nodes and middlewares.
        # we are trying to create the files neccessary to generate namespaces and middlewares
        # Load YAML skeleton from file
        with open(yml_file, "r") as file:
            parser = yaml.safe_load(file)
        if "ros_node" in parser:
            print("Valid YAML file")
            self.node_name = parser["ros_node"]["name"]
            # TODO: validate
            self.publish_topics = parser["ros_node"]["topics"]["publish"]
            # TODO: validate
            self.subscribe_topics = parser["ros_node"]["topics"]["subscribe"]
            node_info = node.ROSNodeInfo(
                node_name=self.node_name,
                node_publishers=self.publish_topics,
                node_subscribers=self.subscribe_topics,
            )
            n = node.Node(node_info)


if __name__ == "__main__":
    gen = RosNodeGen("node_config.yml")
