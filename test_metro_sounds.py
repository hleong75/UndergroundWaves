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


def test_compressed_air_generation():
    """Test compressed air sound generation."""
    print("Testing compressed air generation...")
    simulator = MetroSoundSimulator()
    
    # Test compressed air release
    air_sound = simulator.generate_compressed_air_release(1.0, amplitude=0.25)
    
    # Check correct duration
    expected_samples = 44100
    assert len(air_sound) == expected_samples, f"Expected {expected_samples} samples, got {len(air_sound)}"
    
    # Check that amplitude decays (later samples should be smaller on average)
    first_half = np.mean(np.abs(air_sound[:len(air_sound)//2]))
    second_half = np.mean(np.abs(air_sound[len(air_sound)//2:]))
    assert first_half > second_half, "Compressed air should decay over time"
    
    print("  ✓ Compressed air generation test passed")


def test_electric_motor_generation():
    """Test electric motor sound generation."""
    print("Testing electric motor generation...")
    simulator = MetroSoundSimulator()
    
    # Test electric motor whine
    motor_sound = simulator.generate_electric_motor_whine(1.0, 300, 800, amplitude=0.15)
    
    # Check correct duration
    expected_samples = 44100
    assert len(motor_sound) == expected_samples, f"Expected {expected_samples} samples, got {len(motor_sound)}"
    
    # Check non-zero output
    assert np.max(np.abs(motor_sound)) > 0.01, "Motor sound should be audible"
    
    print("  ✓ Electric motor generation test passed")


def test_inverter_generation():
    """Test power inverter sound generation."""
    print("Testing inverter sound generation...")
    simulator = MetroSoundSimulator()
    
    # Test inverter sound
    inverter_sound = simulator.generate_inverter_sound(0.5, amplitude=0.1)
    
    # Check samples generated
    assert len(inverter_sound) > 0, "Inverter should produce audio samples"
    
    # Check it's not silent
    assert np.std(inverter_sound) > 0, "Inverter sound should not be silent"
    
    print("  ✓ Inverter generation test passed")


def test_wheel_flange_squeal_generation():
    """Test wheel flange squeal sound generation."""
    print("Testing wheel flange squeal generation...")
    simulator = MetroSoundSimulator()
    
    # Test flange squeal
    squeal_sound = simulator.generate_wheel_flange_squeal(1.5, amplitude=0.35)
    
    # Check correct duration
    expected_samples = int(44100 * 1.5)
    assert len(squeal_sound) == expected_samples, f"Expected {expected_samples} samples, got {len(squeal_sound)}"
    
    # Check non-zero output
    assert np.max(np.abs(squeal_sound)) > 0.01, "Flange squeal should be audible"
    
    # Check envelope (should fade in/out)
    assert abs(squeal_sound[0]) < 0.05, "Squeal should start near 0"
    assert abs(squeal_sound[-1]) < 0.05, "Squeal should end near 0"
    
    print("  ✓ Wheel flange squeal generation test passed")


def test_rail_joint_clicks_generation():
    """Test rail joint clicking sound generation."""
    print("Testing rail joint clicks generation...")
    simulator = MetroSoundSimulator()
    
    # Test rail joint clicks
    clicks_sound = simulator.generate_rail_joint_clicks(2.0, interval=0.8, amplitude=0.15)
    
    # Check correct duration
    expected_samples = int(44100 * 2.0)
    assert len(clicks_sound) == expected_samples, f"Expected {expected_samples} samples, got {len(clicks_sound)}"
    
    # Check it's not silent
    assert np.max(np.abs(clicks_sound)) > 0.01, "Rail clicks should be audible"
    
    print("  ✓ Rail joint clicks generation test passed")


def test_brake_squeal_generation():
    """Test brake squeal sound generation."""
    print("Testing brake squeal generation...")
    simulator = MetroSoundSimulator()
    
    # Test brake squeal
    squeal_sound = simulator.generate_brake_squeal(1.0, amplitude=0.25)
    
    # Check correct duration
    expected_samples = 44100
    assert len(squeal_sound) == expected_samples, f"Expected {expected_samples} samples, got {len(squeal_sound)}"
    
    # Check non-zero output
    assert np.max(np.abs(squeal_sound)) > 0.01, "Brake squeal should be audible"
    
    print("  ✓ Brake squeal generation test passed")


def test_low_speed_grinding_generation():
    """Test low-speed grinding sound generation."""
    print("Testing low-speed grinding generation...")
    simulator = MetroSoundSimulator()
    
    # Test low-speed grinding
    grind_sound = simulator.generate_low_speed_grinding(1.0, amplitude=0.18)
    
    # Check correct duration
    expected_samples = 44100
    assert len(grind_sound) == expected_samples, f"Expected {expected_samples} samples, got {len(grind_sound)}"
    
    # Check non-zero output
    assert np.max(np.abs(grind_sound)) > 0.01, "Grinding should be audible"
    
    print("  ✓ Low-speed grinding generation test passed")


def test_wheel_slip_generation():
    """Test wheel slip sound generation."""
    print("Testing wheel slip generation...")
    simulator = MetroSoundSimulator()
    
    # Test wheel slip
    slip_sound = simulator.generate_wheel_slip(0.5, amplitude=0.3)
    
    # Check samples generated
    assert len(slip_sound) > 0, "Wheel slip should produce audio samples"
    
    # Check non-zero output
    assert np.max(np.abs(slip_sound)) > 0.01, "Wheel slip should be audible"
    
    # Check envelope (should have exponential decay)
    first_quarter = np.mean(np.abs(slip_sound[:len(slip_sound)//4]))
    last_quarter = np.mean(np.abs(slip_sound[-len(slip_sound)//4:]))
    assert first_quarter > last_quarter, "Wheel slip should decay over time"
    
    print("  ✓ Wheel slip generation test passed")


def test_rail_switch_generation():
    """Test rail switch (aiguillage) sound generation."""
    print("Testing rail switch generation...")
    simulator = MetroSoundSimulator()
    
    # Test rail switch sound
    switch_sound = simulator.generate_rail_switch(1.2, amplitude=0.25)
    
    # Check correct duration
    expected_samples = int(44100 * 1.2)
    assert len(switch_sound) == expected_samples, f"Expected {expected_samples} samples, got {len(switch_sound)}"
    
    # Check non-zero output
    assert np.max(np.abs(switch_sound)) > 0.01, "Rail switch should be audible"
    
    # Check it's not silent
    assert np.std(switch_sound) > 0, "Rail switch should not be silent"
    
    print("  ✓ Rail switch generation test passed")


def test_rail_defects_generation():
    """Test rail defects sound generation."""
    print("Testing rail defects generation...")
    simulator = MetroSoundSimulator()
    
    # Test rail defects sound multiple times to cover different defect types
    for _ in range(5):
        defect_sound = simulator.generate_rail_defects(0.8, amplitude=0.2)
        
        # Check correct duration
        expected_samples = int(44100 * 0.8)
        assert len(defect_sound) == expected_samples, f"Expected {expected_samples} samples, got {len(defect_sound)}"
        
        # Check non-zero output
        assert np.max(np.abs(defect_sound)) > 0.005, "Rail defects should be audible"
    
    print("  ✓ Rail defects generation test passed")


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
        test_compressed_air_generation,
        test_electric_motor_generation,
        test_inverter_generation,
        test_wheel_flange_squeal_generation,
        test_rail_joint_clicks_generation,
        test_brake_squeal_generation,
        test_low_speed_grinding_generation,
        test_wheel_slip_generation,
        test_rail_switch_generation,
        test_rail_defects_generation,
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
