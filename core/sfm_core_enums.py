"""
Core enumerations for the Social Fabric Matrix (SFM) framework.

This module contains the most commonly used enum values for memory-efficient
imports and operations. These core enums contain the subset of values that
are used in 90%+ of SFM operations.
"""

from __future__ import annotations
from enum import Enum, auto


class CoreValueCategory(Enum):
    """
    Core value categories used in most SFM analysis.
    
    Contains the essential value dimensions that are used in the majority
    of SFM operations, reducing memory overhead for common use cases.
    """
    ECONOMIC = auto()  # Market-priced goods, services, financial returns
    SOCIAL = auto()  # Distributional equity, social cohesion, well-being
    ENVIRONMENTAL = auto()  # Resource stocks, ecological integrity
    CULTURAL = auto()  # Norms, beliefs, heritage
    INSTITUTIONAL = auto()  # Governance quality, rule consistency
    TECHNOLOGICAL = auto()  # Knowledge base, production techniques


class CoreRelationshipKind(Enum):
    """
    Core relationship types used in most SFM analysis.
    
    Contains the most frequently used relationship kinds that appear
    in typical SFM models and analyses.
    """
    # Governance relationships (most common)
    GOVERNS = auto()  # Authority over another entity
    REGULATES = auto()  # Creates or enforces rules for
    IMPLEMENTS = auto()  # Puts into practice
    ENACTS = auto()  # Creates or modifies laws, policies, or regulations
    
    # Resource and economic relationships  
    USES = auto()  # Actor/process employs a resource or technology
    PRODUCES = auto()  # Creates outputs for
    SERVES = auto()  # Provides services to
    FUNDS = auto()  # Provides money to
    EXCHANGES_WITH = auto()  # Actor-to-actor transfer
    TRANSFERS = auto()  # Moves resources without transformation
    
    # Influence and process relationships
    AFFECTS = auto()  # Base Feedback relationship
    INFLUENCES = auto()  # Affects decisions or behavior of
    COLLABORATES_WITH = auto()  # Works jointly with
    PARTICIPATES_IN = auto()  # Takes part in
    SUPPORTS = auto()  # Helps or assists
    BENEFITS_FROM = auto()  # Gains advantage or support from


class CoreResourceType(Enum):
    """
    Core resource types used in most SFM analysis.
    
    Contains the fundamental resource categories that appear in
    typical SFM models and resource flow analyses.
    """
    NATURAL = auto()  # Land, water, raw minerals
    PRODUCED = auto()  # Machinery, infrastructures
    HUMAN = auto()  # Labor, human capital, skills
    INFORMATION = auto()  # Data, R&D findings, patents
    FINANCIAL = auto()  # Money, securities, investments
    SOCIAL_CAPITAL = auto()  # Trust networks, relationships, community bonds


class CoreFlowNature(Enum):
    """
    Core flow natures used in most SFM analysis.
    
    Contains the essential flow types that describe the fundamental
    ways resources and values move through SFM systems.
    """
    INPUT = auto()  # Resource or value entering a process
    OUTPUT = auto()  # Product, waste, or value leaving a process
    TRANSFER = auto()  # Exchange between actors without transformation
    
    # Additional common flow patterns
    INTERNAL = auto()  # Flows contained within system boundaries
    EXTERNAL = auto()  # Flows crossing system boundaries
    CIRCULAR = auto()  # Returns to origin after processing