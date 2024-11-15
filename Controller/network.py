import networkx as nx
import matplotlib.pyplot as plt
from node import Node
from link import Link

class Network:
    def __init__(self):
        self.nodes = {}
        self.links = []
        self.graph = nx.Graph()

    def add_node(self, node_id, name, node_type='router'):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, name, node_type)
            self.graph.add_node(name, node_type=node_type)


    def add_link(self, source_id, destination_id, bandwidth):
        if source_id in self.nodes and destination_id in self.nodes:
            inverse_weight = 1.0 / bandwidth if bandwidth != 0 else float('inf')
            self.links.append(Link(self.nodes[source_id], self.nodes[destination_id], bandwidth))
            self.graph.add_edge(self.nodes[source_id].name, self.nodes[destination_id].name, weight=inverse_weight)
        else:
            print("Error: One or both nodes not found in the network.")

    def remove_node(self, node_id):
        if node_id in self.nodes:
            node_name = self.nodes[node_id].name
            self.graph.remove_node(node_name)
            del self.nodes[node_id]
            self.links = [link for link in self.links if link.source.node_id != node_id and link.destination.node_id != node_id]
            print(f"Node {node_name} and its associated links have been removed from the network.")
        else:
            print(f"Node ID {node_id} not found in the network.")

    def display_network(self):
        print("Nodes in the network:")
        for node in self.nodes.values():
            print(node)
        print("\nLinks in the network:")
        for link in self.links:
            print(link)

    def visualize_network(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=7000, node_color="skyblue", font_size=15, font_weight="bold")
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()
