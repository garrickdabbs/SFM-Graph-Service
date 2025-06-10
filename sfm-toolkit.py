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
import uuid
from datetime import datetime

# =============================================================================
# Data Entity Definitions
# =============================================================================

class SFEntity:
    """
    Represents an entity (policy, regulation, program, etc.) within the Social Fabric Matrix.
    """
    def __init__(self, id: uuid.UUID, name: str, type: str, properties: dict):
        self.id = id
        self.name = name
        self.type = type
        self.properties = properties

    def __repr__(self):
        return f"{self.name} ({self.type})"


class Relationship:
    """
    Represents a directed relationship between two SFEntity objects.
    """
    def __init__(self, rel_id: uuid.UUID, sourceEntityId: uuid.UUID, targetEntityId: uuid.UUID, description: str,
                 value: float, metadata: dict):
        self.id = rel_id
        self.sourceEntityId = sourceEntityId
        self.targetEntityId = targetEntityId
        self.description = description  # e.g., 'impacts', 'supports', etc.
        self.value = value  # A weight or strength indicator between 0 and 1.
        self.metadata = metadata

    def __repr__(self):
        return f"{self.sourceEntityId} --{self.description}:{self.value}--> {self.targetEntityId}"


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
        G.add_edge(rel.sourceEntityId, rel.targetEntityId, description=rel.description,
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

def simulate_policy_change(G: nx.DiGraph, node_id: uuid.UUID, delta: float) -> None:
    """
    Simulate a change in policy impact by adjusting the weight of all outgoing edges from a given node.
    This is a simple example where all relationship 'values' are modified by delta, ensuring the results remain within [0, 1].

    Args:
        G (nx.DiGraph): The social fabric graph.
        node_id (uuid.UUID): Identifier of the node (policy) to simulate change for.
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
    # Create sample entities: These represent an instituion, organization, policy, regulation, or program, for example.
    e1 = SFEntity(uuid.uuid4(), "Data Privacy Policy", "Policy", {"effective_date": "2023-01-01", "version": "1.0"})
    e2 = SFEntity(uuid.uuid4(), "Compliance Regulation", "Regulation", {"jurisdiction": "US"})
    e3 = SFEntity(uuid.uuid4(), "Employee Training Program", "Program", {"department": "HR"})
    e4 = SFEntity(uuid.uuid4(), "Acme Mining Co.", "Corporation", {"sector": "Mining"})

    # Define sample relationships:
    # - e1 complies with e2.
    # - e3 supports e1.
    r1 = Relationship(uuid.uuid4(), e1.id, e2.id, "compliesWith", 0.9, {"last_updated": "2023-05-01"})
    r2 = Relationship(uuid.uuid4(), e3.id, e1.id, "supports", 0.8, {"last_updated": "2023-05-02"})
    r3 = Relationship(uuid.uuid4(), e2.id, e4.id, "regulates", 1, {"last_updated": "2024-05-06"})

    # Aggregate our data
    entities = [e1, e2, e3, e4]
    relationships = [r1, r2, r3]

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
    simulate_policy_change(graph, e1.id, -0.2)

    # Re-visualize graph after simulation to see updated values.
    visualize_graph(graph)
