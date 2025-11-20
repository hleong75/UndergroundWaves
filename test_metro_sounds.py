#!/usr/bin/env python3
"""
Test script for Metro Sound Simulator
Validates sound generation functions without requiring audio playback.
"""

import numpy as np
import sys
from metro_sounds import MetroSoundSimulator


def test_initialization():
    """Test that the simulator initializes correctly."""
    print("Testing initialization...")
    simulator = MetroSoundSimulator(sample_rate=44100)
    assert simulator.sample_rate == 44100
    assert simulator.is_running == False
    print("  ✓ Initialization test passed")


def test_generate_tone():
    """Test tone generation."""
    print("Testing tone generation...")
    simulator = MetroSoundSimulator()
    
    # Generate a 1-second 440 Hz tone
    tone = simulator.generate_tone(440, 1.0, 0.5)
    
    # Check that we got the right number of samples
    expected_samples = 44100
    assert len(tone) == expected_samples, f"Expected {expected_samples} samples, got {len(tone)}"
    
    # Check that values are in reasonable range
    assert np.max(tone) <= 0.5, "Tone amplitude too high"
    assert np.min(tone) >= -0.5, "Tone amplitude too low"
    
    print("  ✓ Tone generation test passed")


def test_generate_noise():
    """Test noise generation."""
    print("Testing noise generation...")
    simulator = MetroSoundSimulator()
    
    # Generate 2 seconds of noise
    noise = simulator.generate_noise(2.0, 0.1, 50, 200)
    
    # Check that we got the right number of samples
    expected_samples = 88200
    assert len(noise) == expected_samples, f"Expected {expected_samples} samples, got {len(noise)}"
    
    # Check that it's not silent
    assert np.std(noise) > 0, "Noise should not be silent"
    
    print("  ✓ Noise generation test passed")


def test_generate_sweep():
    """Test frequency sweep generation."""
    print("Testing frequency sweep generation...")
    simulator = MetroSoundSimulator()
    
    # Generate a 1.5-second sweep from 500 to 1000 Hz
    sweep = simulator.generate_sweep(500, 1000, 1.5, 0.3)
    
    # Check that we got the right number of samples
    expected_samples = int(44100 * 1.5)
    assert len(sweep) == expected_samples, f"Expected {expected_samples} samples, got {len(sweep)}"
    
    # Check that amplitude envelope is applied (should start and end near 0)
    assert abs(sweep[0]) < 0.01, "Sweep should start near 0 (fade-in)"
    assert abs(sweep[-1]) < 0.01, "Sweep should end near 0 (fade-out)"
    
    # Check middle has signal
    middle = len(sweep) // 2
    assert abs(sweep[middle]) > 0.05, "Sweep should have signal in the middle"
    
    print("  ✓ Frequency sweep generation test passed")


def test_audio_generation_non_empty():
    """Test that various sound generation methods produce non-empty results."""
    print("Testing all audio generation methods...")
    simulator = MetroSoundSimulator()
    
    # Test each sound generation method
    tests = [
        ("tone", lambda: simulator.generate_tone(440, 0.5)),
        ("noise", lambda: simulator.generate_noise(0.5)),
        ("sweep", lambda: simulator.generate_sweep(500, 1000, 0.5)),
    ]
    
    for name, func in tests:
        result = func()
        assert len(result) > 0, f"{name} should produce audio samples"
        assert isinstance(result, np.ndarray), f"{name} should return numpy array"
        print(f"  ✓ {name} generation works")
    
    print("  ✓ All audio generation methods test passed")


def test_sample_rate_variations():
    """Test that different sample rates work correctly."""
    print("Testing different sample rates...")
    
    for sample_rate in [22050, 44100, 48000]:
        simulator = MetroSoundSimulator(sample_rate=sample_rate)
        tone = simulator.generate_tone(440, 1.0)
        expected = sample_rate  # 1 second
        assert len(tone) == expected, f"Sample rate {sample_rate}: expected {expected} samples, got {len(tone)}"
    
    print("  ✓ Sample rate variations test passed")


def test_amplitude_bounds():
    """Test that amplitudes are properly bounded."""
    print("Testing amplitude bounds...")
    simulator = MetroSoundSimulator()
    
    # Test with various amplitudes
    for amp in [0.1, 0.3, 0.5, 0.9]:
        tone = simulator.generate_tone(440, 0.5, amplitude=amp)
        max_val = np.max(np.abs(tone))
        assert max_val <= amp + 0.01, f"Amplitude {amp}: max value {max_val} exceeds expected"
    
    print("  ✓ Amplitude bounds test passed")


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("🧪 METRO SOUND SIMULATOR - TEST SUITE")
    print("="*60 + "\n")
    
    tests = [
        test_initialization,
        test_generate_tone,
        test_generate_noise,
        test_generate_sweep,
        test_audio_generation_non_empty,
        test_sample_rate_variations,
        test_amplitude_bounds,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
