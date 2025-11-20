# UndergroundWaves 🚇

A realistic metro/subway sound simulator that generates authentic, continuous underground railway sounds with smooth transitions and logical journey sequences. Experience realistic station departures, smooth cruising, gentle curves, and gradual arrivals.

## Features

- **🔄 Continuous Sound Journey**: Seamless audio experience with smooth transitions between all phases
- **🚉 Realistic Journey Structure**: Logical progression through departure → cruising → arrival → stop cycles
- **🚪 Smooth Door Operations**: Refined compressed air systems with melodic warning chimes and controlled door movements
- **⚡ Gradual Acceleration/Deceleration**: Progressive power delivery and braking that mimics real electric trains
- **🎵 Multi-layered Ambient Sounds**: Continuous motor hum, track vibrations, wheel-rail contact, and inverter noise
- **🛤️ Realistic Wheel-Rail Friction**: Rail joint clicks (clickety-clack), wheel flange squeal on curves, brake squeal, low-speed grinding, and occasional wheel slip
- **💨 Regenerative + Air Braking**: Realistic combined braking system with gradual engagement
- **🔧 Electric System Idle**: Authentic compressor cycling, cooling fans, and auxiliary systems at stations
- **🌊 Smooth Transitions**: All sounds fade in/out naturally to eliminate abrupt changes
- **🛤️ Gentle Curves**: Realistic curve negotiation with subtle wheel-rail contact and occasional flange squeal
- **⏱️ Intelligent Timing**: Journey segments timed to create natural metro operation flow

## Installation

### Requirements

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/hleong75/UndergroundWaves.git
cd UndergroundWaves
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the metro sound simulator:

```bash
python metro_sounds.py
```

You'll be prompted to enter how many minutes you want the simulation to run (default is 2 minutes).

The program will generate a **continuous, realistic journey** with:
- Seamless ambient rumbling with layered electric motor sounds
- Smooth acceleration and deceleration phases with gradual power changes
- Realistic station sequences: arrival → idle systems → door operations → departure
- Gentle curves with subtle sound variations (no harsh screeching)
- Natural transitions between all sound phases
- Multi-layered soundscapes that overlap for continuous audio experience

Press `Ctrl+C` at any time to stop the simulation.

## How It Works

The simulator uses:
- **numpy** for audio signal generation
- **sounddevice** for real-time audio playback
- Procedural audio synthesis to create realistic sounds:
  - Low-frequency noise for rumbling
  - Frequency sweeps for screeching and electric motor whine
  - Sine waves for warning beeps and motor harmonics
  - High-frequency noise for pneumatic air systems
  - Exponential decay envelopes for compressed air release
  - PWM modulation for power inverter sounds
  - Harmonic synthesis for electric traction motors
  - Rhythmic percussive sounds for rail joint clicks
  - Multi-frequency squeals for wheel flange contact and brake squeal
  - Low-frequency grinding for wheel-rail friction at low speeds
  - Rapid modulation for wheel slip effects

All sounds are generated in real-time using mathematical models inspired by actual metro/subway acoustics, specifically modeling:
- **Compressed air systems** (doors and brakes)
- **Electric traction motors** with characteristic frequency sweeps
- **Power electronics** (IGBT/PWM inverters at 4-8 kHz)

## Examples

### Basic Run
```bash
$ python metro_sounds.py
How many minutes should the simulation run? (default: 2): 2
```

### Short Test
```bash
$ python metro_sounds.py
How many minutes should the simulation run? (default: 2): 0.5
```

## Journey Structure

The simulator creates a **continuous, logical journey** following real metro operations:

| Phase | Duration | Description |
|-------|----------|-------------|
| **Station Departure** | ~5-6s | Door closing → smooth acceleration with progressive power |
| **Cruising** | 25-45s | Continuous ambient sounds with occasional gentle curves |
| **Approaching Station** | ~4s | Gradual deceleration with regenerative + air braking |
| **At Station** | ~2-3s | Electric idle systems (compressors, fans, auxiliaries) |

All phases transition smoothly with overlapping sounds for a seamless, realistic experience.

## Technical Details

- Sample Rate: 44,100 Hz (CD quality)
- Audio Format: 16-bit PCM
- Event-based architecture with randomized timing
- Real-time audio synthesis

## License

This project is open source and available for educational and entertainment purposes.

## Contributing

Feel free to open issues or submit pull requests to improve the simulator or add new sound effects!