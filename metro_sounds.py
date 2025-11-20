#!/usr/bin/env python3
"""
Metro Sound Simulator - Simulates realistic metro/subway sounds
Includes random events like turns with screeching and door closures.
"""

import numpy as np
import time
import random
from typing import Tuple

# Try to import sounddevice, but allow the module to work without it for testing
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except (ImportError, OSError):
    AUDIO_AVAILABLE = False
    print("⚠️  Warning: Audio playback not available. Running in silent mode.")


class MetroSoundSimulator:
    """Simulates realistic metro/subway sounds with random events."""
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the metro sound simulator.
        
        Args:
            sample_rate: Audio sample rate in Hz (default: 44100)
        """
        self.sample_rate = sample_rate
        self.is_running = False
        
    def generate_tone(self, frequency: float, duration: float, amplitude: float = 0.3) -> np.ndarray:
        """
        Generate a simple sine wave tone.
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            amplitude: Volume level (0.0 to 1.0)
            
        Returns:
            Audio samples as numpy array
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = amplitude * np.sin(2 * np.pi * frequency * t)
        return tone
    
    def generate_noise(self, duration: float, amplitude: float = 0.1, 
                       low_freq: float = 50, high_freq: float = 200) -> np.ndarray:
        """
        Generate filtered noise (simulates rumbling).
        
        Args:
            duration: Duration in seconds
            amplitude: Volume level
            low_freq: Low frequency cutoff in Hz
            high_freq: High frequency cutoff in Hz
            
        Returns:
            Audio samples as numpy array
        """
        samples = int(self.sample_rate * duration)
        # Generate white noise
        noise = np.random.normal(0, amplitude, samples)
        
        # Simple low-pass filtering by averaging to simulate rumble
        window_size = int(self.sample_rate / high_freq)
        if window_size > 1:
            noise = np.convolve(noise, np.ones(window_size)/window_size, mode='same')
        
        return noise
    
    def generate_sweep(self, start_freq: float, end_freq: float, 
                       duration: float, amplitude: float = 0.4) -> np.ndarray:
        """
        Generate a frequency sweep (for screeching sounds).
        
        Args:
            start_freq: Starting frequency in Hz
            end_freq: Ending frequency in Hz
            duration: Duration in seconds
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        # Linear frequency sweep
        freq = np.linspace(start_freq, end_freq, len(t))
        phase = 2 * np.pi * np.cumsum(freq) / self.sample_rate
        sweep = amplitude * np.sin(phase)
        
        # Add envelope to avoid clicks
        envelope = np.ones_like(sweep)
        fade_samples = int(0.05 * self.sample_rate)  # 50ms fade
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return sweep * envelope
    
    def play_sound(self, audio: np.ndarray, blocking: bool = True):
        """
        Play audio through the default audio device.
        
        Args:
            audio: Audio samples to play
            blocking: If True, wait for playback to complete
        """
        if AUDIO_AVAILABLE:
            sd.play(audio, self.sample_rate)
            if blocking:
                sd.wait()
        else:
            # Simulate playback delay when audio is not available
            duration = len(audio) / self.sample_rate
            if blocking:
                time.sleep(duration)
    
    def ambient_rumble(self, duration: float = 3.0):
        """
        Generate and play ambient metro rumble.
        
        Args:
            duration: Duration in seconds
        """
        print("  🚇 Rumbling along the tracks...")
        # Low frequency rumble with some variation
        rumble = self.generate_noise(duration, amplitude=0.15, low_freq=40, high_freq=150)
        
        # Add some periodic vibration
        vibration_freq = 8  # Hz
        t = np.linspace(0, duration, len(rumble), False)
        vibration = 0.05 * np.sin(2 * np.pi * vibration_freq * t)
        rumble = rumble * (1 + vibration)
        
        self.play_sound(rumble, blocking=False)
        time.sleep(duration)
    
    def turn_screech(self):
        """Generate and play a turn screeching sound."""
        print("  🔊 SCREEEECH! Taking a sharp turn...")
        duration = random.uniform(1.5, 3.0)
        
        # Metal on metal screech - high frequency sweep
        screech1 = self.generate_sweep(800, 1200, duration * 0.7, amplitude=0.3)
        screech2 = self.generate_sweep(600, 900, duration * 0.5, amplitude=0.2)
        
        # Combine screeches
        max_len = max(len(screech1), len(screech2))
        combined = np.zeros(max_len)
        combined[:len(screech1)] += screech1
        combined[:len(screech2)] += screech2
        
        # Add some rumble underneath (match the combined length)
        rumble_duration = max_len / self.sample_rate
        rumble = self.generate_noise(rumble_duration, amplitude=0.1)
        # Ensure rumble length matches combined
        rumble = rumble[:max_len] if len(rumble) > max_len else np.pad(rumble, (0, max_len - len(rumble)))
        combined += rumble
        
        self.play_sound(combined, blocking=True)
    
    def door_closing(self):
        """Generate and play door closing sequence."""
        print("  🚪 Doors closing! Beep beep beep...")
        
        # Warning beeps
        beep_freq = 800
        for i in range(3):
            beep = self.generate_tone(beep_freq, 0.2, amplitude=0.25)
            self.play_sound(beep, blocking=True)
            time.sleep(0.15)
        
        time.sleep(0.3)
        
        # Pneumatic hiss and door slam
        print("  💨 *PSSSHHHH* *THUNK*")
        hiss_duration = 1.2
        hiss = self.generate_noise(hiss_duration, amplitude=0.2, low_freq=2000, high_freq=8000)
        
        # Add door closing thunk at the end
        thunk = self.generate_tone(150, 0.15, amplitude=0.4)
        combined = np.concatenate([hiss, thunk])
        
        self.play_sound(combined, blocking=True)
    
    def acceleration(self, duration: float = 3.0):
        """
        Simulate metro accelerating.
        
        Args:
            duration: Duration in seconds
        """
        print("  🚀 Accelerating...")
        # Rising pitch rumble
        base_rumble = self.generate_noise(duration, amplitude=0.12)
        
        # Add rising tone to simulate acceleration
        accel_tone = self.generate_sweep(60, 120, duration, amplitude=0.08)
        
        combined = base_rumble + accel_tone
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def deceleration(self, duration: float = 2.5):
        """
        Simulate metro decelerating.
        
        Args:
            duration: Duration in seconds
        """
        print("  🛑 Slowing down...")
        # Falling pitch rumble
        decel_rumble = self.generate_noise(duration, amplitude=0.12)
        
        # Add falling tone
        decel_tone = self.generate_sweep(120, 60, duration, amplitude=0.08)
        
        combined = decel_rumble + decel_tone
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def station_arrival(self):
        """Simulate arriving at a station."""
        print("\n📍 Approaching station...")
        self.deceleration(2.5)
        time.sleep(0.5)
        
        # Stopped at station
        print("  ⏸️  Stopped at station")
        time.sleep(1.0)
        
        self.door_closing()
        time.sleep(0.5)
    
    def run_simulation(self, duration_minutes: float = 2.0):
        """
        Run the metro sound simulation.
        
        Args:
            duration_minutes: How long to run the simulation in minutes
        """
        print("\n" + "="*60)
        print("🚇 METRO SOUND SIMULATOR 🚇")
        print("="*60)
        print(f"Starting {duration_minutes}-minute metro journey...\n")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        self.is_running = True
        
        # Start with doors closing and acceleration
        self.door_closing()
        time.sleep(0.5)
        self.acceleration(3.0)
        
        try:
            while time.time() < end_time and self.is_running:
                # Random event selection
                event = random.choices(
                    ['rumble', 'turn', 'station'],
                    weights=[0.6, 0.25, 0.15],
                    k=1
                )[0]
                
                if event == 'rumble':
                    # Normal travel
                    rumble_duration = random.uniform(3.0, 6.0)
                    self.ambient_rumble(rumble_duration)
                    
                elif event == 'turn':
                    # Sharp turn with screech
                    self.turn_screech()
                    time.sleep(random.uniform(0.5, 1.5))
                    
                elif event == 'station':
                    # Station stop
                    self.station_arrival()
                    self.acceleration(3.0)
                
                # Small pause between events
                time.sleep(random.uniform(0.5, 1.5))
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Simulation stopped by user")
            self.is_running = False
        
        print("\n" + "="*60)
        print("🏁 Metro journey complete!")
        print("="*60 + "\n")


def main():
    """Main entry point for the metro sound simulator."""
    print("\n🎵 Welcome to the Metro Sound Simulator! 🎵\n")
    
    if not AUDIO_AVAILABLE:
        print("⚠️  WARNING: Audio output is not available on this system.")
        print("The simulator will run in silent mode (visual output only).")
        print("To enable audio, ensure PortAudio is installed:")
        print("  - Ubuntu/Debian: sudo apt-get install libportaudio2")
        print("  - macOS: brew install portaudio")
        print("  - Windows: Audio should work with pip install sounddevice\n")
    
    print("This program simulates realistic metro/subway sounds including:")
    print("  - Ambient rumbling and engine noise")
    print("  - Random turns with metal screeching")
    print("  - Door closing sequences with warning beeps")
    print("  - Station arrivals and departures")
    print("  - Acceleration and deceleration sounds\n")
    
    # Get simulation duration from user
    try:
        duration_input = input("How many minutes should the simulation run? (default: 2): ").strip()
        duration = float(duration_input) if duration_input else 2.0
        
        if duration <= 0:
            print("⚠️  Duration must be positive. Using default of 2 minutes.")
            duration = 2.0
    except ValueError:
        print("⚠️  Invalid input. Using default of 2 minutes.")
        duration = 2.0
    
    print("\nPress Ctrl+C at any time to stop the simulation.\n")
    time.sleep(1)
    
    # Create and run simulator
    simulator = MetroSoundSimulator(sample_rate=44100)
    simulator.run_simulation(duration_minutes=duration)


if __name__ == "__main__":
    main()
