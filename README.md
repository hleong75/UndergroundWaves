# UndergroundWaves 🚇

A realistic metro/subway sound simulator that generates authentic underground railway sounds including ambient rumbling, screeching turns, door closures, and station stops.

## Features

- **Ambient Rumbling**: Continuous low-frequency rumble simulating metro movement along tracks
- **Random Turn Events**: Sharp turns with realistic metal-on-metal screeching sounds
- **Door Closures**: Complete door closing sequence with warning beeps and pneumatic hiss
- **Station Arrivals**: Deceleration, stop, and door operations at stations
- **Acceleration/Deceleration**: Dynamic pitch changes simulating speed changes
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
- Continuous rumbling sounds as the metro travels
- Random screeching when taking sharp turns
- Door closing sequences with warning beeps
- Station arrival and departure sounds

Press `Ctrl+C` at any time to stop the simulation.

## How It Works

The simulator uses:
- **numpy** for audio signal generation
- **sounddevice** for real-time audio playback
- Procedural audio synthesis to create realistic sounds:
  - Low-frequency noise for rumbling
  - Frequency sweeps for screeching
  - Sine waves for warning beeps
  - High-frequency noise for pneumatic hiss

All sounds are generated in real-time using mathematical models inspired by actual metro/subway acoustics.

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