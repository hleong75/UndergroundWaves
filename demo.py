#!/usr/bin/env python3
"""
Quick demo of the Metro Sound Simulator
Runs a short simulation to demonstrate all features.
"""

from metro_sounds import MetroSoundSimulator
import time


def main():
    print("\n" + "="*60)
    print("🚇 METRO SOUND SIMULATOR - QUICK DEMO")
    print("="*60)
    print("\nThis demo will showcase all the sound features:\n")
    
    simulator = MetroSoundSimulator(sample_rate=44100)
    
    # Demo each sound type
    print("1. Door Closing Sequence:")
    print("   - Warning beeps")
    print("   - Pneumatic hiss and door slam")
    simulator.door_closing()
    time.sleep(1)
    
    print("\n2. Acceleration:")
    print("   - Engine revving up")
    print("   - Rising pitch")
    simulator.acceleration(2.0)
    time.sleep(0.5)
    
    print("\n3. Ambient Rumble:")
    print("   - Low frequency rumbling")
    print("   - Track vibrations")
    simulator.ambient_rumble(3.0)
    time.sleep(0.5)
    
    print("\n4. Sharp Turn with Screeching:")
    print("   - Metal on metal screeching")
    print("   - High frequency sweep")
    simulator.turn_screech()
    time.sleep(0.5)
    
    print("\n5. More Rumbling:")
    simulator.ambient_rumble(2.0)
    time.sleep(0.5)
    
    print("\n6. Deceleration:")
    print("   - Engine slowing down")
    print("   - Falling pitch")
    simulator.deceleration(2.0)
    time.sleep(0.5)
    
    print("\n7. Another Door Closing:")
    simulator.door_closing()
    
    print("\n" + "="*60)
    print("✅ Demo complete!")
    print("="*60)
    print("\nTo run a full simulation, use: python metro_sounds.py")
    print()


if __name__ == "__main__":
    main()
