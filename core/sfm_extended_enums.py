"""
Extended enumerations for specialized SFM framework analysis.

This module contains extended enum values for specialized use cases that
are not needed in typical SFM operations. These enums are loaded on-demand
to minimize memory usage for common operations.
"""

from __future__ import annotations
from enum import Enum, auto


class GovernanceValueCategory(Enum):
    """Extended value categories for governance and institutional analysis."""
    POLITICAL = auto()  # Power distribution, democratic participation, governance
    LEGAL = auto()  # Legal frameworks, rights, justice, compliance
    ACCOUNTABILITY = auto()  # Responsibility, oversight, governance
    TRANSPARENCY = auto()  # Openness, accountability, information access
    LEGITIMACY = auto()  # Acceptance, authority, credibility
    PARTICIPATION = auto()  # Stakeholder involvement, democratic engagement


class SpecializedValueCategory(Enum):
    """Specialized value categories for detailed analysis."""
    EDUCATIONAL = auto()  # Learning outcomes, knowledge transfer, skill development
    HEALTH = auto()  # Public health, medical outcomes, wellness indicators
    SECURITY = auto()  # Safety, defense, risk management, stability
    INFRASTRUCTURE = auto()  # Physical systems, utilities, transportation, communication
    ETHICAL = auto()  # Moral considerations, fairness, integrity
    AESTHETIC = auto()  # Beauty, design quality, artistic value
    RECREATIONAL = auto()  # Leisure, entertainment, quality of life
    SPIRITUAL = auto()  # Religious values, meaning, purpose
    DEMOGRAPHIC = auto()  # Population characteristics, migration, age structure
    SPATIAL = auto()  # Geographic distribution, land use, location value
    TEMPORAL = auto()  # Time preferences, sustainability, intergenerational equity
    INFORMATIONAL = auto()  # Data quality, knowledge systems, communication
    PSYCHOLOGICAL = auto()  # Mental health, stress, satisfaction, motivation
    COMMUNITY = auto()  # Social capital, civic engagement, collective action
    RESOURCE = auto()  # Natural resource management, conservation, efficiency
    PERFORMANCE = auto()  # Effectiveness, efficiency, productivity measures
    QUALITY = auto()  # Standards, excellence, reliability
    ACCESSIBILITY = auto()  # Inclusion, barrier removal, universal design
    RESILIENCE = auto()  # Adaptability, recovery capacity, robustness
    INNOVATION = auto()  # Creativity, research, development, change capacity
    EQUITY = auto()  # Fairness, distributive justice, equal opportunity
    SUSTAINABILITY = auto()  # Long-term viability, resource preservation
    DIVERSITY = auto()  # Variety, inclusion, representation
    COOPERATION = auto()  # Collaboration, partnership, collective action
    COMPETITIVENESS = auto()  # Market position, comparative advantage
    MOBILITY = auto()  # Movement, transportation, migration
    COMMUNICATION = auto()  # Information flow, dialogue, understanding
    ADAPTATION = auto()  # Flexibility, responsiveness, evolution
    INTEGRATION = auto()  # Coordination, coherence, synergy
    AUTONOMY = auto()  # Independence, self-determination, freedom
    STABILITY = auto()  # Consistency, predictability, equilibrium
    EFFICIENCY = auto()  # Resource optimization, productivity, waste reduction
    EFFECTIVENESS = auto()  # Goal achievement, impact, outcomes
    CAPACITY = auto()  # Capability, resources, potential
    CONNECTIVITY = auto()  # Networks, relationships, linkages
    FLEXIBILITY = auto()  # Adaptability, responsiveness, agility
    SCALABILITY = auto()  # Growth potential, expansion capability
    INTEROPERABILITY = auto()  # Compatibility, integration, coordination


class SpecializedResourceType(Enum):
    """Extended resource types for detailed resource analysis."""
    # Financial and Economic Resources
    MONETARY = auto()  # Currency, liquid assets, reserves
    CREDIT = auto()  # Loans, debt instruments, financing capabilities
    EQUITY = auto()  # Ownership shares, stock, investment capital
    
    # Knowledge and Intellectual Resources
    INTELLECTUAL = auto()  # Patents, copyrights, trademarks, intellectual property
    KNOWLEDGE = auto()  # Explicit knowledge, theories, methodologies
    CULTURAL = auto()  # Cultural heritage, traditions, practices, languages
    CREATIVE = auto()  # Artistic, design, and creative works
    
    # Social and Network Resources
    REPUTATIONAL = auto()  # Brand value, goodwill, credibility
    POLITICAL = auto()  # Influence, power, representation
    ACCESS = auto()  # Rights of entry or use, permissions, privileges
    
    # Infrastructure and Physical Resources
    BUILT = auto()  # Buildings, physical structures, permanent installations
    UTILITY = auto()  # Water systems, energy grids, telecommunications networks
    TRANSPORTATION = auto()  # Mobility infrastructure, vehicles, transit systems
    HOUSING = auto()  # Residential structures and communities
    
    # Energy Resources
    FOSSIL_FUEL = auto()  # Coal, oil, natural gas
    RENEWABLE = auto()  # Solar, wind, hydro, geothermal
    NUCLEAR = auto()  # Fission and fusion materials and facilities
    BIOENERGY = auto()  # Biomass, biofuels, organic energy sources
    
    # Natural Resources Subcategories
    LAND = auto()  # Territory, real estate, soil
    WATER = auto()  # Fresh water, marine resources, aquifers
    MINERAL = auto()  # Metals, stones, extractive resources
    BIOLOGICAL = auto()  # Flora, fauna, genetic resources
    ECOSYSTEM_SERVICE = auto()  # Natural processes, climate regulation, pollination
    
    # Technological Resources
    DIGITAL = auto()  # Software, algorithms, digital assets
    COMPUTATIONAL = auto()  # Computing capacity, processing power
    DATA = auto()  # Organized information, datasets, records
    NETWORK_INFRASTRUCTURE = auto()  # Internet, telecommunications, connectivity
    
    # Time-based Resources
    TEMPORAL = auto()  # Time availability, scheduling capacity
    HISTORICAL = auto()  # Past events, precedent, legacy resources
    FUTURE_OPTION = auto()  # Rights to future resources or opportunities
    
    # Capacity and System Resources
    ORGANIZATIONAL = auto()  # Structural capacity, institutional frameworks
    LOGISTICAL = auto()  # Supply chains, distribution capabilities
    REGULATORY = auto()  # Permits, certifications, compliance assets
    MANAGERIAL = auto()  # Coordination capabilities, administration
    RESILIENCE = auto()  # Adaptive capacity, redundancy, backup systems


class SpecializedFlowNature(Enum):
    """Extended flow natures for detailed flow analysis."""
    # Transformation-based flows
    CONVERSION = auto()  # Resources transformed from one form to another
    EXTRACTION = auto()  # Removal of resources from natural systems
    PROCESSING = auto()  # Intermediate transformation steps
    RECYCLING = auto()  # Reprocessing of materials for reuse
    WASTE = auto()  # Unwanted byproducts or residuals
    DEGRADATION = auto()  # Reduction in quality or utility
    RESTORATION = auto()  # Renewal or repair of resources
    
    # Medium-based flows
    FINANCIAL = auto()  # Money, credit, financial instruments
    MATERIAL = auto()  # Physical goods and substances
    ENERGY = auto()  # Power, heat, electricity flows
    INFORMATION = auto()  # Data, knowledge, signals
    CULTURAL = auto()  # Values, practices, symbols
    SOCIAL = auto()  # Relationships, trust, social capital
    SERVICE = auto()  # Non-physical value delivery
    REGULATORY = auto()  # Control signals, permissions, constraints
    
    # Directionality flows
    CASCADING = auto()  # Sequential flows through multiple processes
    RECIPROCAL = auto()  # Bidirectional exchanges
    DISTRIBUTIVE = auto()  # One-to-many flows (distribution)
    CUMULATIVE = auto()  # Flows that build up or accumulate over time
    FEEDBACK = auto()  # Information returned to control processes
    
    # Temporal pattern flows
    CONTINUOUS = auto()  # Steady, uninterrupted flows
    INTERMITTENT = auto()  # Irregular or sporadic flows
    PULSED = auto()  # Regular bursts of flow
    SEASONAL = auto()  # Flows tied to natural or social cycles
    ACCELERATING = auto()  # Flows increasing in rate
    DECELERATING = auto()  # Flows decreasing in rate
    THRESHOLD = auto()  # Flows that occur after conditions are met
    
    # Purpose-based flows
    PROVISIONING = auto()  # Providing goods or services
    REGULATING = auto()  # Controlling system processes
    SUPPORTING = auto()  # Enabling other flows or processes
    MAINTENANCE = auto()  # Preserving system functions
    GROWTH = auto()  # Expanding system capacity
    INVESTMENT = auto()  # Building future capacity
    CONSUMPTION = auto()  # Using up resources for immediate benefit
    
    # Boundary-crossing flows
    IMPORT = auto()  # Flows entering from outside the system
    EXPORT = auto()  # Flows leaving the system
    TRANSBOUNDARY = auto()  # Flows crossing multiple boundaries
    SPILLOVER = auto()  # Unintended flows across boundaries
    LEAKAGE = auto()  # Unintended escape of resources from system
    
    # Specific economic flows
    TAXATION = auto()  # Mandatory payments to governmental entities
    SUBSIDY = auto()  # Support payments from government to entities
    DIVIDEND = auto()  # Distribution of profits to shareholders
    WAGE = auto()  # Compensation for labor
    RENT = auto()  # Payment for use of property or resources
    INTEREST = auto()  # Payment for use of borrowed capital
    
    # Governance and institutional flows
    MANDATE = auto()  # Authoritative directives or requirements
    COMPLIANCE = auto()  # Conformity with rules or standards
    AUTHORIZATION = auto()  # Formal permission or approval
    CERTIFICATION = auto()  # Verification of adherence to standards
    REPORTING = auto()  # Required information disclosure