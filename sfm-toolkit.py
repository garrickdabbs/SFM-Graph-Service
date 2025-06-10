#!/usr/bin/env python3
"""
SFM Toolkit: A Prototype for Implementing the Social Fabric Matrix Framework
# Copyright (C) 2025 Garrick Dabbs
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

This module sets up a basic model using:
- SFEntity: A core class to represent any object such as policies, regulations, programs, etc.
- Relationship: A class to capture directed relationships between entities.
- A graph representing the social fabric with interconnections between policies and other components.
- A simple simulation function to illustrate how adjustments in policy impact might be evaluated.

Dependencies:
    - networkx
    - matplotlib
"""

import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# =============================================================================
# Data Entity Definitions
# =============================================================================

class SFEntity:
    """
    Represents an entity (policy, regulation, program, etc.) within the Social Fabric Matrix.
    """
    def __init__(self, entity_id: str, name: str, entity_type: str, properties: dict):
        self.id = entity_id
        self.name = name
        self.type = entity_type
        self.properties = properties

    def __repr__(self):
        return f"{self.name} ({self.type})"


class Relationship:
    """
    Represents a directed relationship between two SFEntity objects.
    """
    def __init__(self, rel_id: str, source: SFEntity, target: SFEntity, property_name: str,
                 value: float, metadata: dict):
        self.id = rel_id
        self.source = source
        self.target = target
        self.property_name = property_name  # e.g., 'impacts', 'supports', etc.
        self.value = value  # A weight or strength indicator between 0 and 1.
        self.metadata = metadata

    def __repr__(self):
        return f"{self.source.name} --{self.property_name}:{self.value}--> {self.target.name}"


# =============================================================================
# Graph Construction & Visualization
# =============================================================================

def build_graph(entities: list, relationships: list) -> nx.DiGraph:
    """
    Build and return a directed graph (NetworkX DiGraph) from a list of entities and relationships.
    
    Args:
        entities (list): List of SFEntity objects.
        relationships (list): List of Relationship objects.
    
    Returns:
        nx.DiGraph: A directed graph representing the social fabric.
    """
    G = nx.DiGraph()
    
    # Add all entities as nodes.
    for entity in entities:
        G.add_node(entity.id, name=entity.name, type=entity.type, properties=entity.properties)
    
    # Add relationships as edges.
    for rel in relationships:
        G.add_edge(rel.source.id, rel.target.id, property_name=rel.property_name,
                   value=rel.value, metadata=rel.metadata)
    return G

def visualize_graph(G: nx.DiGraph) -> None:
    """
    Visualizes the graph using matplotlib with nodes labeled by their names.
    
    Args:
        G (nx.DiGraph): The diagram representing the social fabric.
    """
    pos = nx.spring_layout(G)  # Position nodes using Fruchterman-Reingold force-directed algorithm.
    labels = nx.get_node_attributes(G, 'name')
    edge_labels = nx.get_edge_attributes(G, 'property_name')
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='skyblue', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title("Social Fabric Matrix - Example Graph")
    plt.show()

# =============================================================================
# Simulation & Analysis Tools
# =============================================================================

def simulate_policy_change(G: nx.DiGraph, node_id: str, delta: float) -> None:
    """
    Simulate a change in policy impact by adjusting the weight of all outgoing edges from a given node.
    This is a simple example where all relationship 'values' are modified by delta, ensuring the results remain within [0, 1].

    Args:
        G (nx.DiGraph): The social fabric graph.
        node_id (str): Identifier of the node (policy) to simulate change for.
        delta (float): The value to add/subtract from each outgoing relationship's weight.
    """
    for _, target, data in G.out_edges(node_id, data=True):
        old_value = data['value']
        # Ensure the new value is clamped between 0 and 1.
        new_value = max(0, min(old_value + delta, 1))
        data['value'] = new_value
        print(f"Updated relationship from {node_id} to {target}: {old_value} -> {new_value}")

# =============================================================================
# Main Routine: Prototype Demonstration
# =============================================================================

if __name__ == "__main__":
    # Create sample entities: These represent a policy, regulation, and program, for example.
    e1 = SFEntity("e1", "Data Privacy Policy", "Policy", {"effective_date": "2023-01-01", "version": "1.0"})
    e2 = SFEntity("e2", "Compliance Regulation", "Regulation", {"jurisdiction": "US"})
    e3 = SFEntity("e3", "Employee Training Program", "Program", {"department": "HR"})

    # Define sample relationships:
    # - e1 complies with e2.
    # - e3 supports e1.
    r1 = Relationship("r1", e1, e2, "compliesWith", 0.9, {"last_updated": "2023-05-01"})
    r2 = Relationship("r2", e3, e1, "supports", 0.8, {"last_updated": "2023-05-02"})

    # Aggregate our data
    entities = [e1, e2, e3]
    relationships = [r1, r2]

    # Build our graph model.
    graph = build_graph(entities, relationships)

    # Display the nodes and edges of the graph.
    print("Nodes in the Social Fabric Graph:")
    for node, data in graph.nodes(data=True):
        print(f"{node}: {data}")

    print("\nEdges in the Social Fabric Graph:")
    for source, target, data in graph.edges(data=True):
        print(f"{source} -> {target}: {data}")

    # Visualize the resulting graph.
    visualize_graph(graph)

    # Example simulation: Adjust impact weight from node e1 by reducing by 0.2.
    print("\nSimulating policy change on node 'e1' with a delta of -0.2:")
    simulate_policy_change(graph, "e1", -0.2)

    # Re-visualize graph after simulation to see updated values.
    visualize_graph(graph)
