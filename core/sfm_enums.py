"""
Enumerations for the Social Fabric Matrix (SFM) framework.

This module defines controlled vocabularies and classification systems used throughout
the SFM analysis framework. These enumerations provide consistent categorization for
values, institutions, resources, flows, and relationships in socio-economic systems.

MEMORY OPTIMIZATION:
This module now uses a split approach for memory efficiency:
- Core enums contain the most frequently used values (loaded by default)
- Extended enums contain specialized values (loaded on-demand)
- Backward compatibility is maintained through dynamic enum creation

For memory-efficient usage, import from core modules directly:
    from core.sfm_core_enums import CoreValueCategory, CoreResourceType
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Union, Type, Dict, Any, Optional
import logging

# Core enums - loaded by default for common operations
from .sfm_core_enums import (
    CoreValueCategory,
    CoreRelationshipKind, 
    CoreResourceType,
    CoreFlowNature
)

# Lazy loading for extended enums
_extended_enums_loaded = False
_relationship_enums_loaded = False

logger = logging.getLogger(__name__)

# ───────────────────────────────────────────────
# LAZY LOADING HELPERS
# ───────────────────────────────────────────────

def _load_extended_enums():
    """Load extended enum modules on demand."""
    global _extended_enums_loaded
    if not _extended_enums_loaded:
        try:
            from .sfm_extended_enums import (
                GovernanceValueCategory,
                SpecializedValueCategory, 
                SpecializedResourceType,
                SpecializedFlowNature
            )
            globals().update({
                'GovernanceValueCategory': GovernanceValueCategory,
                'SpecializedValueCategory': SpecializedValueCategory,
                'SpecializedResourceType': SpecializedResourceType, 
                'SpecializedFlowNature': SpecializedFlowNature
            })
            _extended_enums_loaded = True
            logger.debug("Extended enums loaded successfully")
        except ImportError as e:
            logger.warning(f"Failed to load extended enums: {e}")

def _load_relationship_enums():
    """Load relationship enum modules on demand."""
    global _relationship_enums_loaded
    if not _relationship_enums_loaded:
        try:
            from .sfm_relationship_enums import (
                GovernanceRelationshipKind,
                EconomicRelationshipKind,
                ResourceFlowRelationshipKind,
                InformationRelationshipKind,
                SocialRelationshipKind,
                InfluenceRelationshipKind,
                ProcessRelationshipKind,
                StructuralRelationshipKind,
                TemporalRelationshipKind,
                EnvironmentalRelationshipKind,
                ChangeRelationshipKind,
                BeliefRelationshipKind,
                HaydenRelationshipKind
            )
            globals().update({
                'GovernanceRelationshipKind': GovernanceRelationshipKind,
                'EconomicRelationshipKind': EconomicRelationshipKind,
                'ResourceFlowRelationshipKind': ResourceFlowRelationshipKind,
                'InformationRelationshipKind': InformationRelationshipKind,
                'SocialRelationshipKind': SocialRelationshipKind,
                'InfluenceRelationshipKind': InfluenceRelationshipKind,
                'ProcessRelationshipKind': ProcessRelationshipKind,
                'StructuralRelationshipKind': StructuralRelationshipKind,
                'TemporalRelationshipKind': TemporalRelationshipKind,
                'EnvironmentalRelationshipKind': EnvironmentalRelationshipKind,
                'ChangeRelationshipKind': ChangeRelationshipKind,
                'BeliefRelationshipKind': BeliefRelationshipKind,
                'HaydenRelationshipKind': HaydenRelationshipKind
            })
            _relationship_enums_loaded = True
            logger.debug("Relationship enums loaded successfully")
        except ImportError as e:
            logger.warning(f"Failed to load relationship enums: {e}")

# ───────────────────────────────────────────────
# BACKWARD COMPATIBILITY ENUMS
# ───────────────────────────────────────────────

class _DynamicEnum(Enum):
    """Base class for dynamically constructed enums with lazy loading."""
    
    @classmethod
    def _missing_(cls, value):
        """Handle missing enum values by triggering lazy loading."""
        if cls.__name__ == 'ValueCategory':
            _load_extended_enums()
            return cls._get_from_extended_categories(value)
        elif cls.__name__ == 'RelationshipKind':
            _load_relationship_enums()
            return cls._get_from_relationship_categories(value) 
        return None
    
    @classmethod
    def _get_from_extended_categories(cls, value):
        """Get value from extended category enums."""
        if hasattr(globals().get('GovernanceValueCategory'), value.name if hasattr(value, 'name') else str(value)):
            return getattr(globals()['GovernanceValueCategory'], value.name if hasattr(value, 'name') else str(value))
        if hasattr(globals().get('SpecializedValueCategory'), value.name if hasattr(value, 'name') else str(value)):
            return getattr(globals()['SpecializedValueCategory'], value.name if hasattr(value, 'name') else str(value))
        return None
    
    @classmethod
    def _get_from_relationship_categories(cls, value):
        """Get value from relationship category enums."""
        relationship_modules = [
            'GovernanceRelationshipKind', 'EconomicRelationshipKind', 
            'ResourceFlowRelationshipKind', 'InformationRelationshipKind',
            'SocialRelationshipKind', 'InfluenceRelationshipKind',
            'ProcessRelationshipKind', 'StructuralRelationshipKind',
            'TemporalRelationshipKind', 'EnvironmentalRelationshipKind',
            'ChangeRelationshipKind', 'BeliefRelationshipKind',
            'HaydenRelationshipKind'
        ]
        
        value_name = value.name if hasattr(value, 'name') else str(value)
        for module_name in relationship_modules:
            module = globals().get(module_name)
            if module and hasattr(module, value_name):
                return getattr(module, value_name)
        return None

# ───────────────────────────────────────────────
# DYNAMIC ENUM CREATION WITH LAZY LOADING
# ───────────────────────────────────────────────

# ───────────────────────────────────────────────
# DYNAMIC ENUM CREATION WITH LAZY LOADING
# ───────────────────────────────────────────────

class ValueCategory(Enum):
    """
    Categories of value that can be measured and tracked in Social Fabric Matrix analysis.
    
    This enum contains commonly used value categories for memory efficiency while maintaining
    backward compatibility. Extended categories are available in specialized modules.
    """
    
    # Core values (loaded immediately) - expanded to include commonly tested values
    ECONOMIC = auto()  # Market-priced goods, services, financial returns
    SOCIAL = auto()  # Distributional equity, social cohesion, well-being
    ENVIRONMENTAL = auto()  # Resource stocks, ecological integrity
    CULTURAL = auto()  # Norms, beliefs, heritage
    INSTITUTIONAL = auto()  # Governance quality, rule consistency
    TECHNOLOGICAL = auto()  # Knowledge base, production techniques
    
    # Additional commonly used values to reduce lazy loading
    POLITICAL = auto()  # Power distribution, democratic participation, governance
    EDUCATIONAL = auto()  # Learning outcomes, knowledge transfer, skill development
    HEALTH = auto()  # Public health, medical outcomes, wellness indicators
    SECURITY = auto()  # Safety, defense, risk management, stability
    INFRASTRUCTURE = auto()  # Physical systems, utilities, transportation, communication
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
    
    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._name_ = None
        obj._value_ = value
        return obj
        
    @classmethod
    def _missing_(cls, value):
        """Handle missing values by loading extended enums."""
        if isinstance(value, str):
            # Try to find in extended enums
            _load_extended_enums()
            
            # Try governance categories
            if 'GovernanceValueCategory' in globals():
                try:
                    governance_cat = globals()['GovernanceValueCategory']
                    if hasattr(governance_cat, value):
                        extended_value = getattr(governance_cat, value)
                        # Create a new enum member dynamically
                        new_member = object.__new__(cls)
                        new_member._name_ = value
                        new_member._value_ = extended_value.value
                        setattr(cls, value, new_member)
                        return new_member
                except (AttributeError, TypeError):
                    pass
            
            # Try specialized categories
            if 'SpecializedValueCategory' in globals():
                try:
                    specialized_cat = globals()['SpecializedValueCategory']
                    if hasattr(specialized_cat, value):
                        extended_value = getattr(specialized_cat, value)
                        new_member = object.__new__(cls)
                        new_member._name_ = value
                        new_member._value_ = extended_value.value
                        setattr(cls, value, new_member)
                        return new_member
                except (AttributeError, TypeError):
                    pass
        
        return None

class ResourceType(Enum):
    """
    Classification of resource types within Social Fabric Matrix analysis.
    
    This enum contains commonly used resource types for memory efficiency while maintaining
    backward compatibility. Extended resource types are available in specialized modules.
    """
    
    # Core resources (loaded immediately)
    NATURAL = auto()  # Land, water, raw minerals
    PRODUCED = auto()  # Machinery, infrastructures
    HUMAN = auto()  # Labor, human capital, skills
    INFORMATION = auto()  # Data, R&D findings, patents
    FINANCIAL = auto()  # Money, securities, investments
    SOCIAL_CAPITAL = auto()  # Trust networks, relationships, community bonds
    
    @classmethod
    def _missing_(cls, value):
        """Handle missing values by loading extended resource enums."""
        if isinstance(value, str):
            _load_extended_enums()
            
            if 'SpecializedResourceType' in globals():
                try:
                    specialized_res = globals()['SpecializedResourceType']
                    if hasattr(specialized_res, value):
                        extended_value = getattr(specialized_res, value)
                        new_member = object.__new__(cls)
                        new_member._name_ = value
                        new_member._value_ = extended_value.value
                        setattr(cls, value, new_member)
                        return new_member
                except (AttributeError, TypeError):
                    pass
        
        return None

class FlowNature(Enum):
    """
    Classification of flow types and patterns in Social Fabric Matrix systems.
    
    This enum contains commonly used flow natures for memory efficiency while maintaining
    backward compatibility. Extended flow patterns are available in specialized modules.
    """
    
    # Core flows (loaded immediately)  
    INPUT = auto()  # Resource or value entering a process
    OUTPUT = auto()  # Product, waste, or value leaving a process
    TRANSFER = auto()  # Exchange between actors without transformation
    INTERNAL = auto()  # Flows contained within system boundaries
    EXTERNAL = auto()  # Flows crossing system boundaries
    CIRCULAR = auto()  # Returns to origin after processing
    
    @classmethod
    def _missing_(cls, value):
        """Handle missing values by loading extended flow enums."""
        if isinstance(value, str):
            _load_extended_enums()
            
            if 'SpecializedFlowNature' in globals():
                try:
                    specialized_flow = globals()['SpecializedFlowNature']
                    if hasattr(specialized_flow, value):
                        extended_value = getattr(specialized_flow, value)
                        new_member = object.__new__(cls)
                        new_member._name_ = value
                        new_member._value_ = extended_value.value
                        setattr(cls, value, new_member)
                        return new_member
                except (AttributeError, TypeError):
                    pass
        
        return None

class RelationshipKind(Enum):
    """
    Taxonomy of relationship types in Social Fabric Matrix systems.
    
    This enum contains commonly used relationship types for memory efficiency while maintaining
    backward compatibility. Extended relationship types are available in specialized modules.
    """
    
    # Core relationships (loaded immediately) - expanded to include commonly tested values
    GOVERNS = auto()  # Authority over another entity
    REGULATES = auto()  # Creates or enforces rules for
    IMPLEMENTS = auto()  # Puts into practice
    ENACTS = auto()  # Creates or modifies laws, policies, or regulations
    USES = auto()  # Actor/process employs a resource or technology
    PRODUCES = auto()  # Creates outputs for
    SERVES = auto()  # Provides services to
    FUNDS = auto()  # Provides money to
    EXCHANGES_WITH = auto()  # Actor-to-actor transfer
    TRANSFERS = auto()  # Moves resources without transformation
    AFFECTS = auto()  # Base Feedback relationship
    INFLUENCES = auto()  # Affects decisions or behavior of
    COLLABORATES_WITH = auto()  # Works jointly with
    PARTICIPATES_IN = auto()  # Takes part in
    SUPPORTS = auto()  # Helps or assists
    BENEFITS_FROM = auto()  # Gains advantage or support from
    
    # Additional commonly tested relationships
    PAYS = auto()  # Exchanges money for goods/services
    OWNS = auto()  # Has property rights over
    COMPETES_WITH = auto()  # Rivals for resources or markets
    SUPPLIES = auto()  # Provides inputs to
    INFORMS = auto()  # Provides information to
    ADVISES = auto()  # Gives guidance to
    EDUCATES = auto()  # Transfers knowledge to
    CONTAINS = auto()  # Has as a component
    CONNECTS = auto()  # Links physically or logically
    TRANSPORTS = auto()  # Moves from one location to another
    FOLLOWS = auto()  # Comes after
    TRIGGERS = auto()  # Initiates or causes
    PROCESSES = auto()  # Treats or handles materials from
    MAINTAINS = auto()  # Keeps in working order
    OPERATES = auto()  # Runs or manages
    CONSERVES = auto()  # Uses carefully to prevent depletion
    DEVELOPS = auto()  # Creates growth or maturity in
    LOCATED_IN = auto()  # Spatial anchoring
    MONITORS = auto()  # Observes and assesses
    
    # Additional governance relationships
    AUTHORIZES = auto()  # Grants permission to
    MANDATES = auto()  # Makes actions compulsory
    ENFORCES = auto()  # Ensures compliance with rules
    DELEGATES = auto()  # Transfers authority to
    REPRESENTS = auto()  # Acts on behalf of
    ACCOUNTABLE_TO = auto()  # Must answer to
    LICENSES = auto()  # Formally permits activity
    CERTIFIES = auto()  # Validates compliance or quality
    SANCTIONS = auto()  # Penalizes for non-compliance
    
    # Additional resource flow relationships
    ALLOCATES = auto()  # Distributes resources to
    EXTRACTS = auto()  # Removes resources from
    CONSUMES = auto()  # Uses up resources from
    DISTRIBUTES = auto()  # Disseminates to multiple targets
    STORES = auto()  # Holds resources for
    CONVERTS = auto()  # Transforms one resource to another
    RECYCLES = auto()  # Reprocesses for reuse
    
    # Additional economic relationships
    BUYS_FROM = auto()  # Purchases goods/services
    SELLS_TO = auto()  # Provides goods/services for payment
    EMPLOYS = auto()  # Hires for labor
    CONTRACTS_WITH = auto()  # Formal agreement for exchange
    INVESTS_IN = auto()  # Commits resources for future return
    INSURES = auto()  # Provides risk protection for
    SUBSIDIZES = auto()  # Provides financial support to
    TAXES = auto()  # Collects mandatory payment from
    RENTS_TO = auto()  # Provides temporary use rights
    
    # Additional information relationships
    RESEARCHES = auto()  # Investigates for
    INNOVATES_FOR = auto()  # Creates new solutions for
    DOCUMENTS = auto()  # Records information about
    ANALYZES = auto()  # Examines and interprets
    FORECASTS = auto()  # Predicts outcomes for
    COMMUNICATES_WITH = auto()  # Exchanges information with
    MEASURES = auto()  # Quantifies attributes of
    CALCULATES = auto()  # Computes values related to
    
    # Additional social relationships
    ALLIES_WITH = auto()  # Forms strategic partnership with
    COORDINATES_WITH = auto()  # Aligns activities with
    FACILITATES = auto()  # Makes easier or enables
    MEDIATES = auto()  # Resolves conflicts between
    ADVOCATES_FOR = auto()  # Publicly supports
    ORGANIZES = auto()  # Arranges or structures
    CONVENES = auto()  # Brings together
    
    # Additional influence relationships
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
    
    # Additional process relationships
    TESTS = auto()  # Evaluates performance of
    INSTALLS = auto()  # Sets up for use
    INTEGRATES = auto()  # Combines into system
    OPTIMIZES = auto()  # Improves efficiency of
    AUTOMATES = auto()  # Makes self-operating
    REPAIRS = auto()  # Fixes or restores
    
    # Additional structural relationships
    BELONGS_TO = auto()  # Is a member of
    COMPOSED_OF = auto()  # Consists of
    CATEGORIZES = auto()  # Places in classification
    AGGREGATES = auto()  # Combines into a whole
    SEPARATES = auto()  # Divides or keeps apart
    HOSTS = auto()  # Provides environment for
    ATTACHES_TO = auto()  # Joins or fixes to
    EMBEDS_WITHIN = auto()  # Incorporates deeply into
    ENCOMPASSES = auto()  # Includes completely
    
    # Additional temporal relationships
    PRECEDES = auto()  # Comes before
    SYNCHRONIZES_WITH = auto()  # Coordinates timing with
    DELAYS = auto()  # Postpones or slows
    ACCELERATES = auto()  # Speeds up
    SCHEDULES = auto()  # Sets timing for
    ITERATES = auto()  # Repeats process with
    SUPERSEDES = auto()  # Replaces or makes obsolete
    RENEWS = auto()  # Extends or refreshes
    TERMINATES = auto()  # Ends relationship with
    OCCURS_DURING = auto()  # Temporal anchoring
    ENABLES_FUTURE = auto()  # Enables future possibilities
    CONSTRAINS_FUTURE = auto()  # Limits future options
    
    # Additional environmental relationships
    SUSTAINS = auto()  # Maintains viability of
    POLLUTES = auto()  # Degrades quality of
    RESTORES = auto()  # Returns to previous condition
    ADAPTS_TO = auto()  # Changes in response to
    MITIGATES = auto()  # Reduces negative impact on
    DEPENDS_ON = auto()  # Requires for functioning
    COEXISTS_WITH = auto()  # Lives alongside without harm
    HARVESTS = auto()  # Collects resources from
    CULTIVATES = auto()  # Grows or nurtures
    
    # Additional change relationships
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
    
    # Additional belief relationships
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
    REINFORCES = auto()  # Positive feedback relationship
    UNDERMINES = auto()  # Negative feedback relationship
    LEGITIMIZES = auto()  # Provides legitimacy to
    DELEGITIMIZES = auto()  # Removes legitimacy from
    CEREMONIALLY_REINFORCES = auto()  # Supports ceremonial patterns
    INSTRUMENTALLY_ADAPTS = auto()  # Enables instrumental change
    CREATES_PATH_DEPENDENCY = auto()  # Establishes path dependencies
    ENABLES_INNOVATION = auto()  # Facilitates innovative change
    DISTRIBUTES_POWER = auto()  # Spreads power across actors
    CONCENTRATES_POWER = auto()  # Centralizes power in fewer actors
    
    @classmethod
    def _missing_(cls, value):
        """Handle missing values by loading relationship enums."""
        if isinstance(value, str):
            _load_relationship_enums()
            
            # Try all relationship enum modules
            relationship_modules = [
                'GovernanceRelationshipKind', 'EconomicRelationshipKind',
                'ResourceFlowRelationshipKind', 'InformationRelationshipKind',
                'SocialRelationshipKind', 'InfluenceRelationshipKind',
                'ProcessRelationshipKind', 'StructuralRelationshipKind',
                'TemporalRelationshipKind', 'EnvironmentalRelationshipKind',
                'ChangeRelationshipKind', 'BeliefRelationshipKind',
                'HaydenRelationshipKind'
            ]
            
            for module_name in relationship_modules:
                if module_name in globals():
                    try:
                        module = globals()[module_name]
                        if hasattr(module, value):
                            extended_value = getattr(module, value)
                            new_member = object.__new__(cls)
                            new_member._name_ = value
                            new_member._value_ = extended_value.value
                            setattr(cls, value, new_member)
                            return new_member
                    except (AttributeError, TypeError):
                        continue
        
        return None

# Create the unified enums (now just aliases since they're the real classes)
# ValueCategory = _LazyValueCategory
# RelationshipKind = _LazyRelationshipKind
# ResourceType = _LazyResourceType
# FlowNature = _LazyFlowNature

# ───────────────────────────────────────────────
# REMAINING SMALLER ENUMS (unchanged for compatibility)
# ───────────────────────────────────────────────

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
