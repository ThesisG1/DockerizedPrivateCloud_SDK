class Parser:

    # Parse the types found in the ['type'] field of the node_publishers and node_subscribers
    def parse_types(ros_node_info):
        imports = set()
        types = {}
        for i in range(len(ros_node_info.node_publishers)):
            type = ros_node_info.node_publishers[f"topic_{i+1}"]["type"]
            if "/" in type:
                import_type, type_name = type.split("/")
                imports.add(import_type)
                if import_type in types:
                    types[import_type].append(type_name)
                else:
                    types[import_type] = [type_name]

        for sub in ros_node_info.node_subscribers:
            type = ros_node_info.node_subscribers[sub]["type"]

            if "/" in type:
                import_type, type_name = type.split("/")
                imports.add(import_type)
                if type in types:
                    types[import_type].append(type_name)
                else:
                    types[import_type] = [type_name]
        return imports, types
