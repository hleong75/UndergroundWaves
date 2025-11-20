#!/usr/bin/env python3
"""
Quick demo of the Metro Sound Simulator
Runs a short simulation to demonstrate all features including
compressed air systems and electric traction motors.
"""

from metro_sounds import MetroSoundSimulator
import time


def main():
    print("\n" + "="*60)
    print("🚇⚡💨 METRO SOUND SIMULATOR - QUICK DEMO")
    print("="*60)
    print("\nThis demo showcases all sound features including:")
    print("  - Compressed air door systems")
    print("  - Compressed air brakes")
    print("  - Electric traction motors")
    print("  - Power inverters (IGBT/PWM)")
    print()
    
    simulator = MetroSoundSimulator(sample_rate=44100)
    
    # Demo each sound type
    print("1. Door Closing with Compressed Air System:")
    print("   - Warning beeps")
    print("   - Air pressure release")
    print("   - Door motor and continuous air hiss")
    print("   - Final air equalization and slam")
    simulator.door_closing()
    time.sleep(1)
    
    print("\n2. Electric Motor Acceleration:")
    print("   - Power inverter startup (PWM switching)")
    print("   - Traction motor whine (rising pitch)")
    print("   - Harmonically rich electric motor sound")
    simulator.acceleration(2.5)
    time.sleep(0.5)
    
    print("\n3. Ambient Travel with Electric Motors:")
    print("   - Track rumbling and vibrations")
    print("   - Constant electric motor hum")
    print("   - Inverter background noise")
    simulator.ambient_rumble(3.0)
    time.sleep(0.5)
    
    print("\n4. Sharp Turn with Screeching:")
    print("   - Metal on metal screech")
    print("   - High frequency sweep")
    simulator.turn_screech()
    time.sleep(0.5)
    
    print("\n5. Deceleration with Air Brakes:")
    print("   - Electric regenerative braking (falling pitch)")
    print("   - Compressed air brake engagement")
    print("   - Brake pad friction sound")
    simulator.deceleration(2.5)
    time.sleep(0.5)
    
    print("\n6. Station Stop - Electric Idle:")
    print("   - Auxiliary systems humming (120 Hz)")
    print("   - Air compressor cycling (180 Hz)")
    print("   - Inverter standby noise")
    simulator.electric_idle(2.0)
    time.sleep(0.5)
    
    print("\n7. Door Closing Again:")
    simulator.door_closing()
    
    print("\n" + "="*60)
    print("✅ Demo complete!")
    print("="*60)
    print("\nFeatures demonstrated:")
    print("  ✓ Compressed air door systems")
    print("  ✓ Compressed air brakes")
    print("  ✓ Electric traction motors with harmonics")
    print("  ✓ Power inverter (PWM) sounds")
    print("  ✓ Regenerative braking")
    print("  ✓ Auxiliary electric systems")
    print("\nTo run a full simulation, use: python metro_sounds.py")
    print()


if __name__ == "__main__":
    main()
