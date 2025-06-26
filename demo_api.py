#!/usr/bin/env python3
"""
SFM API Demo Script

This script demonstrates how to use the SFM FastAPI REST API.
It creates sample data and shows various API operations.
"""

import time
import json
import requests
from typing import Dict, Any, Optional

class SFMAPIDemo:
    """Demo client for the SFM API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def wait_for_api(self, timeout: int = 30) -> bool:
        """Wait for the API to be ready."""
        print(f"⏳ Waiting for API at {self.base_url}...")
        
        for i in range(timeout):
            try:
                response = self.session.get(f"{self.base_url}/health", timeout=2)
                if response.status_code == 200:
                    print("✅ API is ready!")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            if i % 5 == 0 and i > 0:
                print(f"   Still waiting... ({i}s)")
            time.sleep(1)
        
        print("❌ API not ready within timeout")
        return False
    
    def demo_health_check(self):
        """Demonstrate health check endpoint."""
        print("\n🏥 Health Check")
        print("-" * 20)
        
        response = self.session.get(f"{self.base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"Status: {health['status']}")
            print(f"Backend: {health['backend']}")
            print(f"Last operation: {health.get('last_operation', 'None')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    
    def demo_create_entities(self) -> Dict[str, str]:
        """Demonstrate creating entities and return their IDs."""
        print("\n🏗️ Creating Sample Entities")
        print("-" * 30)
        
        entity_ids = {}
        
        # Create an actor
        print("Creating USDA actor...")
        actor_data = {
            "name": "USDA",
            "description": "United States Department of Agriculture",
            "sector": "government",
            "legal_form": "federal_agency",
            "meta": {"country": "USA", "established": "1862"}
        }
        
        response = self.session.post(f"{self.base_url}/actors", json=actor_data)
        if response.status_code == 201:
            actor = response.json()
            entity_ids["usda"] = actor["id"]
            print(f"✅ Created actor: {actor['name']} (ID: {actor['id'][:8]}...)")
        else:
            print(f"❌ Failed to create actor: {response.status_code}")
        
        # Create a policy
        print("Creating Farm Bill policy...")
        policy_data = {
            "name": "Farm Bill 2023",
            "description": "Comprehensive agricultural policy framework",
            "authority": "US Congress",
            "target_sectors": ["agriculture", "food_security"],
            "enforcement": 0.8,
            "meta": {"budget": "1.5T", "duration": "5_years"}
        }
        
        response = self.session.post(f"{self.base_url}/policies", json=policy_data)
        if response.status_code == 201:
            policy = response.json()
            entity_ids["farm_bill"] = policy["id"]
            print(f"✅ Created policy: {policy['name']} (ID: {policy['id'][:8]}...)")
        else:
            print(f"❌ Failed to create policy: {response.status_code}")
        
        # Create a resource
        print("Creating corn resource...")
        resource_data = {
            "name": "Corn",
            "description": "Agricultural grain commodity",
            "rtype": "NATURAL",
            "unit": "bushels",
            "meta": {"seasonal": "true", "storage_type": "grain_elevator"}
        }
        
        response = self.session.post(f"{self.base_url}/resources", json=resource_data)
        if response.status_code == 201:
            resource = response.json()
            entity_ids["corn"] = resource["id"]
            print(f"✅ Created resource: {resource['name']} (ID: {resource['id'][:8]}...)")
        else:
            print(f"❌ Failed to create resource: {response.status_code}")
        
        # Create an institution
        print("Creating Farm Credit System institution...")
        institution_data = {
            "name": "Farm Credit System",
            "description": "Network of borrower-owned lending institutions",
            "meta": {"type": "cooperative", "established": "1916"}
        }
        
        response = self.session.post(f"{self.base_url}/institutions", json=institution_data)
        if response.status_code == 201:
            institution = response.json()
            entity_ids["farm_credit"] = institution["id"]
            print(f"✅ Created institution: {institution['name']} (ID: {institution['id'][:8]}...)")
        else:
            print(f"❌ Failed to create institution: {response.status_code}")
        
        return entity_ids
    
    def demo_create_relationships(self, entity_ids: Dict[str, str]):
        """Demonstrate creating relationships between entities."""
        print("\n🔗 Creating Relationships")
        print("-" * 25)
        
        relationships = [
            {
                "source": "usda",
                "target": "farm_bill",
                "kind": "IMPLEMENTS",
                "weight": 0.9,
                "description": "USDA implements Farm Bill"
            },
            {
                "source": "farm_bill",
                "target": "corn",
                "kind": "AFFECTS",
                "weight": 0.7,
                "description": "Farm Bill affects corn production"
            },
            {
                "source": "farm_credit",
                "target": "corn",
                "kind": "SUPPORTS",
                "weight": 0.6,
                "description": "Farm Credit supports corn farmers"
            }
        ]
        
        for rel in relationships:
            if rel["source"] in entity_ids and rel["target"] in entity_ids:
                relationship_data = {
                    "source_id": entity_ids[rel["source"]],
                    "target_id": entity_ids[rel["target"]],
                    "kind": rel["kind"],
                    "weight": rel["weight"],
                    "meta": {"description": rel["description"]}
                }
                
                response = self.session.post(f"{self.base_url}/relationships", json=relationship_data)
                if response.status_code == 201:
                    relationship = response.json()
                    print(f"✅ Created relationship: {rel['description']} ({rel['kind']})")
                else:
                    print(f"❌ Failed to create relationship: {response.status_code}")
            else:
                print(f"⚠️ Skipping relationship: missing entities")
    
    def demo_analytics(self, entity_ids: Dict[str, str]):
        """Demonstrate analytics endpoints."""
        print("\n📊 Analytics & Analysis")
        print("-" * 25)
        
        # Get statistics
        print("Getting graph statistics...")
        response = self.session.get(f"{self.base_url}/statistics")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Total nodes: {stats['total_nodes']}")
            print(f"✅ Total relationships: {stats['total_relationships']}")
            print(f"✅ Entity breakdown: {stats.get('entity_breakdown', {})}")
        else:
            print(f"❌ Failed to get statistics: {response.status_code}")
        
        # Quick analysis
        print("\nPerforming quick analysis...")
        response = self.session.get(f"{self.base_url}/analytics/quick")
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Quick analysis completed")
            print(f"   Graph status: {analysis.get('health', {}).get('status', 'unknown')}")
            if 'top_central_nodes' in analysis:
                print(f"   Central nodes found: {len(analysis['top_central_nodes'])}")
        else:
            print(f"❌ Failed to perform quick analysis: {response.status_code}")
        
        # Centrality analysis
        print("\nPerforming centrality analysis...")
        response = self.session.get(f"{self.base_url}/analytics/centrality?centrality_type=betweenness&limit=5")
        if response.status_code == 200:
            centrality = response.json()
            print(f"✅ Centrality analysis completed")
            print(f"   Analysis type: {centrality.get('centrality_type', 'unknown')}")
            nodes = centrality.get('top_nodes', [])
            if nodes:
                print(f"   Top central node: {nodes[0].get('name', 'unknown')} (score: {nodes[0].get('score', 0):.3f})")
        else:
            print(f"❌ Failed to perform centrality analysis: {response.status_code}")
        
        # Policy impact analysis
        if "farm_bill" in entity_ids:
            print("\nAnalyzing policy impact...")
            policy_id = entity_ids["farm_bill"]
            response = self.session.get(f"{self.base_url}/analytics/policy-impact/{policy_id}?impact_radius=3")
            if response.status_code == 200:
                impact = response.json()
                print(f"✅ Policy impact analysis completed")
                print(f"   Affected nodes: {impact.get('affected_nodes_count', 0)}")
                print(f"   Impact radius: {impact.get('impact_radius', 0)}")
            else:
                print(f"❌ Failed to analyze policy impact: {response.status_code}")
    
    def demo_list_operations(self):
        """Demonstrate listing operations."""
        print("\n📋 Listing Operations")
        print("-" * 22)
        
        # List nodes
        response = self.session.get(f"{self.base_url}/nodes?limit=10")
        if response.status_code == 200:
            nodes = response.json()
            print(f"✅ Found {len(nodes)} nodes:")
            for node in nodes[:3]:  # Show first 3
                print(f"   - {node.get('name', 'Unknown')} ({node.get('type', 'Unknown')})")
            if len(nodes) > 3:
                print(f"   ... and {len(nodes) - 3} more")
        else:
            print(f"❌ Failed to list nodes: {response.status_code}")
        
        # List relationships
        response = self.session.get(f"{self.base_url}/relationships?limit=10")
        if response.status_code == 200:
            relationships = response.json()
            print(f"✅ Found {len(relationships)} relationships:")
            for rel in relationships[:3]:  # Show first 3
                print(f"   - {rel.get('kind', 'Unknown')} (weight: {rel.get('weight', 0)})")
            if len(relationships) > 3:
                print(f"   ... and {len(relationships) - 3} more")
        else:
            print(f"❌ Failed to list relationships: {response.status_code}")
    
    def demo_metadata(self):
        """Demonstrate metadata endpoints."""
        print("\n📖 Metadata & Documentation") 
        print("-" * 30)
        
        # Get entity types
        response = self.session.get(f"{self.base_url}/metadata/entity-types")
        if response.status_code == 200:
            metadata = response.json()
            entity_types = list(metadata.get('entity_types', {}).keys())
            print(f"✅ Available entity types: {', '.join(entity_types)}")
            
            relationship_kinds = metadata.get('relationship_kinds', [])
            print(f"✅ Available relationship kinds: {len(relationship_kinds)} types")
        else:
            print(f"❌ Failed to get metadata: {response.status_code}")
        
        # Get API info
        response = self.session.get(f"{self.base_url}/metadata/api-info")
        if response.status_code == 200:
            api_info = response.json()
            print(f"✅ API version: {api_info.get('api_version', 'unknown')}")
            features = api_info.get('features', [])
            print(f"✅ Available features: {len(features)}")
        else:
            print(f"❌ Failed to get API info: {response.status_code}")
    
    def run_full_demo(self):
        """Run the complete demo."""
        print("🚀 SFM API Demonstration")
        print("=" * 50)
        
        # Wait for API to be ready
        if not self.wait_for_api():
            print("❌ Demo cannot proceed - API not available")
            return False
        
        try:
            # Run demo sections
            self.demo_health_check()
            entity_ids = self.demo_create_entities()
            
            if entity_ids:
                self.demo_create_relationships(entity_ids)
                self.demo_analytics(entity_ids)
            
            self.demo_list_operations()
            self.demo_metadata()
            
            print("\n" + "=" * 50)
            print("🎉 Demo completed successfully!")
            print("\nYou can now:")
            print("- Visit http://localhost:8000/docs for interactive API documentation")
            print("- Use the API endpoints to build your own applications")
            print("- Explore the network analysis capabilities")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            return False

if __name__ == "__main__":
    demo = SFMAPIDemo()
    demo.run_full_demo()
