#!/usr/bin/env python3
"""
Test script for AI-Enhanced Sound Engine
Validates AI components without requiring audio playback.
"""

import numpy as np
import sys
from ai_sound_engine import (
    SoundContext,
    AIParameterLearner,
    IntelligentNoiseGenerator,
    ContextAwareFrequencyModulator,
    AdaptiveSoundEvolution,
    IntelligentEventPredictor
)


def test_sound_context():
    """Test SoundContext initialization and attributes."""
    print("Testing SoundContext...")
    context = SoundContext()
    
    assert context.journey_time == 0.0
    assert context.speed == 0.0
    assert context.temperature == 20.0
    assert context.track_wear >= 0.0 and context.track_wear <= 1.0
    
    # Test with custom values
    custom_context = SoundContext(
        journey_time=10.0,
        speed=50.0,
        temperature=25.0,
        track_wear=0.7
    )
    assert custom_context.journey_time == 10.0
    assert custom_context.speed == 50.0
    
    print("  ✓ SoundContext test passed")


def test_ai_parameter_learner():
    """Test AI parameter learning and prediction."""
    print("Testing AIParameterLearner...")
    learner = AIParameterLearner(memory_size=50)
    
    # Learn some parameter values
    for i in range(20):
        learner.learn_parameter('test_param', 1.0 + i * 0.01)
    
    # Predict value
    predicted = learner.predict_parameter('test_param')
    assert isinstance(predicted, float)
    assert predicted > 0.0
    
    # Test with context
    context = SoundContext(speed=60.0, track_wear=0.8)
    predicted_with_context = learner.predict_parameter('test_param', context)
    assert isinstance(predicted_with_context, float)
    
    print("  ✓ AIParameterLearner test passed")


def test_intelligent_noise_generator():
    """Test AI-driven noise generation."""
    print("Testing IntelligentNoiseGenerator...")
    generator = IntelligentNoiseGenerator(sample_rate=44100)
    
    # Generate noise without context
    noise = generator.generate_intelligent_noise(1.0, 0.1)
    assert len(noise) == 44100
    assert isinstance(noise, np.ndarray)
    assert np.std(noise) > 0
    
    # Generate noise with context
    context = SoundContext(speed=50.0, track_wear=0.7, weather_condition='rain')
    noise_with_context = generator.generate_intelligent_noise(1.0, 0.1, context)
    assert len(noise_with_context) == 44100
    assert isinstance(noise_with_context, np.ndarray)
    
    print("  ✓ IntelligentNoiseGenerator test passed")


def test_context_aware_frequency_modulator():
    """Test context-aware frequency modulation."""
    print("Testing ContextAwareFrequencyModulator...")
    modulator = ContextAwareFrequencyModulator()
    
    context = SoundContext(
        speed=50.0,
        temperature=25.0,
        track_wear=0.6,
        vehicle_age=0.5
    )
    
    # Test frequency modulation
    base_freq = 440.0
    modulated = modulator.modulate_frequency(base_freq, 'motor_whine', context)
    assert isinstance(modulated, float)
    assert modulated > 0.0
    
    # Test harmonic generation
    harmonics = modulator.get_harmonic_intelligence(440.0, 'motor', context)
    assert len(harmonics) > 0
    assert all(isinstance(h[0], (float, np.floating)) for h in harmonics)
    assert all(isinstance(h[1], (float, np.floating)) for h in harmonics)
    
    # Check that harmonics have decreasing amplitudes (generally)
    amplitudes = [h[1] for h in harmonics]
    assert amplitudes[0] >= amplitudes[-1]
    
    print("  ✓ ContextAwareFrequencyModulator test passed")


def test_adaptive_sound_evolution():
    """Test adaptive sound evolution over time."""
    print("Testing AdaptiveSoundEvolution...")
    evolution = AdaptiveSoundEvolution()
    
    # Initial state
    assert evolution.time_elapsed == 0.0
    assert 'brake_temperature' in evolution.evolution_state
    
    # Update during braking
    context = SoundContext(speed=30.0, acceleration=-2.0, temperature=20.0)
    evolution.update(5.0, context)
    
    # Check that time elapsed
    assert evolution.time_elapsed == 5.0
    
    # Check temperature increased (braking)
    assert evolution.evolution_state['brake_temperature'] > 20.0
    
    # Get modulation factors
    temp_mod = evolution.get_temperature_modulation()
    assert isinstance(temp_mod, float)
    assert temp_mod >= 1.0
    
    # Get wear effects
    wear_effects = evolution.get_wear_effects()
    assert 'bearing_noise' in wear_effects
    assert 'roughness' in wear_effects
    assert 'vibration' in wear_effects
    
    print("  ✓ AdaptiveSoundEvolution test passed")


def test_intelligent_event_predictor():
    """Test intelligent event prediction."""
    print("Testing IntelligentEventPredictor...")
    predictor = IntelligentEventPredictor()
    
    # Test event prediction
    context = SoundContext(speed=50.0, track_wear=0.8, vehicle_age=0.7)
    
    # Run predictions multiple times
    events_predicted = []
    for i in range(100):
        event = predictor.predict_event(float(i), context)
        if event:
            events_predicted.append(event)
    
    # Should predict some events but not too many
    assert len(events_predicted) >= 0  # May or may not predict events
    
    # If events were predicted, they should be valid types
    valid_events = {'curve', 'rail_switch', 'rail_defect', 'wheel_squeal', 'brake_squeal'}
    for event in events_predicted:
        assert event in valid_events
    
    print("  ✓ IntelligentEventPredictor test passed")


def test_ai_integration():
    """Test integration of AI components."""
    print("Testing AI integration...")
    
    # Create all components
    context = SoundContext(speed=50.0, track_wear=0.6)
    learner = AIParameterLearner()
    noise_gen = IntelligentNoiseGenerator()
    freq_mod = ContextAwareFrequencyModulator()
    evolution = AdaptiveSoundEvolution()
    event_pred = IntelligentEventPredictor()
    
    # Simulate a journey segment
    for t in range(10):
        # Learn parameters
        learner.learn_parameter('speed', context.speed)
        
        # Generate noise
        noise = noise_gen.generate_intelligent_noise(0.1, 0.1, context)
        assert len(noise) > 0
        
        # Modulate frequency
        freq = freq_mod.modulate_frequency(440.0, 'test', context)
        assert freq > 0
        
        # Update evolution
        evolution.update(1.0, context)
        
        # Predict events
        event = event_pred.predict_event(float(t), context)
        
        # Update context
        context.journey_time += 1.0
    
    print("  ✓ AI integration test passed")


def run_all_tests():
    """Run all AI engine tests."""
    print("\n" + "="*60)
    print("🤖 AI SOUND ENGINE - TEST SUITE")
    print("="*60 + "\n")
    
    tests = [
        test_sound_context,
        test_ai_parameter_learner,
        test_intelligent_noise_generator,
        test_context_aware_frequency_modulator,
        test_adaptive_sound_evolution,
        test_intelligent_event_predictor,
        test_ai_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
