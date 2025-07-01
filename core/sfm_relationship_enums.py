"""
Extended relationship enumerations for specialized SFM framework analysis.

This module contains relationship types for specialized use cases that
are not needed in typical SFM operations. These enums are loaded on-demand
to minimize memory usage for common operations.
"""

from __future__ import annotations
from enum import Enum, auto


class GovernanceRelationshipKind(Enum):
    """Governance and authority relationships for institutional analysis."""
    # Authority and regulation
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


class EconomicRelationshipKind(Enum):
    """Economic and market relationships for financial analysis."""
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


class ResourceFlowRelationshipKind(Enum):
    """Resource flow relationships for material and energy analysis."""
    # Resource Flow Relationships
    PAYS = auto()  # Exchanges money for goods/services
    ALLOCATES = auto()  # Distributes resources to
    EXTRACTS = auto()  # Removes resources from
    CONSUMES = auto()  # Uses up resources from
    DISTRIBUTES = auto()  # Disseminates to multiple targets
    STORES = auto()  # Holds resources for
    CONVERTS = auto()  # Transforms one resource to another
    RECYCLES = auto()  # Reprocesses for reuse


class InformationRelationshipKind(Enum):
    """Knowledge and information relationships for data flow analysis."""
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


class SocialRelationshipKind(Enum):
    """Social and collaborative relationships for network analysis."""
    # Social and Collaborative Relationships
    ALLIES_WITH = auto()  # Forms strategic partnership with
    COORDINATES_WITH = auto()  # Aligns activities with
    FACILITATES = auto()  # Makes easier or enables
    MEDIATES = auto()  # Resolves conflicts between
    ADVOCATES_FOR = auto()  # Publicly supports
    ORGANIZES = auto()  # Arranges or structures
    CONVENES = auto()  # Brings together


class InfluenceRelationshipKind(Enum):
    """Influence and impact relationships for power analysis."""
    # Influence and Impact Relationships
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


class ProcessRelationshipKind(Enum):
    """Process and operational relationships for workflow analysis."""
    # Process and Operational Relationships
    OPERATES = auto()  # Runs or manages
    MAINTAINS = auto()  # Keeps in working order
    TESTS = auto()  # Evaluates performance of
    INSTALLS = auto()  # Sets up for use
    TRANSPORTS = auto()  # Moves from one location to another
    INTEGRATES = auto()  # Combines into system
    OPTIMIZES = auto()  # Improves efficiency of
    AUTOMATES = auto()  # Makes self-operating
    REPAIRS = auto()  # Fixes or restores


class StructuralRelationshipKind(Enum):
    """Structural and containment relationships for system architecture."""
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


class TemporalRelationshipKind(Enum):
    """Temporal and sequential relationships for time-based analysis."""
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
    ENABLES_FUTURE = auto()  # Enables future possibilities
    CONSTRAINS_FUTURE = auto()  # Limits future options


class EnvironmentalRelationshipKind(Enum):
    """Environmental and ecological relationships for sustainability analysis."""
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


class ChangeRelationshipKind(Enum):
    """Development and change relationships for transformation analysis."""
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


class BeliefRelationshipKind(Enum):
    """Belief and value relationships for cultural analysis."""
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


class HaydenRelationshipKind(Enum):
    """Hayden-specific relationships for institutional economics analysis."""
    # Hayden-specific relationships for institutional analysis
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