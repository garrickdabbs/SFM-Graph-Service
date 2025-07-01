#!/usr/bin/env python3
"""
Demonstration script showing the new enum functionality for SFM models.

This script demonstrates that string-based fields have been successfully
converted to use proper enums for type safety and consistency.
"""

from core.sfm_models import (
    Flow, PolicyInstrument, ChangeProcess, BehavioralPattern,
    FeedbackLoop, TemporalDynamics, ValidationRule, SystemProperty,
    TimeSlice
)
from core.sfm_enums import (
    FlowType, PolicyInstrumentType, ChangeType, BehaviorPatternType,
    FeedbackPolarity, FeedbackType, TemporalFunctionType,
    ValidationRuleType, SystemPropertyType
)

def demonstrate_enum_usage():
    """Demonstrate the new enum usage in SFM models."""
    
    print("=== SFM Enum Demonstration ===\n")
    
    # 1. Flow with FlowType enum
    flow = Flow(
        label="Material Flow Example",
        flow_type=FlowType.MATERIAL,
        quantity=100.0,
        unit="kg"
    )
    print(f"1. Flow: {flow.label}")
    print(f"   Type: {flow.flow_type} (enum value)")
    print(f"   String representation: {str(flow.flow_type)}\n")
    
    # 2. PolicyInstrument with PolicyInstrumentType enum
    policy_instrument = PolicyInstrument(
        label="Carbon Tax Policy",
        instrument_type=PolicyInstrumentType.ECONOMIC,
        target_behavior="reduce emissions",
        effectiveness_measure=0.8
    )
    print(f"2. PolicyInstrument: {policy_instrument.label}")
    print(f"   Type: {policy_instrument.instrument_type} (enum value)")
    print(f"   Target: {policy_instrument.target_behavior}\n")
    
    # 3. ChangeProcess with ChangeType enum
    change_process = ChangeProcess(
        label="Digital Transformation",
        change_type=ChangeType.REVOLUTIONARY,
        success_probability=0.7
    )
    print(f"3. ChangeProcess: {change_process.label}")
    print(f"   Type: {change_process.change_type} (enum value)")
    print(f"   Success probability: {change_process.success_probability}\n")
    
    # 4. BehavioralPattern with BehaviorPatternType enum
    behavioral_pattern = BehavioralPattern(
        label="Adaptive Learning",
        pattern_type=BehaviorPatternType.ADAPTIVE,
        frequency=0.9,
        predictability=0.6
    )
    print(f"4. BehavioralPattern: {behavioral_pattern.label}")
    print(f"   Type: {behavioral_pattern.pattern_type} (enum value)")
    print(f"   Frequency: {behavioral_pattern.frequency}\n")
    
    # 5. FeedbackLoop with enum types
    feedback_loop = FeedbackLoop(
        label="Economic Growth Loop",
        polarity=FeedbackPolarity.REINFORCING,
        type=FeedbackType.POSITIVE,
        strength=0.8
    )
    print(f"5. FeedbackLoop: {feedback_loop.label}")
    print(f"   Polarity: {feedback_loop.polarity} (enum value)")
    print(f"   Type: {feedback_loop.type} (enum value)")
    print(f"   Strength: {feedback_loop.strength}\n")
    
    # 6. TemporalDynamics with TemporalFunctionType enum
    temporal_dynamics = TemporalDynamics(
        start_time=TimeSlice(label="2024"),
        function_type=TemporalFunctionType.EXPONENTIAL,
        parameters={"growth_rate": 0.05}
    )
    print(f"6. TemporalDynamics: {temporal_dynamics.start_time.label}")
    print(f"   Function type: {temporal_dynamics.function_type} (enum value)")
    print(f"   Parameters: {temporal_dynamics.parameters}\n")
    
    # 7. ValidationRule with ValidationRuleType enum
    validation_rule = ValidationRule(
        rule_type=ValidationRuleType.RANGE,
        target_field="effectiveness",
        parameters={"min": 0.0, "max": 1.0},
        error_message="Effectiveness must be between 0 and 1"
    )
    print(f"7. ValidationRule: {validation_rule.target_field}")
    print(f"   Rule type: {validation_rule.rule_type} (enum value)")
    print(f"   Parameters: {validation_rule.parameters}\n")
    
    # 8. SystemProperty with SystemPropertyType enum
    system_property = SystemProperty(
        label="Network Density",
        property_type=SystemPropertyType.STRUCTURAL,
        value=0.65,
        unit="ratio"
    )
    print(f"8. SystemProperty: {system_property.label}")
    print(f"   Property type: {system_property.property_type} (enum value)")
    print(f"   Value: {system_property.value} {system_property.unit}\n")
    
    # Demonstrate type safety
    print("=== Type Safety Demonstration ===")
    print("All enum values provide type safety:")
    print(f"- FlowType options: {[e.name for e in FlowType]}")
    print(f"- PolicyInstrumentType options: {[e.name for e in PolicyInstrumentType]}")
    print(f"- ChangeType options: {[e.name for e in ChangeType]}")
    print(f"- BehaviorPatternType options: {[e.name for e in BehaviorPatternType]}")
    print(f"- FeedbackPolarity options: {[e.name for e in FeedbackPolarity]}")
    print(f"- FeedbackType options: {[e.name for e in FeedbackType]}")
    print(f"- TemporalFunctionType options: {[e.name for e in TemporalFunctionType]}")
    print(f"- ValidationRuleType options: {[e.name for e in ValidationRuleType]}")
    print(f"- SystemPropertyType options: {[e.name for e in SystemPropertyType]}")

if __name__ == "__main__":
    demonstrate_enum_usage()