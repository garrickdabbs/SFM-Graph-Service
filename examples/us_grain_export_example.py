import sys
import os
from pathlib import Path

# Add the workspace root to Python path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from core.sfm_models import (
    Actor, Institution, Resource, Policy, Flow, Relationship, Indicator, SFMGraph
)
from core.sfm_enums import RelationshipKind, ResourceType, FlowNature
from core.sfm_query import SFMQueryFactory, NetworkXSFMQueryEngine
from db.sfm_dao import NetworkXSFMRepository

def create_us_grain_market_graph(repo: NetworkXSFMRepository, graph: SFMGraph):

    # Create actors
    usda = Actor(label="USDA", sector="Government")
    farmers = Actor(label="Farmers", sector="Agriculture")
    traders = Actor(label="Traders", sector="Private")

    # Create institutions
    government = Institution(label="US Government")
    trade_org = Institution(label="Trade Organization")

    # Create resources
    grain = Resource(label="Grain", rtype=ResourceType.PRODUCED)
    land = Resource(label="Land", rtype=ResourceType.NATURAL)

    # Create policies
    subsidy = Policy(label="Grain Subsidy", authority="USDA")
    tariff = Policy(label="Export Tariff", authority="US Government")

    # Create flows
    export_flow = Flow(label="Grain Export", nature=FlowNature.OUTPUT)
    financial_flow = Flow(label="Subsidy Payment", nature=FlowNature.INPUT)

    # Create indicators
    grain_price = Indicator(label="Grain Price", current_value=300)  # Example price in USD per ton
    production_level = Indicator(label="Production Level", current_value=1000000)  # Example production in tons

    # Add nodes to the repository
    repo.create_node(usda)
    repo.create_node(farmers)
    repo.create_node(traders)
    repo.create_node(government)
    repo.create_node(trade_org)
    repo.create_node(grain)
    repo.create_node(land)
    repo.create_node(subsidy)
    repo.create_node(tariff)
    repo.create_node(export_flow)
    repo.create_node(financial_flow)
    repo.create_node(grain_price)
    repo.create_node(production_level)
    
    sfm_graph.add_node(usda)
    sfm_graph.add_node(farmers)
    sfm_graph.add_node(traders)
    sfm_graph.add_node(government)
    sfm_graph.add_node(trade_org)
    sfm_graph.add_node(grain)
    sfm_graph.add_node(land)
    sfm_graph.add_node(subsidy)
    sfm_graph.add_node(tariff)
    sfm_graph.add_node(export_flow)
    sfm_graph.add_node(financial_flow)
    sfm_graph.add_node(grain_price)
    sfm_graph.add_node(production_level)
    

    # Create relationships
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=usda.id, target_id=farmers.id, kind=RelationshipKind.GOVERNS)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=farmers.id, target_id=grain.id, kind=RelationshipKind.PRODUCES)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=farmers.id, target_id=land.id, kind=RelationshipKind.USES)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=farmers.id, target_id=traders.id, kind=RelationshipKind.EXCHANGES_WITH)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=traders.id, target_id=grain.id, kind=RelationshipKind.TRANSFERS)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=government.id, target_id=subsidy.id, kind=RelationshipKind.IMPLEMENTS)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=subsidy.id, target_id=farmers.id, kind=RelationshipKind.FUNDS)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=government.id, target_id=tariff.id, kind=RelationshipKind.ENACTS)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=grain.id, target_id=export_flow.id, kind=RelationshipKind.EXCHANGES_WITH)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=export_flow.id, target_id=traders.id, kind=RelationshipKind.TRANSFERS)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=grain.id, target_id=grain_price.id, kind=RelationshipKind.AFFECTS)))
    sfm_graph.add_relationship(repo.create_relationship(Relationship(source_id=grain.id, target_id=production_level.id, kind=RelationshipKind.AFFECTS)))
    
    repo.save_graph(sfm_graph) # Set the graph in the repository

    return sfm_graph

if __name__ == "__main__":
    repo = NetworkXSFMRepository() # Initialize the repository
    sfm_graph = SFMGraph() # Initialize the graph
    repo.save_graph(sfm_graph) # Set the graph in the repository
    us_gm_graph = create_us_grain_market_graph(repo, sfm_graph) # Create the graph
    
    print(f"Graph created with {len(us_gm_graph)} entities.")
    print(f"Graph contains {len(us_gm_graph.relationships)} relationships.")
    print(f"Graph contains {len(us_gm_graph.actors)} actors.")
    print(f"Graph contains {len(us_gm_graph.institutions)} institutions.")
    print(f"Graph contains {len(us_gm_graph.resources)} resources.")
    print(f"Graph contains {len(us_gm_graph.policies)} policies.")
    print(f"Graph contains {len(us_gm_graph.flows)} flows.")
    print(f"Graph contains {len(us_gm_graph.indicators)} indicators.")
    
    # Demonstrate analytical queries using the SFM Query Engine
    print("\n--- SFM Analysis Examples ---")
    
    try:
        # Create query engine
        query_engine = SFMQueryFactory.create_query_engine(us_gm_graph, "networkx")
        
        # Example 1: Find most central actors
        print("\nMost central actors:")
        from core.sfm_models import Actor
        central_actors = query_engine.get_most_central_nodes(Actor, "betweenness", 3)
        for node_id, score in central_actors:
            actor = us_gm_graph.actors.get(node_id)
            if actor:
                print(f"  {actor.label}: {score:.3f}")
        
        # Example 2: Analyze policy impact
        print("\nPolicy impact analysis:")
        for policy_id, policy in us_gm_graph.policies.items():
            impact = query_engine.analyze_policy_impact(policy_id, impact_radius=2)
            print(f"  {policy.label}: affects {impact.get('total_affected_nodes', 0)} nodes")
        
        # Example 3: Network structure metrics
        print(f"\nNetwork density: {query_engine.get_network_density():.3f}")
        
        # Example 4: Resource flow analysis
        print("\nResource flow analysis:")
        grain_flows = query_engine.trace_resource_flows(ResourceType.PRODUCED)
        print(f"  Identified {len(grain_flows.flow_volumes)} flow connections")
        
        # Example 5: Identify structural holes/bridges
        print("\nStructural bridges (key connector nodes):")
        bridges = query_engine.get_structural_holes()
        for bridge_id in bridges[:3]:  # Show top 3
            for node_collection in [us_gm_graph.actors, us_gm_graph.institutions, 
                                  us_gm_graph.resources, us_gm_graph.policies]:
                if bridge_id in node_collection:
                    print(f"  {node_collection[bridge_id].label}")
                    break
        
    except Exception as e:
        print(f"Analysis error: {e}")
    
    us_gm_graph.clear() # Clear the graph;
    repo.clear() # Clear the repository
    print("\nGraph and Repo cleared.")


