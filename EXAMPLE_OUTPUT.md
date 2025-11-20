# Example Output

Here's what you'll see when running the Metro Sound Simulator:

## Running the Main Simulator

```bash
$ python metro_sounds.py

🎵 Welcome to the Metro Sound Simulator! 🎵

This program simulates realistic metro/subway sounds including:
  - Ambient rumbling and engine noise
  - Random turns with metal screeching
  - Door closing sequences with warning beeps
  - Station arrivals and departures
  - Acceleration and deceleration sounds

How many minutes should the simulation run? (default: 2): 1

Press Ctrl+C at any time to stop the simulation.

============================================================
🚇 METRO SOUND SIMULATOR 🚇
============================================================
Starting 1-minute metro journey...

  🚪 Doors closing! Beep beep beep...
  💨 *PSSSHHHH* (compressed air) *WHIRRRR* *THUNK*
  🚀⚡ Accelerating (electric motor whine)...
  🚇⚡ Rumbling along the tracks (electric motors)...
  🔊 SCREEEECH! Taking a sharp turn...
  🚇⚡ Rumbling along the tracks (electric motors)...
  🚇⚡ Rumbling along the tracks (electric motors)...

📍 Approaching station...
  🛑💨 Slowing down (air brakes + regen braking)...
  ⏸️  Stopped at station (electric systems humming)...
  🚪 Doors closing! Beep beep beep...
  💨 *PSSSHHHH* (compressed air) *WHIRRRR* *THUNK*
  🚀⚡ Accelerating (electric motor whine)...
  🚇⚡ Rumbling along the tracks (electric motors)...
  🔊 SCREEEECH! Taking a sharp turn...
  🚇⚡ Rumbling along the tracks (electric motors)...

============================================================
🏁 Metro journey complete!
============================================================
```

## Running the Demo

```bash
$ python demo.py

============================================================
🚇 METRO SOUND SIMULATOR - QUICK DEMO
============================================================

This demo will showcase all the sound features:

1. Door Closing Sequence:
   - Warning beeps
   - Pneumatic hiss and door slam
  🚪 Doors closing! Beep beep beep...
  💨 *PSSSHHHH* *THUNK*

2. Acceleration:
   - Engine revving up
   - Rising pitch
  🚀 Accelerating...

3. Ambient Rumble:
   - Low frequency rumbling
   - Track vibrations
  🚇 Rumbling along the tracks...

4. Sharp Turn with Screeching:
   - Metal on metal screeching
   - High frequency sweep
  🔊 SCREEEECH! Taking a sharp turn...

5. More Rumbling:
  🚇 Rumbling along the tracks...

6. Deceleration:
   - Engine slowing down
   - Falling pitch
  🛑 Slowing down...

7. Another Door Closing:
  🚪 Doors closing! Beep beep beep...
  💨 *PSSSHHHH* *THUNK*

============================================================
✅ Demo complete!
============================================================

To run a full simulation, use: python metro_sounds.py
```

## Sound Events

The simulator randomly generates these authentic metro sounds:

### 🚇⚡ Ambient Rumble (Electric Train)
- Low frequency rumbling (40-150 Hz) from wheels
- Constant electric motor hum (400-600 Hz)
- Inverter background noise (4-7 kHz)
- Periodic track vibrations at ~8 Hz
- Duration: 3-6 seconds

### 🔊 Sharp Turn / Screeching
- High frequency sweeps (600-1200 Hz)
- Metal-on-metal screech effect
- Multiple frequency components layered
- Duration: 1.5-3 seconds

### 🚪💨 Door Closing (Compressed Air System)
1. Three warning beeps at 800 Hz (0.2s each)
2. Short pause
3. Compressed air pressure release (exponential decay)
4. Door motor sound (200-150 Hz sweep)
5. Continuous air hiss during movement
6. Final air equalization
7. Door slam (150 Hz thunk)

### 🚀⚡ Acceleration (Electric Motor)
- Electric traction motor whine (300-900 Hz sweep)
- Multiple harmonics (2x, 3x fundamental)
- Power inverter startup (PWM at 4-6 kHz)
- Base rumble from wheels
- Duration: ~3 seconds

### 🛑💨 Deceleration (Regenerative + Air Brakes)
- Electric motor regen braking (800-250 Hz sweep)
- Compressed air brake engagement
- Brake pad friction (100-400 Hz)
- Combined braking systems
- Duration: ~2.5 seconds

### ⏸️⚡ Station Stop (Electric Idle)
- Auxiliary systems hum (120 Hz)
- Air compressor cycling (180 Hz)
- Inverter standby noise (3-5 kHz)
- Realistic idle power consumption sounds

### 📍 Station Arrival
- Complete deceleration with air brakes
- Stop with electric idle sounds
- Compressed air door operation
- Electric motor acceleration for departure

## Event Probabilities

The simulator uses weighted random selection:

- **60%** - Ambient rumbling (normal travel)
- **25%** - Sharp turn with screeching
- **15%** - Station arrival and departure

This creates a realistic metro journey experience with varied events!
