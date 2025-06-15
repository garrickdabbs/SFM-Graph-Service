import networkx as nx

class SFMGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entity(self, entity):
        self.graph.add_node(entity.entity_id, **entity.model_dump())

    def add_relationship(self, relationship):
        source_id = relationship.sourceEntityId
        target_id = relationship.targetEntityId
        
        if source_id not in self.graph.nodes:
            raise ValueError(f"Source entity {source_id} does not exist")
        if target_id not in self.graph.nodes:
            raise ValueError(f"Target entity {target_id} does not exist")
            
        self.graph.add_edge(source_id, target_id, **relationship.model_dump())
    
    def remove_entity(self, entity_id):
        self.graph.remove_node(entity_id)
        
    def get_entity(self, entity_id):
        if entity_id in self.graph.nodes:
            return self.graph.nodes[entity_id]
        return None
    
    # TODO: move to a separate service
    def visualize(self, node_size=2000, font_size=10, save_path=None):
        """Visualize the SFM graph.
        
        Args:
            node_size: Size of nodes in the visualization
            font_size: Size of label font
            save_path: Optional path to save the visualization instead of displaying
        """
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=node_size, font_size=font_size)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()


