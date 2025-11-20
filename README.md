# UndergroundWaves 🚇

A realistic metro/subway sound simulator that generates authentic underground railway sounds including ambient rumbling, screeching turns, door closures, and station stops.

## Features

- **Compressed Air Door Systems**: Realistic air pressure release, door motor sounds, and pneumatic hiss during door operation
- **Compressed Air Brakes**: Air brake engagement and release sounds with friction effects
- **Electric Traction Motors**: Harmonically rich motor whine with PWM inverter modulation
- **Regenerative Braking**: Electric motor sounds during deceleration with falling pitch
- **Power Inverter Sounds**: IGBT/MOSFET switching noise characteristic of modern electric trains
- **Ambient Rumbling**: Continuous low-frequency rumble with electric motor hum in background
- **Random Turn Events**: Sharp turns with realistic metal-on-metal screeching sounds
- **Station Arrivals**: Complete sequence with electric idle sounds (compressor, auxiliaries)
- **Realistic Timing**: Random event timing inspired by real metro operations

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

The program will generate:
- Continuous rumbling sounds with electric motor hum
- Random screeching when taking sharp turns
- Door closing sequences with compressed air and warning beeps
- Electric motor acceleration and regenerative braking
- Compressed air brake sounds
- Station arrival and departure sounds with electric idle

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

## Sound Events

The simulator randomly generates these events:

| Event | Probability | Description |
|-------|-------------|-------------|
| Ambient Rumble | 60% | Normal travel with low rumbling |
| Sharp Turn | 25% | Metal screeching as metro turns |
| Station Stop | 15% | Full deceleration, stop, and door sequence |

## Technical Details

- Sample Rate: 44,100 Hz (CD quality)
- Audio Format: 16-bit PCM
- Event-based architecture with randomized timing
- Real-time audio synthesis

## License

This project is open source and available for educational and entertainment purposes.

## Contributing

Feel free to open issues or submit pull requests to improve the simulator or add new sound effects!