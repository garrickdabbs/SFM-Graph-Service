"""
Enumerations for the Social Fabric Matrix (SFM) framework.

This module defines controlled vocabularies and classification systems used throughout
the SFM analysis framework. These enumerations provide consistent categorization for
values, institutions, resources, flows, and relationships in socio-economic systems.
"""

from __future__ import annotations

from enum import Enum, auto

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


class FlowType(Enum):
    """
    Classification of flow types by medium/content in Social Fabric Matrix systems.
    
    Defines the fundamental types of flows that can occur between actors, processes,
    and resources in socio-economic systems.
    """
    MATERIAL = auto()  # Physical goods and substances
    ENERGY = auto()  # Power, heat, electricity flows
    INFORMATION = auto()  # Data, knowledge, signals
    FINANCIAL = auto()  # Money, credit, financial instruments
    SOCIAL = auto()  # Relationships, trust, social capital


class PolicyInstrumentType(Enum):
    """
    Classification of policy instrument types for implementation analysis.
    
    Categorizes the different mechanisms through which policies can be implemented
    and enforced in socio-economic systems.
    """
    REGULATORY = auto()  # Rules, regulations, legal requirements
    ECONOMIC = auto()  # Taxes, subsidies, market-based mechanisms
    VOLUNTARY = auto()  # Voluntary agreements, codes of conduct
    INFORMATION = auto()  # Education, disclosure, awareness campaigns


class ChangeType(Enum):
    """
    Classification of institutional and technological change patterns.
    
    Defines different modes of change that can occur in socio-economic systems,
    following institutional economics and innovation theory.
    """
    EVOLUTIONARY = auto()  # Gradual, adaptive change
    REVOLUTIONARY = auto()  # Rapid, disruptive transformation
    CYCLICAL = auto()  # Recurring patterns of change
    INCREMENTAL = auto()  # Small, continuous improvements


class BehaviorPatternType(Enum):
    """
    Classification of behavioral patterns in Social Fabric Matrix analysis.
    
    Categorizes recurring patterns of behavior that actors exhibit in
    socio-economic systems.
    """
    HABITUAL = auto()  # Routine, unconscious behaviors
    STRATEGIC = auto()  # Deliberate, goal-oriented behaviors
    ADAPTIVE = auto()  # Flexible, responsive behaviors
    RESISTANT = auto()  # Change-resistant, conservative behaviors


class FeedbackPolarity(Enum):
    """
    Classification of feedback loop polarity in system dynamics.
    
    Defines whether a feedback loop reinforces or balances system behavior.
    """
    REINFORCING = auto()  # Amplifies or accelerates change (positive feedback)
    BALANCING = auto()  # Stabilizes or counteracts change (negative feedback)


class FeedbackType(Enum):
    """
    Classification of feedback types by directional impact.
    
    Categorizes feedback effects based on their directional influence
    on system behavior.
    """
    POSITIVE = auto()  # Enhancing, amplifying feedback
    NEGATIVE = auto()  # Dampening, correcting feedback
    NEUTRAL = auto()  # Balanced or minimal feedback


class TemporalFunctionType(Enum):
    """
    Classification of temporal function types for modeling change over time.
    
    Defines mathematical functions used to model how values change
    over time in temporal dynamics analysis.
    """
    LINEAR = auto()  # Constant rate of change
    EXPONENTIAL = auto()  # Accelerating or decelerating change
    LOGISTIC = auto()  # S-curve growth with limits
    CYCLICAL = auto()  # Periodic, repeating patterns
    STEP = auto()  # Discrete jumps or threshold changes
    RANDOM = auto()  # Stochastic or unpredictable changes


class ValidationRuleType(Enum):
    """
    Classification of validation rule types for data integrity.
    
    Defines different types of validation rules that can be applied
    to ensure data quality and consistency.
    """
    RANGE = auto()  # Value within specified bounds
    SUM = auto()  # Sum constraints across multiple values
    REQUIRED = auto()  # Mandatory field validation
    UNIQUE = auto()  # Uniqueness constraints
    FORMAT = auto()  # Format or pattern validation
    RELATIONSHIP = auto()  # Cross-field relationship validation


class SystemPropertyType(Enum):
    """
    Classification of system-level property types in SFM analysis.
    
    Defines different categories of system-level metrics and properties
    that can be measured and tracked.
    """
    STRUCTURAL = auto()  # Network structure properties
    DYNAMIC = auto()  # Temporal behavior properties
    PERFORMANCE = auto()  # Efficiency and effectiveness metrics
    RESILIENCE = auto()  # Adaptive capacity and robustness
    EQUITY = auto()  # Distributional fairness metrics
    SUSTAINABILITY = auto()  # Long-term viability indicators


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
    SOLVES = auto()  # Addresses problems or challenges
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

    @property
    def ceremonial_tendency(self) -> float:
        """
        Returns a value from 0.0-1.0 indicating ceremonial vs instrumental nature.
        
        Based on Hayden's SFM framework distinction between ceremonial and instrumental
        behaviors. 0.0 = purely instrumental (problem-solving, adaptive), 
        1.0 = purely ceremonial (status-preserving, traditional).
        
        Returns:
            float: Ceremonial tendency score from 0.0 (instrumental) to 1.0 (ceremonial)
        """
        # Mapping of relationship types to their ceremonial tendency
        ceremonial_tendencies = {
            # Highly ceremonial relationships (0.8-1.0) - status, tradition, hierarchy
            RelationshipKind.CEREMONIALLY_REINFORCES: 0.95,
            RelationshipKind.LEGITIMIZES: 0.85,
            RelationshipKind.GOVERNS: 0.75,
            RelationshipKind.AUTHORIZES: 0.75,
            RelationshipKind.MANDATES: 0.75,
            RelationshipKind.REPRESENTS: 0.70,
            RelationshipKind.SANCTIONS: 0.80,
            RelationshipKind.VALUES: 0.85,
            RelationshipKind.TRUSTS: 0.70,
            RelationshipKind.BELIEVES_IN: 0.80,
            RelationshipKind.NORMALIZES: 0.75,
            RelationshipKind.PRIORITIZES: 0.70,
            
            # Moderately ceremonial (0.5-0.8) - mixed institutional/adaptive
            RelationshipKind.REGULATES: 0.65,
            RelationshipKind.ENFORCES: 0.65,
            RelationshipKind.DELEGATES: 0.60,
            RelationshipKind.MONITORS: 0.55,
            RelationshipKind.LICENSES: 0.60,
            RelationshipKind.CERTIFIES: 0.55,
            RelationshipKind.REINFORCES: 0.60,
            RelationshipKind.ALIGNS_WITH: 0.55,
            RelationshipKind.ACCEPTS: 0.55,
            RelationshipKind.INTERPRETS: 0.50,
            
            # Moderately instrumental (0.2-0.5) - some adaptation with structure
            RelationshipKind.ADVISES: 0.45,
            RelationshipKind.EDUCATES: 0.40,
            RelationshipKind.INFORMS: 0.35,
            RelationshipKind.ANALYZES: 0.30,
            RelationshipKind.MEASURES: 0.25,
            RelationshipKind.CALCULATES: 0.20,
            RelationshipKind.RESEARCHES: 0.30,
            RelationshipKind.INNOVATES_FOR: 0.25,
            RelationshipKind.DEVELOPS: 0.35,
            RelationshipKind.EVOLVES_WITH: 0.40,
            RelationshipKind.ADAPTS_TO: 0.35,
            
            # Highly instrumental (0.0-0.2) - problem-solving, adaptive, productive
            RelationshipKind.INSTRUMENTALLY_ADAPTS: 0.05,
            RelationshipKind.PRODUCES: 0.15,
            RelationshipKind.PROCESSES: 0.10,
            RelationshipKind.CONVERTS: 0.10,
            RelationshipKind.CONSTRUCTS: 0.15,
            RelationshipKind.OPERATES: 0.15,
            RelationshipKind.MAINTAINS: 0.20,
            RelationshipKind.REPAIRS: 0.15,
            RelationshipKind.UPGRADES: 0.20,
            RelationshipKind.CUSTOMIZES: 0.15,
            RelationshipKind.ENABLES_INNOVATION: 0.10,
            RelationshipKind.SOLVES: 0.05,
            
            # Economic relationships - moderately instrumental (0.3-0.6)
            RelationshipKind.EXCHANGES_WITH: 0.40,
            RelationshipKind.BUYS_FROM: 0.35,
            RelationshipKind.SELLS_TO: 0.35,
            RelationshipKind.INVESTS_IN: 0.45,
            RelationshipKind.EMPLOYS: 0.50,
            RelationshipKind.CONTRACTS_WITH: 0.45,
            RelationshipKind.FUNDS: 0.40,
            RelationshipKind.PAYS: 0.30,
            RelationshipKind.ALLOCATES: 0.45,
            RelationshipKind.DISTRIBUTES: 0.40,
        }
        
        # Return the mapped value, or default to moderate (0.5) if not explicitly mapped
        return ceremonial_tendencies.get(self, 0.5)


class PowerResourceType(Enum):
    """
    Classification of power resource types in Social Fabric Matrix analysis.
    
    Based on Hayden's analysis of power dynamics within institutional systems,
    representing different forms of power and control that actors can wield
    to influence outcomes and maintain or change institutional arrangements.
    """
    INSTITUTIONAL_AUTHORITY = auto()  # Formal authority roles and positions
    ECONOMIC_CONTROL = auto()  # Control over financial resources and economic flows
    INFORMATION_ACCESS = auto()  # Access to and control of information and knowledge
    NETWORK_POSITION = auto()  # Strategic position within social and institutional networks
    CULTURAL_LEGITIMACY = auto()  # Cultural authority and legitimacy sources


class ToolSkillTechnologyType(Enum):
    """
    Classification of tool-skill-technology complex components.
    
    Represents Hayden's concept of the tool-skill-technology complex as integrated
    systems where physical tools, human skills, and technological knowledge
    combine to enable instrumental problem-solving capabilities.
    """
    PHYSICAL_TOOL = auto()  # Material instruments and devices
    COGNITIVE_SKILL = auto()  # Mental capabilities and knowledge
    TECHNOLOGY_SYSTEM = auto()  # Integrated technological arrangements
    TECHNIQUE = auto()  # Specific methods and procedures
    METHODOLOGY = auto()  # Systematic approaches and frameworks
    CRAFT_KNOWLEDGE = auto()  # Embodied practical knowledge
    DIGITAL_CAPABILITY = auto()  # Digital tools and skills
    ANALYTICAL_METHOD = auto()  # Formal analytical techniques
    PROBLEM_SOLVING_APPROACH = auto()  # General problem-solving strategies
    INNOVATION_CAPACITY = auto()  # Capability to create new solutions


class PathDependencyType(Enum):
    """
    Classification of path dependency strength in institutional systems.
    
    Represents the degree to which institutional arrangements become locked-in
    and resistant to change due to historical patterns, sunk costs, and
    reinforcing mechanisms.
    """
    WEAK = auto()  # Easy to change, low switching costs, flexible arrangements
    MODERATE = auto()  # Some resistance to change, moderate switching costs
    STRONG = auto()  # High resistance to change, significant switching costs
    LOCKED_IN = auto()  # Extremely difficult to change, path dependency dominates


class InstitutionalChangeType(Enum):
    """
    Classification of institutional change mechanisms and patterns.
    
    Represents different modes and patterns through which institutional
    arrangements evolve, transform, or maintain stability over time.
    """
    INCREMENTAL = auto()  # Gradual, small-scale adjustments
    TRANSFORMATIONAL = auto()  # Significant structural changes
    REVOLUTIONARY = auto()  # Rapid, fundamental system overhaul
    EVOLUTIONARY = auto()  # Organic adaptation over time
    ADAPTIVE = auto()  # Responsive changes to environmental pressures
    CRISIS_DRIVEN = auto()  # Changes triggered by system crises
    INNOVATION_LED = auto()  # Changes driven by technological or social innovation
    REFORM_BASED = auto()  # Planned, policy-driven changes
    EMERGENT = auto()  # Bottom-up, spontaneous changes
    CYCLICAL = auto()  # Recurring patterns of change and stability


# ───────────────────────────────────────────────
# ERROR HANDLING AND VALIDATION
# ───────────────────────────────────────────────


class SFMEnumError(Exception):
    """Base exception for SFM enum-related errors."""
    pass


class IncompatibleEnumError(SFMEnumError):
    """Raised when incompatible enum values are used together."""
    pass


class InvalidEnumOperationError(SFMEnumError):
    """Raised when an invalid operation is attempted on enum values."""
    pass


class EnumValidator:
    """Validates enum values and combinations for SFM consistency."""
    
    # Define node type mappings - these correspond to the actual model classes
    ACTOR_TYPES = {'Actor'}
    INSTITUTION_TYPES = {'Institution', 'Policy'}
    RESOURCE_TYPES = {'Resource'}
    PROCESS_TYPES = {'Process', 'Flow'}
    SYSTEM_TYPES = {'TechnologySystem', 'BeliefSystem', 'ValueSystem'}
    OTHER_TYPES = {'FeedbackLoop', 'Indicator', 'AnalyticalContext', 'SystemProperty', 
                   'CeremonialBehavior', 'InstrumentalBehavior', 'PolicyInstrument'}
    
    # Define relationship context rules
    RELATIONSHIP_RULES = {
        RelationshipKind.GOVERNS: {
            'valid_combinations': [
                ('Actor', 'Actor'),
                ('Actor', 'Institution'),
                ('Actor', 'Policy'),
                ('Actor', 'Resource'),  # Actors can govern resources (ownership, stewardship)
                ('Institution', 'Institution'),
                ('Institution', 'Actor'),
                ('Institution', 'Policy'),  # Institutions can govern policies
                ('Institution', 'Resource'),  # Institutions can govern/regulate resources
                ('Policy', 'Actor'),
                ('Policy', 'Institution'),
                ('Policy', 'Resource')  # Policies can govern resources (regulations)
            ],
            'description': 'GOVERNS relationship requires entities capable of authority or regulation',
            'invalid_message': 'GOVERNS relationship requires authority-capable entities (Actors, Institutions, Policies) governing appropriate targets'
        },
        RelationshipKind.EMPLOYS: {
            'valid_combinations': [
                ('Actor', 'Actor'),
                ('Institution', 'Actor')  # Organizations can employ people
            ],
            'description': 'EMPLOYS relationship for labor relationships',
            'invalid_message': 'EMPLOYS relationship requires Actor or Institution employing Actor entities'
        },
        RelationshipKind.OWNS: {
            'valid_combinations': [
                ('Actor', 'Resource'),
                ('Institution', 'Resource'),
                ('Actor', 'TechnologySystem'),
                ('Institution', 'TechnologySystem')
            ],
            'description': 'OWNS relationship requires an entity capable of ownership and an ownable resource',
            'invalid_message': 'OWNS relationship requires Actor/Institution owning Resource/TechnologySystem'
        },
        RelationshipKind.USES: {
            'valid_combinations': [
                ('Actor', 'Resource'),
                ('Process', 'Resource'),
                ('Actor', 'TechnologySystem'),
                ('Process', 'TechnologySystem'),
                ('Actor', 'Institution'),
                ('Process', 'Institution')
            ],
            'description': 'USES relationship requires a user and a usable entity',
            'invalid_message': 'USES relationship requires Actor/Process using Resource/TechnologySystem/Institution'
        },
        RelationshipKind.PRODUCES: {
            'valid_combinations': [
                ('Actor', 'Resource'),
                ('Process', 'Resource'),
                ('TechnologySystem', 'Resource'),
                ('Actor', 'Flow'),
                ('Process', 'Flow'),
                ('TechnologySystem', 'Flow'),
                ('Actor', 'ValueFlow'),
                ('Process', 'ValueFlow'),
                ('TechnologySystem', 'ValueFlow'),
                ('PolicyInstrument', 'Flow'),
                ('PolicyInstrument', 'ValueFlow'),
                ('PolicyInstrument', 'Resource')
            ],
            'description': 'PRODUCES relationship requires a producer and a producible output',
            'invalid_message': 'PRODUCES relationship requires Actor/Process/TechnologySystem/PolicyInstrument producing Resource/Flow/ValueFlow'
        }
    }
    
    @staticmethod
    def validate_relationship_context(
        kind: RelationshipKind, 
        source_type: str, 
        target_type: str
    ) -> None:
        """Validate that relationship makes sense in context.
        
        Args:
            kind: The type of relationship
            source_type: Type of source node (class name)
            target_type: Type of target node (class name)
            
        Raises:
            IncompatibleEnumError: If relationship doesn't make sense
            InvalidEnumOperationError: If invalid parameters provided
        """
        if not isinstance(kind, RelationshipKind):
            raise InvalidEnumOperationError(
                f"Expected RelationshipKind, got {type(kind).__name__}"
            )
        
        if not source_type or not target_type:
            raise InvalidEnumOperationError(
                "Source and target types must be provided and non-empty"
            )
        
        # Check if we have specific rules for this relationship kind
        if kind in EnumValidator.RELATIONSHIP_RULES:
            rule = EnumValidator.RELATIONSHIP_RULES[kind]
            valid_combinations = rule['valid_combinations']
            
            if (source_type, target_type) not in valid_combinations:
                suggestions = EnumValidator._generate_suggestions(kind, source_type, target_type)
                raise IncompatibleEnumError(
                    f"{rule['invalid_message']}. "
                    f"Got {source_type}->{target_type}. "
                    f"{suggestions}"
                )
    
    @staticmethod
    def validate_flow_combination(nature: FlowNature, flow_type: FlowType) -> None:
        """Validate that flow nature and type are compatible.
        
        Args:
            nature: The nature of the flow
            flow_type: The type of the flow
            
        Raises:
            IncompatibleEnumError: If flow nature and type are incompatible
            InvalidEnumOperationError: If invalid parameters provided
        """
        if not isinstance(nature, FlowNature):
            raise InvalidEnumOperationError(
                f"Expected FlowNature, got {type(nature).__name__}"
            )
        
        if not isinstance(flow_type, FlowType):
            raise InvalidEnumOperationError(
                f"Expected FlowType, got {type(flow_type).__name__}"
            )
        
        # Define obviously incompatible combinations (semantically impossible)
        strictly_incompatible = {
            # These combinations are clearly nonsensical
            (FlowNature.ENERGY, FlowType.INFORMATION),
            (FlowNature.INFORMATION, FlowType.ENERGY)
        }
        
        if (nature, flow_type) in strictly_incompatible:
            raise IncompatibleEnumError(
                f"Flow nature {nature.name} is semantically incompatible with flow type {flow_type.name}. "
                f"Consider using compatible combinations."
            )
    
    @staticmethod
    def validate_institution_layer_context(
        layer: InstitutionLayer,
        institution_type: str
    ) -> None:
        """Validate that institution layer makes sense for the institution type.
        
        Args:
            layer: The institutional layer
            institution_type: Type of institution
            
        Raises:
            IncompatibleEnumError: If layer doesn't match institution type
            InvalidEnumOperationError: If invalid parameters provided
        """
        if not isinstance(layer, InstitutionLayer):
            raise InvalidEnumOperationError(
                f"Expected InstitutionLayer, got {type(layer).__name__}"
            )
        
        # Formal rules should typically apply to formal institutions
        if layer == InstitutionLayer.FORMAL_RULE and institution_type in ['BeliefSystem', 'ValueSystem']:
            raise IncompatibleEnumError(
                f"FORMAL_RULE layer is typically not appropriate for {institution_type}. "
                f"Consider using CULTURAL_VALUE or KNOWLEDGE_SYSTEM layers for belief/value systems."
            )
    
    @staticmethod
    def _generate_suggestions(kind: RelationshipKind, source_type: str, target_type: str) -> str:
        """Generate helpful suggestions for valid combinations."""
        if kind in EnumValidator.RELATIONSHIP_RULES:
            valid_combinations = EnumValidator.RELATIONSHIP_RULES[kind]['valid_combinations']
            
            # Find suggestions for the source type
            source_suggestions = [combo[1] for combo in valid_combinations if combo[0] == source_type]
            target_suggestions = [combo[0] for combo in valid_combinations if combo[1] == target_type]
            
            suggestions = []
            if source_suggestions:
                suggestions.append(f"For {source_type} sources, valid targets are: {', '.join(set(source_suggestions))}")
            if target_suggestions:
                suggestions.append(f"For {target_type} targets, valid sources are: {', '.join(set(target_suggestions))}")
            
            if suggestions:
                return "Suggestions: " + "; ".join(suggestions)
        
        return "Check the relationship documentation for valid combinations."


def validate_enum_operation(operation_name: str):
    """Decorator to validate enum operations and provide better error messages.
    
    Args:
        operation_name: Name of the operation being performed
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError, AttributeError) as e:
                raise InvalidEnumOperationError(
                    f"Invalid {operation_name} operation: {str(e)}"
                ) from e
        return wrapper
    return decorator
