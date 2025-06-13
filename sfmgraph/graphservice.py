import networkx as nx

class SFMGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entity(self, entity):
        self.graph.add_node(entity.id, **entity.dict())

    def add_relationship(self, relationship):
        self.graph.add_edge(relationship.source_id, relationship.target_id, **relationship.dict())

    def visualize(self):
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, font_size=10)
        plt.show()
