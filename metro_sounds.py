#!/usr/bin/env python3
"""
Metro Sound Simulator - Simulates realistic metro/subway sounds
Simulateur de bruits de métro - Simule des sons réalistes de métro/souterrain

Includes random events like turns with screeching and door closures.
Comprend des événements aléatoires comme des virages avec grincements et des fermetures de portes.
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
    
    def generate_compressed_air_release(self, duration: float, amplitude: float = 0.25) -> np.ndarray:
        """
        Generate compressed air release sound (for doors and brakes).
        
        Args:
            duration: Duration in seconds
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        # High frequency noise for air hiss with decreasing amplitude
        samples = int(self.sample_rate * duration)
        noise = self.generate_noise(duration, amplitude=amplitude, low_freq=3000, high_freq=10000)
        
        # Apply exponential decay envelope for realistic air release
        t = np.linspace(0, duration, samples, False)
        decay = np.exp(-2 * t / duration)  # Exponential decay
        
        # Add some turbulence variation
        turbulence = 1 + 0.15 * np.random.normal(0, 1, samples)
        
        return noise * decay * turbulence
    
    def generate_electric_motor_whine(self, duration: float, start_freq: float = 300, 
                                      end_freq: float = 800, amplitude: float = 0.15) -> np.ndarray:
        """
        Generate electric traction motor whine (characteristic of electric trains).
        
        Args:
            duration: Duration in seconds
            start_freq: Starting frequency in Hz
            end_freq: Ending frequency in Hz
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        # Electric motor produces harmonically rich sound
        fundamental = self.generate_sweep(start_freq, end_freq, duration, amplitude)
        
        # Add harmonics for more realistic electric motor sound
        harmonic2 = self.generate_sweep(start_freq * 2, end_freq * 2, duration, amplitude * 0.3)
        harmonic3 = self.generate_sweep(start_freq * 3, end_freq * 3, duration, amplitude * 0.15)
        
        # Combine with slight phase differences
        samples = len(fundamental)
        combined = np.zeros(samples)
        combined += fundamental
        combined[:min(len(harmonic2), samples)] += harmonic2[:min(len(harmonic2), samples)]
        combined[:min(len(harmonic3), samples)] += harmonic3[:min(len(harmonic3), samples)]
        
        # Add slight PWM (inverter) modulation characteristic of modern electric trains
        t = np.linspace(0, duration, samples, False)
        pwm_freq = random.uniform(4000, 6000)  # Inverter switching frequency
        pwm_modulation = 1 + 0.03 * np.sin(2 * np.pi * pwm_freq * t)
        
        return combined * pwm_modulation
    
    def generate_inverter_sound(self, duration: float = 0.5, amplitude: float = 0.1) -> np.ndarray:
        """
        Generate power inverter switching sound (electric trains).
        
        Args:
            duration: Duration in seconds
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        # High frequency carrier from IGBT/MOSFET switching
        carrier_freq = random.uniform(4000, 8000)
        carrier = self.generate_tone(carrier_freq, duration, amplitude * 0.3)
        
        # Modulation at lower frequency
        samples = len(carrier)
        t = np.linspace(0, duration, samples, False)
        modulation = 1 + 0.5 * np.sin(2 * np.pi * 120 * t)  # 120 Hz modulation
        
        return carrier * modulation

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
        Generate and play ambient metro rumble with electric motor background.
        
        Args:
            duration: Duration in seconds
        """
        print("  🚇⚡ Rumbling along the tracks (electric motors)...")
        # Low frequency rumble with some variation
        rumble = self.generate_noise(duration, amplitude=0.15, low_freq=40, high_freq=150)
        
        # Add some periodic vibration
        vibration_freq = 8  # Hz
        t = np.linspace(0, duration, len(rumble), False)
        vibration = 0.05 * np.sin(2 * np.pi * vibration_freq * t)
        rumble = rumble * (1 + vibration)
        
        # Add constant electric motor hum in background
        motor_freq = random.uniform(400, 600)
        motor_hum = self.generate_tone(motor_freq, duration, amplitude=0.06)
        
        # Slight inverter noise
        inverter_noise = self.generate_noise(duration, amplitude=0.04, low_freq=4000, high_freq=7000)
        
        combined = rumble + motor_hum + inverter_noise
        self.play_sound(combined, blocking=False)
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
        """Generate and play door closing sequence with compressed air system."""
        print("  🚪 Doors closing! Beep beep beep...")
        
        # Warning beeps
        beep_freq = 800
        for i in range(3):
            beep = self.generate_tone(beep_freq, 0.2, amplitude=0.25)
            self.play_sound(beep, blocking=True)
            time.sleep(0.15)
        
        time.sleep(0.3)
        
        # Compressed air system activation and door movement
        print("  💨 *PSSSHHHH* (compressed air) *WHIRRRR* *THUNK*")
        
        # Initial air pressure release as doors unlock
        air_release = self.generate_compressed_air_release(0.4, amplitude=0.22)
        self.play_sound(air_release, blocking=True)
        
        # Door motor sound during closing
        time.sleep(0.1)
        door_motor = self.generate_sweep(200, 150, 0.8, amplitude=0.15)
        
        # Continuous air hiss during movement
        hiss = self.generate_noise(0.8, amplitude=0.15, low_freq=2000, high_freq=7000)
        door_sound = door_motor + hiss[:len(door_motor)]
        self.play_sound(door_sound, blocking=True)
        
        # Final air pressure equalization and door slam
        time.sleep(0.1)
        final_air = self.generate_compressed_air_release(0.5, amplitude=0.18)
        thunk = self.generate_tone(150, 0.15, amplitude=0.4)
        combined = np.concatenate([final_air, thunk])
        
        self.play_sound(combined, blocking=True)
    
    def acceleration(self, duration: float = 3.0):
        """
        Simulate electric metro accelerating with traction motor sounds.
        
        Args:
            duration: Duration in seconds
        """
        print("  🚀⚡ Accelerating (electric motor whine)...")
        # Base rumble from wheels
        base_rumble = self.generate_noise(duration, amplitude=0.10)
        
        # Electric traction motor whine (characteristic of electric trains)
        motor_whine = self.generate_electric_motor_whine(duration, 300, 900, amplitude=0.18)
        
        # Power inverter sound at startup
        inverter = self.generate_inverter_sound(duration * 0.3, amplitude=0.12)
        
        # Combine all sounds
        samples = int(self.sample_rate * duration)
        combined = np.zeros(samples)
        combined += base_rumble[:samples]
        combined += motor_whine[:samples]
        combined[:len(inverter)] += inverter
        
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def deceleration(self, duration: float = 2.5):
        """
        Simulate metro decelerating with electric regenerative braking and air brakes.
        
        Args:
            duration: Duration in seconds
        """
        print("  🛑💨 Slowing down (air brakes + regen braking)...")
        # Base rumble
        decel_rumble = self.generate_noise(duration, amplitude=0.12)
        
        # Electric motor regenerative braking (falling pitch)
        motor_whine = self.generate_electric_motor_whine(duration, 800, 250, amplitude=0.15)
        
        # Air brake engagement sound (compressed air)
        brake_duration = duration * 0.6
        air_brake = self.generate_compressed_air_release(brake_duration, amplitude=0.20)
        
        # Brake pad friction sound (low frequency rumble with some harmonics)
        friction_sound = self.generate_noise(duration, amplitude=0.10, low_freq=100, high_freq=400)
        
        # Combine all sounds
        samples = int(self.sample_rate * duration)
        combined = np.zeros(samples)
        combined += decel_rumble[:samples]
        combined += motor_whine[:samples]
        combined[:len(air_brake)] += air_brake
        combined += friction_sound[:samples]
        
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def electric_idle(self, duration: float = 1.0):
        """
        Generate electric system idle sound when stopped at station.
        
        Args:
            duration: Duration in seconds
        """
        # Compressor and auxiliary systems humming
        aux_hum = self.generate_tone(120, duration, amplitude=0.08)  # 120 Hz hum
        
        # Air compressor cycling
        compressor = self.generate_tone(180, duration, amplitude=0.06)
        
        # High frequency inverter standby
        inverter_idle = self.generate_noise(duration, amplitude=0.04, low_freq=3000, high_freq=5000)
        
        combined = aux_hum + compressor + inverter_idle
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def station_arrival(self):
        """Simulate arriving at a station with compressed air brakes."""
        print("\n📍 Approaching station...")
        self.deceleration(2.5)
        time.sleep(0.5)
        
        # Stopped at station - electric idle sounds
        print("  ⏸️  Stopped at station (electric systems humming)...")
        self.electric_idle(1.0)
        
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
