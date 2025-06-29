from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any
from datetime import datetime

# ───────────────────────────────────────────────
# ENUMERATIONS  (shared controlled vocabularies)
# ───────────────────────────────────────────────


class ValueCategory(Enum):
    """
    Categories of value that can be measured and tracked in Social Fabric Matrix analysis.
    
    These categories represent different dimensions of value creation, distribution, and impact
    within socio-economic systems, following Hayden's institutional analysis framework.
    """
    # Original categories
    ECONOMIC = auto()  # Market-priced goods, services, financial returns
    SOCIAL = auto()  # Distributional equity, social cohesion, well-being
    ENVIRONMENTAL = auto()  # Resource stocks, ecological integrity
    CULTURAL = auto()  # Norms, beliefs, heritage
    INSTITUTIONAL = auto()  # Governance quality, rule consistency
    TECHNOLOGICAL = auto()  # Knowledge base, production techniques

    # Additional common SFM value categories
    POLITICAL = auto()  # Power distribution, democratic participation, governance
    EDUCATIONAL = auto()  # Learning outcomes, knowledge transfer, skill development
    HEALTH = auto()  # Public health, medical outcomes, wellness indicators
    SECURITY = auto()  # Safety, defense, risk management, stability
    INFRASTRUCTURE = (
        auto()
    )  # Physical systems, utilities, transportation, communication
    LEGAL = auto()  # Legal frameworks, rights, justice, compliance
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
    TRANSPARENCY = auto()  # Openness, accountability, information access
    PARTICIPATION = auto()  # Stakeholder involvement, democratic engagement
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
    ACCOUNTABILITY = auto()  # Responsibility, oversight, governance
    LEGITIMACY = auto()  # Acceptance, authority, credibility
    CAPACITY = auto()  # Capability, resources, potential
    CONNECTIVITY = auto()  # Networks, relationships, linkages
    FLEXIBILITY = auto()  # Adaptability, responsiveness, agility
    SCALABILITY = auto()  # Growth potential, expansion capability
    INTEROPERABILITY = auto()  # Compatibility, integration, coordination


class InstitutionLayer(Enum):
    """
    Hayden's three-layer institutional framework plus extended institutional forms.
    
    Based on F. Gregory Hayden's analysis of institutional structure, this enum represents
    the different layers at which institutions operate, from formal constitutional rules
    to informal cultural norms, plus additional institutional forms relevant to SFM analysis.
    """
    # Existing values
    FORMAL_RULE = auto()  # Constitutions, statutes, property law
    ORGANIZATION = auto()  # Firms, ministries, NGOs, unions
    INFORMAL_NORM = auto()  # Customs, habits, social expectations

    # Additional values
    CULTURAL_VALUE = auto()  # Deep cultural beliefs that underpin institutions
    POLICY_INSTRUMENT = auto()  # Specific implementation tools (taxes, subsidies)
    MARKET_MECHANISM = auto()  # Price systems, contracts, trading platforms
    NETWORK = auto()  # Collaborative structures, alliances, partnerships
    TECHNOLOGICAL_STANDARD = auto()  # Technical specifications and protocols
    PROFESSIONAL_PRACTICE = auto()  # Professional codes, methodologies, best practices
    COMMUNITY_GOVERNANCE = auto()  # Local and community-based governance
    INTERNATIONAL_REGIME = auto()  # Transnational agreements, treaties
    HYBRID_INSTITUTION = auto()  # Public-private partnerships, mixed governance
    KNOWLEDGE_SYSTEM = auto()  # Scientific paradigms, research programs
    PLANNING_FRAMEWORK = auto()  # Strategic planning systems
    REGULATORY_REGIME = auto()  # Enforcement and compliance systems
    TRADITIONAL_AUTHORITY = auto()  # Customary and indigenous governance structures
    EMERGENT_INSTITUTION = auto()  # Newly forming institutional arrangements


class ResourceType(Enum):
    """
    Classification of resource types within Social Fabric Matrix analysis.
    
    Categorizes different forms of resources that flow through socio-economic systems,
    including traditional economic resources and expanded categories relevant to
    institutional and technological analysis.
    """
    # Existing values
    NATURAL = auto()  # Land, water, raw minerals
    PRODUCED = auto()  # Machinery, infrastructures
    HUMAN = auto()  # Labor, human capital, skills
    INFORMATION = auto()  # Data, R&D findings, patents

    # Financial and Economic Resources
    FINANCIAL = auto()  # Money, securities, investments, financial instruments
    MONETARY = auto()  # Currency, liquid assets, reserves
    CREDIT = auto()  # Loans, debt instruments, financing capabilities
    EQUITY = auto()  # Ownership shares, stock, investment capital

    # Knowledge and Intellectual Resources
    INTELLECTUAL = auto()  # Patents, copyrights, trademarks, intellectual property
    KNOWLEDGE = auto()  # Explicit knowledge, theories, methodologies
    CULTURAL = auto()  # Cultural heritage, traditions, practices, languages
    CREATIVE = auto()  # Artistic, design, and creative works

    # Social and Network Resources
    SOCIAL_CAPITAL = auto()  # Trust networks, relationships, community bonds
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


class FlowNature(Enum):
    """
    Classification of flow types and patterns in Social Fabric Matrix systems.
    
    Describes the nature, direction, timing, and purpose of flows of resources, 
    information, value, and other elements through socio-economic systems.
    Essential for understanding system dynamics and transformation processes.
    """
    # Current basic flow types
    INPUT = auto()  # Resource or value entering a process
    OUTPUT = auto()  # Product, waste, or value leaving a process
    TRANSFER = auto()  # Exchange between actors without transformation

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
    CIRCULAR = auto()  # Returns to origin after processing
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
    INTERNAL = auto()  # Flows contained within system boundaries
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


class RelationshipKind(Enum):
    """
    Taxonomy of relationship types in Social Fabric Matrix systems.
    
    Defines the various ways actors, institutions, resources, and processes can be
    related to each other. Includes governance, economic, social, informational,
    temporal, and ecological relationships, as well as Hayden-specific institutional
    relationships for analyzing ceremonial vs. instrumental patterns.
    """
    # Governance and Authority Relationships
    GOVERNS = auto()  # Authority over another entity
    REGULATES = auto()  # Creates or enforces rules for
    AUTHORIZES = auto()  # Grants permission to
    MANDATES = auto()  # Makes actions compulsory
    ENFORCES = auto()  # Ensures compliance with rules
    DELEGATES = auto()  # Transfers authority to
    REPRESENTS = auto()  # Acts on behalf of
    MONITORS = auto()  # Observes and assesses
    ACCOUNTABLE_TO = auto()  # Must answer to
    LICENSES = auto()  # Formally permits activity
    CERTIFIES = auto()  # Validates compliance or quality
    SANCTIONS = auto()  # Penalizes for non-compliance
    REINFORCES = auto()  # Positive feedback relationship
    UNDERMINES = auto()  # Negative feedback relationship
    AFFECTS = auto()  # Base Feedback relationship
    ENACTS = auto()  # Creates or modifies laws, policies, or regulations

    # Resource Flow Relationships
    FUNDS = auto()  # Provides money to
    PAYS = auto()  # Exchanges money for goods/services
    ALLOCATES = auto()  # Distributes resources to
    TRANSFERS = auto()  # Moves resources without transformation
    EXTRACTS = auto()  # Removes resources from
    CONSUMES = auto()  # Uses up resources from
    PRODUCES = auto()  # Creates outputs for
    DISTRIBUTES = auto()  # Disseminates to multiple targets
    STORES = auto()  # Holds resources for
    CONVERTS = auto()  # Transforms one resource to another
    RECYCLES = auto()  # Reprocesses for reuse

    # Economic and Market Relationships
    BUYS_FROM = auto()  # Purchases goods/services
    SELLS_TO = auto()  # Provides goods/services for payment
    COMPETES_WITH = auto()  # Rivals for resources or markets
    SUPPLIES = auto()  # Provides inputs to
    EMPLOYS = auto()  # Hires for labor
    CONTRACTS_WITH = auto()  # Formal agreement for exchange
    INVESTS_IN = auto()  # Commits resources for future return
    INSURES = auto()  # Provides risk protection for
    SUBSIDIZES = auto()  # Provides financial support to
    TAXES = auto()  # Collects mandatory payment from
    RENTS_TO = auto()  # Provides temporary use rights
    OWNS = auto()  # Has property rights over
    EXCHANGES_WITH = auto()  # Actor-to-actor transfer

    # Knowledge and Information Relationships
    INFORMS = auto()  # Provides information to
    ADVISES = auto()  # Gives guidance to
    EDUCATES = auto()  # Transfers knowledge to
    RESEARCHES = auto()  # Investigates for
    INNOVATES_FOR = auto()  # Creates new solutions for
    DOCUMENTS = auto()  # Records information about
    ANALYZES = auto()  # Examines and interprets
    FORECASTS = auto()  # Predicts outcomes for
    COMMUNICATES_WITH = auto()  # Exchanges information with
    MEASURES = auto()  # Quantifies attributes of
    CALCULATES = auto()  # Computes values related to

    # Social and Collaborative Relationships
    COLLABORATES_WITH = auto()  # Works jointly with
    SERVES = auto()  # Provides services to
    SUPPORTS = auto()  # Helps or assists
    PARTICIPATES_IN = auto()  # Takes part in
    ALLIES_WITH = auto()  # Forms strategic partnership with
    COORDINATES_WITH = auto()  # Aligns activities with
    FACILITATES = auto()  # Makes easier or enables
    MEDIATES = auto()  # Resolves conflicts between
    ADVOCATES_FOR = auto()  # Publicly supports
    ORGANIZES = auto()  # Arranges or structures
    CONVENES = auto()  # Brings together

    # Influence and Impact Relationships
    INFLUENCES = auto()  # Affects decisions or behavior of
    CONSTRAINS = auto()  # Limits actions of
    ENABLES = auto()  # Makes possible actions of
    INCENTIVIZES = auto()  # Motivates specific behaviors
    DISCOURAGES = auto()  # Deters specific behaviors
    SHAPES = auto()  # Molds or forms
    STRENGTHENS = auto()  # Increases capacity of
    WEAKENS = auto()  # Diminishes capacity of
    DISRUPTS = auto()  # Causes discontinuity in
    STABILIZES = auto()  # Maintains equilibrium of
    TRANSFORMS = auto()  # Fundamentally changes

    # Process and Operational Relationships
    IMPLEMENTS = auto()  # Puts into practice
    OPERATES = auto()  # Runs or manages
    MAINTAINS = auto()  # Keeps in working order
    TESTS = auto()  # Evaluates performance of
    INSTALLS = auto()  # Sets up for use
    TRANSPORTS = auto()  # Moves from one location to another
    INTEGRATES = auto()  # Combines into system
    OPTIMIZES = auto()  # Improves efficiency of
    AUTOMATES = auto()  # Makes self-operating
    REPAIRS = auto()  # Fixes or restores
    USES = auto()  # Actor/process employs a resource or technology

    # Structural and Containment Relationships
    CONTAINS = auto()  # Has as a component
    BELONGS_TO = auto()  # Is a member of
    CONNECTS = auto()  # Links physically or logically
    COMPOSED_OF = auto()  # Consists of
    CATEGORIZES = auto()  # Places in classification
    AGGREGATES = auto()  # Combines into a whole
    SEPARATES = auto()  # Divides or keeps apart
    HOSTS = auto()  # Provides environment for
    ATTACHES_TO = auto()  # Joins or fixes to
    EMBEDS_WITHIN = auto()  # Incorporates deeply into
    ENCOMPASSES = auto()  # Includes completely
    LOCATED_IN = auto()  # Spatial anchoring

    # Temporal and Sequential Relationships
    PRECEDES = auto()  # Comes before
    FOLLOWS = auto()  # Comes after
    TRIGGERS = auto()  # Initiates or causes
    SYNCHRONIZES_WITH = auto()  # Coordinates timing with
    DELAYS = auto()  # Postpones or slows
    ACCELERATES = auto()  # Speeds up
    SCHEDULES = auto()  # Sets timing for
    ITERATES = auto()  # Repeats process with
    SUPERSEDES = auto()  # Replaces or makes obsolete
    RENEWS = auto()  # Extends or refreshes
    TERMINATES = auto()  # Ends relationship with
    OCCURS_DURING = auto()  # Temporal anchoring
    ENABLES_FUTURE = auto()
    CONSTRAINS_FUTURE = auto()

    # Environmental and Ecological Relationships
    SUSTAINS = auto()  # Maintains viability of
    POLLUTES = auto()  # Degrades quality of
    CONSERVES = auto()  # Uses carefully to prevent depletion
    RESTORES = auto()  # Returns to previous condition
    ADAPTS_TO = auto()  # Changes in response to
    MITIGATES = auto()  # Reduces negative impact on
    DEPENDS_ON = auto()  # Requires for functioning
    COEXISTS_WITH = auto()  # Lives alongside without harm
    HARVESTS = auto()  # Collects resources from
    PROCESSES = auto()  # Treats or handles materials from
    CULTIVATES = auto()  # Grows or nurtures

    # Development and Change Relationships
    DEVELOPS = auto()  # Creates growth or maturity in
    EXPANDS = auto()  # Increases size or scope of
    CONTRACTS = auto()  # Decreases size or scope of
    REDESIGNS = auto()  # Changes structure or function of
    EVOLVES_WITH = auto()  # Changes in mutual response with
    EMERGES_FROM = auto()  # Comes into existence from
    TRANSITIONS_TO = auto()  # Changes state to become
    CONSTRUCTS = auto()  # Builds or creates
    DEMOLISHES = auto()  # Tears down or removes
    UPGRADES = auto()  # Improves quality or function of
    CUSTOMIZES = auto()  # Modifies to suit specific needs
    INHIBITS = auto()  # Limiting or constraining relationship

    # Belief and Value Relationships
    VALUES = auto()  # Holds in high regard
    TRUSTS = auto()  # Has confidence in
    PERCEIVES = auto()  # Forms mental impression of
    INTERPRETS = auto()  # Ascribes meaning to
    CHALLENGES = auto()  # Questions validity of
    ACCEPTS = auto()  # Receives as valid or appropriate
    REJECTS = auto()  # Refuses to accept
    NORMALIZES = auto()  # Makes conform to standard
    PRIORITIZES = auto()  # Gives precedence to
    ALIGNS_WITH = auto()  # Positions in agreement with
    DISAGREES_WITH = auto()  # Holds contrary views to
    BELIEVES_IN = auto()  # Holds a conviction about

    # Hayden-specific relationships
    LEGITIMIZES = auto()
    DELEGITIMIZES = auto()
    CEREMONIALLY_REINFORCES = auto()
    INSTRUMENTALLY_ADAPTS = auto()
    CREATES_PATH_DEPENDENCY = auto()
    ENABLES_INNOVATION = auto()
    DISTRIBUTES_POWER = auto()
    CONCENTRATES_POWER = auto()
    BENEFITS_FROM = auto()  # Gains advantage or support from
