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
    print("🚇⚡💨🛤️🤖 METRO SOUND SIMULATOR - QUICK DEMO")
    print("="*60)
    print("\nThis demo showcases all sound features including:")
    print("  - 🤖 AI-Enhanced Sound Generation (NEW!)")
    print("  - Compressed air door systems")
    print("  - Compressed air brakes")
    print("  - Electric traction motors")
    print("  - Power inverters (IGBT/PWM)")
    print("  - Wheel-rail friction sounds")
    print("\n🤖 AI Features:")
    print("  - Context-aware sound generation")
    print("  - Adaptive sound evolution over time")
    print("  - Intelligent event prediction")
    print("  - Realistic wear and temperature simulation")
    print()
    
    simulator = MetroSoundSimulator(sample_rate=44100, enable_ai=True)
    print()
    
    # Demo each sound type
    print("1. Door Closing with Compressed Air System:")
    print("   - Warning beeps")
    print("   - Air pressure release")
    print("   - Door motor and continuous air hiss")
    print("   - Final air equalization and slam")
    simulator.door_closing()
    time.sleep(1)
    
    print("\n2. Electric Motor Acceleration with Wheel-Rail Sounds:")
    print("   - Power inverter startup (PWM switching)")
    print("   - Traction motor whine (rising pitch)")
    print("   - Low-speed grinding sounds (NEW!)")
    print("   - Occasional wheel slip (NEW!)")
    simulator.acceleration(2.5)
    time.sleep(0.5)
    
    print("\n3. Ambient Travel with Enhanced Wheel-Rail Contact:")
    print("   - Track rumbling and vibrations")
    print("   - Constant electric motor hum")
    print("   - Rail joint clicks - clickety-clack (NEW!)")
    print("   - Inverter background noise")
    simulator.ambient_rumble(3.0)
    time.sleep(0.5)
    
    print("\n4. Gentle Curve with Wheel Flange Contact:")
    print("   - Subtle motor frequency changes")
    print("   - Enhanced wheel-rail contact")
    print("   - Occasional flange squeal (NEW!)")
    simulator.gentle_curve(2.5)
    time.sleep(0.5)
    
    print("\n5. Sharp Turn with Screeching:")
    print("   - Metal on metal screech")
    print("   - High frequency sweep")
    simulator.turn_screech()
    time.sleep(0.5)
    
    print("\n6. Deceleration with Enhanced Braking Sounds:")
    print("   - Electric regenerative braking (falling pitch)")
    print("   - Compressed air brake engagement")
    print("   - Enhanced brake pad friction")
    print("   - Occasional brake squeal (NEW!)")
    print("   - Low-speed grinding at end (NEW!)")
    simulator.deceleration(2.5)
    time.sleep(0.5)
    
    print("\n7. Station Stop - Electric Idle:")
    print("   - Auxiliary systems humming (120 Hz)")
    print("   - Air compressor cycling (180 Hz)")
    print("   - Inverter standby noise")
    simulator.electric_idle(2.0)
    time.sleep(0.5)
    
    print("\n8. Door Closing Again:")
    simulator.door_closing()
    
    print("\n" + "="*60)
    print("✅ Demo complete!")
    print("="*60)
    print("\nFeatures demonstrated:")
    print("  ✓ 🤖 AI-Enhanced sound generation")
    print("  ✓ Context-aware frequency modulation")
    print("  ✓ Adaptive sound evolution")
    print("  ✓ Compressed air door systems")
    print("  ✓ Compressed air brakes")
    print("  ✓ Electric traction motors with harmonics")
    print("  ✓ Power inverter (PWM) sounds")
    print("  ✓ Regenerative braking")
    print("  ✓ Auxiliary electric systems")
    print("  ✓ Rail joint clicks (clickety-clack)")
    print("  ✓ Wheel flange squeal on curves")
    print("  ✓ Brake squeal")
    print("  ✓ Low-speed grinding")
    print("  ✓ Wheel slip sounds")
    print("\n🤖 AI enhancements make sounds more realistic by:")
    print("  • Learning from journey context")
    print("  • Adapting to speed, temperature, and wear")
    print("  • Evolving over time (brake heating, bearing wear)")
    print("  • Intelligently predicting events")
    print("\nTo run a full simulation, use: python metro_sounds.py")
    print()


if __name__ == "__main__":
    main()
