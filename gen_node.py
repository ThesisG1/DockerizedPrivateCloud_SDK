import yaml
import Ros_Node as node

class RosNodeGen():


    def generate_node(self):

        # Load YAML skeleton from file
        with open('node_config.yml', 'r') as file:
            ros_node_info = yaml.safe_load(file)

        self.node_name = ros_node_info['ros_node']['name']
        self.publish_topics = ros_node_info['ros_node']['topics']['publish']
        self.subscribe_topics = ros_node_info['ros_node']['topics']['subscribe']

        node_info = node.ROSNodeInfo(node_name=self.node_name , node_publishers=self.publish_topics, node_subscribers=self.subscribe_topics)
        n = node.Node(node_info)



if __name__ == '__main__':

    gen = RosNodeGen()
    gen.generate_node()

