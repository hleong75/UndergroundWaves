# Example Output

Here's what you'll see when running the **Realistic Metro Journey Simulator**:

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
🚇 REALISTIC METRO JOURNEY SIMULATOR 🚇
============================================================
Starting 1.0-minute realistic metro journey...

🎵 Continuous ambient sounds with logical transitions


📍 At station - preparing to depart...
  🚪 Doors closing (warning chime)...
  💨 Air system engaging - doors closing smoothly...
  🚀⚡ Departing station (gradual acceleration)...
  🚀⚡ Smoothly accelerating (electric traction motors)...

🚇 Cruising to next station...
  🚇⚡ Cruising smoothly (continuous motor hum)...
  🚇⚡ Cruising smoothly (continuous motor hum)...
  🔄 Taking a gentle curve...
  🚇⚡ Cruising smoothly (continuous motor hum)...

📍 Station ahead - preparing to stop...
  🛑💨 Gradually slowing down (regenerative + air brakes)...
  ⏸️  Arrived at station (electric systems humming)...

📍 At station - preparing to depart...
  🚪 Doors closing (warning chime)...
  💨 Air system engaging - doors closing smoothly...
  🚀⚡ Departing station (gradual acceleration)...
  🚀⚡ Smoothly accelerating (electric traction motors)...
  🚇⚡ Cruising smoothly (continuous motor hum)...

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

## Sound Phases

The simulator creates a **continuous journey** with these authentic metro sounds:

### 🚇⚡ Continuous Cruising (Electric Train)
- Low frequency rumbling (40-150 Hz) from wheels
- Multi-layered electric motor hum (450-550 Hz + harmonics)
- Enhanced wheel-rail contact sounds (800-2000 Hz)
- **Rhythmic rail joint clicks** (clickety-clack pattern at speed-dependent intervals)
- Inverter background noise (4-7 kHz)
- Periodic track vibrations at ~3 Hz and ~8 Hz
- Natural random variations for realism
- Smooth fade in/out transitions
- Duration: 10-18 seconds per segment

### 🔄 Gentle Curves
- Subtle motor frequency changes (500-600 Hz)
- Slightly increased rumble
- Enhanced wheel-rail contact variations with flange contact noise (900-1500 Hz)
- **Occasional wheel flange squeal** (30% chance) - multi-frequency metallic squealing with pulsing modulation
- No harsh emergency screeching - realistic curve negotiation
- Duration: 2.5-4 seconds

### 🚪💨 Smooth Door Operations (Compressed Air System)
1. Three melodic warning chimes at 800 Hz (~0.18s each)
2. Short pause
3. Compressed air pressure release (softer, controlled)
4. Door motor sound (210-145 Hz sweep over 1s)
5. Continuous air hiss during movement (quieter, smoother)
6. Door mechanism sounds (150-400 Hz)
7. Final air equalization and gentle seal (145 Hz)
8. All with smooth fade in/out envelopes

### 🚀⚡ Gradual Acceleration (Electric Traction Motors)
- Progressive power delivery with amplitude ramping
- Electric traction motor whine (250-850 Hz sweep)
- Motor load harmonics (500-1700 Hz)
- Power inverter startup surge (PWM at 4-6 kHz with decay)
- **Low-speed grinding** sounds from wheels (150-400 Hz) at start
- **Occasional wheel slip** (20% chance) - rapid frequency modulation and grinding
- Track noise increasing with speed
- Base rumble growing from quiet to full
- Smooth fade-in at start
- Duration: ~4 seconds (adjustable)

### 🛑💨 Gradual Deceleration (Regenerative + Air Brakes)
- Progressive power reduction with envelope
- Electric regen braking (850-200 Hz sweep)
- Motor harmonics fading (1700-400 Hz)
- Delayed air brake engagement (starts 20% into decel)
- Enhanced brake pad friction increasing progressively (100-400 Hz)
- **Occasional brake squeal** (25% chance) - high-frequency resonance (2500-4000 Hz) with wobble modulation
- **Low-speed grinding** at end (150-400 Hz with roughness texture)
- Track noise decreasing with speed
- Smooth fade-out at end
- Duration: ~3.5 seconds (adjustable)

### ⏸️⚡ Electric Idle at Station (Realistic Auxiliary Systems)
- Main power supply hum (60, 120, 180 Hz harmonics)
- Air compressor with realistic on/off cycling (~3s period)
- Cooling fan sounds (90-110 Hz + turbulence)
- Inverter standby with 120 Hz modulation (3-5 kHz)
- Occasional relay clicks for realism
- All with smooth fade transitions
- Duration: ~2 seconds at each stop

## Journey Logic

The simulator follows a **realistic, continuous journey pattern**:

**Journey Structure:**
1. **Departure Phase** (~5-6s): Door close → Smooth acceleration
2. **Cruising Phase** (25-45s): Continuous ambient with occasional gentle curves
3. **Arrival Phase** (~4s): Gradual deceleration → Station idle
4. **Dwell Time** (~2-3s): Electric systems running → Next departure

**Key Improvements:**
- ✅ **Continuous soundscape** - no silence gaps
- ✅ **Logical transitions** - sounds flow naturally into each other
- ✅ **Progressive changes** - no abrupt jumps in sound
- ✅ **Realistic timing** - based on actual metro operations
- ✅ **Smooth curves** - no harsh "breakdown-like" screeching
- ✅ **Overlapping audio** - multiple layers for richness

This creates an immersive, realistic metro journey that sounds **continuous and natural**!
