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
    
    def generate_wheel_flange_squeal(self, duration: float = 1.5, amplitude: float = 0.35) -> np.ndarray:
        """
        Generate wheel flange squeal sound (when wheel flanges rub against rail sides on curves).
        
        Args:
            duration: Duration in seconds
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # High-pitched metallic squeal - multiple frequency components
        squeal1 = self.generate_sweep(1200, 1800, duration, amplitude * 0.6)
        squeal2 = self.generate_sweep(900, 1500, duration, amplitude * 0.4)
        squeal3 = self.generate_sweep(1500, 2200, duration, amplitude * 0.3)
        
        # Add irregular pulsing for realistic flange contact
        pulse_freq = random.uniform(6, 12)  # Pulsing at 6-12 Hz
        pulse_modulation = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * pulse_freq * t))
        
        # Combine squeals with pulsing
        combined = np.zeros(samples)
        combined[:len(squeal1)] += squeal1
        combined[:len(squeal2)] += squeal2
        combined[:len(squeal3)] += squeal3
        combined = combined * pulse_modulation
        
        # Add some grinding noise component
        grinding = self.generate_noise(duration, amplitude * 0.2, low_freq=600, high_freq=3000)
        combined[:len(grinding)] += grinding
        
        # Apply envelope for realistic onset/release
        envelope = np.ones(samples)
        fade_samples = int(0.2 * self.sample_rate)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return combined * envelope
    
    def generate_rail_joint_clicks(self, duration: float, interval: float = 0.8, 
                                   amplitude: float = 0.15) -> np.ndarray:
        """
        Generate rhythmic rail joint clicking sounds (clickety-clack pattern).
        
        Args:
            duration: Duration in seconds
            interval: Time between clicks in seconds (represents rail segment length/speed)
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        samples = int(self.sample_rate * duration)
        combined = np.zeros(samples)
        
        # Generate clicks at regular intervals
        t = 0
        while t < duration:
            click_pos = int(t * self.sample_rate)
            if click_pos < samples:
                # Each click is a short percussive sound - two-part for realism
                # First part: sharp metallic click
                click_duration = 0.02  # 20ms
                click1 = self.generate_tone(1200, click_duration, amplitude * 0.8)
                click1_envelope = np.exp(-50 * np.linspace(0, 1, len(click1)))
                click1 = click1 * click1_envelope
                
                # Second part: lower resonance
                click2 = self.generate_tone(450, click_duration * 1.5, amplitude * 0.5)
                click2_envelope = np.exp(-30 * np.linspace(0, 1, len(click2)))
                click2 = click2 * click2_envelope
                
                # Add both parts with slight offset
                end_pos1 = min(click_pos + len(click1), samples)
                combined[click_pos:end_pos1] += click1[:end_pos1 - click_pos]
                
                offset = int(0.005 * self.sample_rate)  # 5ms offset
                click_pos2 = click_pos + offset
                end_pos2 = min(click_pos2 + len(click2), samples)
                if click_pos2 < samples:
                    combined[click_pos2:end_pos2] += click2[:end_pos2 - click_pos2]
            
            # Add slight randomness to interval for realism
            t += interval * random.uniform(0.95, 1.05)
        
        return combined
    
    def generate_brake_squeal(self, duration: float = 1.0, amplitude: float = 0.25) -> np.ndarray:
        """
        Generate brake squeal sound (high-frequency brake pad vibration).
        
        Args:
            duration: Duration in seconds
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # High-frequency squeal from brake pad resonance
        squeal_freq = random.uniform(2500, 4000)  # Typical brake squeal frequency
        squeal = self.generate_tone(squeal_freq, duration, amplitude)
        
        # Add frequency modulation for realistic brake squeal character
        modulation_freq = random.uniform(8, 15)  # Wobble in the squeal
        freq_mod = 1 + 0.05 * np.sin(2 * np.pi * modulation_freq * t)
        squeal = squeal * freq_mod
        
        # Add harmonics
        harmonic2 = self.generate_tone(squeal_freq * 1.5, duration, amplitude * 0.3)
        squeal[:len(harmonic2)] += harmonic2
        
        # Apply amplitude modulation (squeal often pulsates)
        amp_modulation = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 3 * t))
        squeal = squeal * amp_modulation
        
        # Apply envelope
        envelope = np.ones(samples)
        fade_in = int(0.15 * self.sample_rate)
        fade_out = int(0.2 * self.sample_rate)
        envelope[:fade_in] = np.linspace(0, 1, fade_in)
        envelope[-fade_out:] = np.linspace(1, 0, fade_out)
        
        return squeal * envelope
    
    def generate_low_speed_grinding(self, duration: float = 1.0, amplitude: float = 0.18) -> np.ndarray:
        """
        Generate low-speed wheel-rail grinding sound.
        
        Args:
            duration: Duration in seconds
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Low-frequency grinding from slow wheel rotation
        grind1 = self.generate_sweep(150, 300, duration, amplitude * 0.5)
        grind2 = self.generate_sweep(200, 400, duration, amplitude * 0.4)
        
        # Add roughness texture
        roughness = self.generate_noise(duration, amplitude * 0.3, low_freq=100, high_freq=800)
        
        # Rhythmic component for wheel rotation at low speed
        rotation_freq = 2.5  # ~2.5 Hz rotation at low speed
        rotation_pattern = 1 + 0.3 * np.sin(2 * np.pi * rotation_freq * t)
        
        combined = np.zeros(samples)
        combined[:len(grind1)] += grind1
        combined[:len(grind2)] += grind2
        combined[:len(roughness)] += roughness
        combined = combined * rotation_pattern
        
        return combined
    
    def generate_wheel_slip(self, duration: float = 0.5, amplitude: float = 0.3) -> np.ndarray:
        """
        Generate wheel slip sound (momentary loss of traction).
        
        Args:
            duration: Duration in seconds
            amplitude: Volume level
            
        Returns:
            Audio samples as numpy array
        """
        samples = int(self.sample_rate * duration)
        
        # High-pitched squealing from slipping wheel
        slip_squeal = self.generate_sweep(800, 1500, duration, amplitude * 0.7)
        
        # Add rapid frequency modulation for spinning effect
        t = np.linspace(0, duration, samples, False)
        spin_mod = 1 + 0.15 * np.sin(2 * np.pi * 30 * t)  # Rapid modulation
        slip_squeal = slip_squeal * spin_mod
        
        # Add some grinding noise
        grinding = self.generate_noise(duration, amplitude * 0.4, low_freq=300, high_freq=1500)
        
        combined = np.zeros(samples)
        combined[:len(slip_squeal)] += slip_squeal
        combined[:len(grinding)] += grinding
        
        # Sharp attack and quick decay
        envelope = np.exp(-3 * np.linspace(0, 1, samples))
        
        return combined * envelope

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
        Generate and play continuous ambient metro rumble with electric motor background.
        
        Args:
            duration: Duration in seconds
        """
        print("  🚇⚡ Cruising smoothly (continuous motor hum)...")
        # Low frequency rumble with some variation
        rumble = self.generate_noise(duration, amplitude=0.12, low_freq=40, high_freq=150)
        
        # Add multiple periodic vibrations for realism
        t = np.linspace(0, duration, len(rumble), False)
        
        # Primary track vibration at ~8 Hz
        vibration1 = 0.04 * np.sin(2 * np.pi * 8 * t)
        # Secondary harmonic at ~3 Hz for wheel rhythm
        vibration2 = 0.03 * np.sin(2 * np.pi * 3 * t)
        # Add slight random variation to simulate real track irregularities
        variation = 1 + vibration1 + vibration2 + 0.02 * np.random.uniform(-1, 1, len(t))
        
        rumble = rumble * variation
        
        # Add constant electric motor hum in background (more stable frequency)
        motor_freq = random.uniform(450, 550)
        motor_hum = self.generate_tone(motor_freq, duration, amplitude=0.08)
        
        # Add second harmonic for richer motor sound
        motor_freq2 = motor_freq * 1.5
        motor_hum2 = self.generate_tone(motor_freq2, duration, amplitude=0.04)
        
        # Slight inverter noise (less prominent for smoother sound)
        inverter_noise = self.generate_noise(duration, amplitude=0.03, low_freq=4000, high_freq=7000)
        
        # Add enhanced wheel-rail contact sounds
        rail_contact = self.generate_noise(duration, amplitude=0.06, low_freq=800, high_freq=2000)
        
        # Add rail joint clicks (clickety-clack) - speed-dependent interval
        speed_factor = random.uniform(0.7, 1.0)  # Simulates different speeds
        rail_clicks = self.generate_rail_joint_clicks(duration, interval=0.8 * speed_factor, amplitude=0.12)
        
        combined = rumble + motor_hum + motor_hum2 + inverter_noise + rail_contact
        combined[:len(rail_clicks)] += rail_clicks
        
        # Apply gentle fade in/out for smoother transitions
        fade_samples = int(0.5 * self.sample_rate)  # 500ms fade
        if len(combined) > 2 * fade_samples:
            fade_in = np.linspace(0.7, 1.0, fade_samples)
            fade_out = np.linspace(1.0, 0.7, fade_samples)
            combined[:fade_samples] *= fade_in
            combined[-fade_samples:] *= fade_out
        
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def turn_screech(self):
        """Generate and play a turn screeching sound (kept for backward compatibility)."""
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
    
    def gentle_curve(self, duration: float = 2.5):
        """Generate a gentle curve sound without harsh screeching."""
        print("  🔄 Taking a gentle curve...")
        
        # Subtle pitch change in motor
        motor_sweep = self.generate_sweep(500, 600, duration, amplitude=0.10)
        
        # Slight increase in rumble
        rumble = self.generate_noise(duration, amplitude=0.13, low_freq=40, high_freq=180)
        
        # Wheel-rail contact change (mild)
        rail_sound = self.generate_sweep(700, 850, duration, amplitude=0.08)
        
        # Add subtle wheel flange contact sound (not full squeal, just light contact)
        flange_contact = self.generate_noise(duration, amplitude=0.06, low_freq=900, high_freq=1500)
        
        # Sometimes add a light flange squeal for tighter curves (30% chance)
        if random.random() < 0.3:
            squeal_duration = duration * 0.6  # Squeal for part of the curve
            flange_squeal = self.generate_wheel_flange_squeal(squeal_duration, amplitude=0.18)
            # Position squeal in middle of curve
            squeal_start = int((duration - squeal_duration) * 0.5 * self.sample_rate)
            
        combined = motor_sweep + rumble + rail_sound + flange_contact
        
        # Add squeal if generated
        if random.random() < 0.3:
            squeal_duration = duration * 0.6
            flange_squeal = self.generate_wheel_flange_squeal(squeal_duration, amplitude=0.18)
            squeal_start = int((duration - squeal_duration) * 0.5 * self.sample_rate)
            squeal_end = min(squeal_start + len(flange_squeal), len(combined))
            combined[squeal_start:squeal_end] += flange_squeal[:squeal_end - squeal_start]
        
        # Smooth envelope
        samples = len(combined)
        envelope = np.ones(samples)
        fade_len = int(0.3 * self.sample_rate)
        envelope[:fade_len] = np.linspace(0.8, 1.0, fade_len)
        envelope[-fade_len:] = np.linspace(1.0, 0.8, fade_len)
        combined = combined * envelope
        
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def door_closing(self):
        """Generate and play realistic door closing sequence with compressed air system."""
        print("  🚪 Doors closing (warning chime)...")
        
        # Warning chime - more melodic and less harsh
        beep_freq = 800
        for i in range(3):
            beep = self.generate_tone(beep_freq, 0.18, amplitude=0.22)
            # Add slight fade to beeps
            fade = np.linspace(1.0, 0.3, len(beep))
            beep = beep * fade
            self.play_sound(beep, blocking=True)
            time.sleep(0.12)
        
        time.sleep(0.25)
        
        # Compressed air system activation and door movement
        print("  💨 Air system engaging - doors closing smoothly...")
        
        # Initial air pressure release as doors unlock (softer)
        air_release = self.generate_compressed_air_release(0.35, amplitude=0.20)
        self.play_sound(air_release, blocking=True)
        
        # Door motor sound during closing - smoother operation
        time.sleep(0.08)
        door_motor = self.generate_sweep(210, 145, 1.0, amplitude=0.13)
        
        # Continuous air hiss during movement (quieter, more controlled)
        hiss = self.generate_noise(1.0, amplitude=0.12, low_freq=2000, high_freq=6500)
        
        # Add door mechanism sounds
        mechanism = self.generate_noise(1.0, amplitude=0.08, low_freq=150, high_freq=400)
        
        door_sound = door_motor + hiss[:len(door_motor)] + mechanism[:len(door_motor)]
        
        # Apply envelope for smooth operation
        envelope = np.ones(len(door_sound))
        fade_in = int(0.1 * self.sample_rate)
        fade_out = int(0.15 * self.sample_rate)
        envelope[:fade_in] = np.linspace(0.3, 1.0, fade_in)
        envelope[-fade_out:] = np.linspace(1.0, 0.5, fade_out)
        door_sound = door_sound * envelope
        
        self.play_sound(door_sound, blocking=True)
        
        # Final air pressure equalization and gentle door seal
        time.sleep(0.08)
        final_air = self.generate_compressed_air_release(0.4, amplitude=0.15)
        # Softer thunk - sealed, not slammed
        thunk = self.generate_tone(145, 0.12, amplitude=0.30)
        thunk_envelope = np.exp(-10 * np.linspace(0, 1, len(thunk)))
        thunk = thunk * thunk_envelope
        
        combined = np.concatenate([final_air, thunk])
        self.play_sound(combined, blocking=True)
    
    def acceleration(self, duration: float = 3.0):
        """
        Simulate gradual, realistic electric metro acceleration with smooth power delivery.
        
        Args:
            duration: Duration in seconds
        """
        print("  🚀⚡ Smoothly accelerating (electric traction motors)...")
        # Base rumble from wheels - starts quiet, gets louder
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Gradual amplitude increase for rumble
        rumble_envelope = np.clip(t / duration, 0.3, 1.0)
        base_rumble = self.generate_noise(duration, amplitude=0.11)
        base_rumble = base_rumble * rumble_envelope
        
        # Electric traction motor whine with gradual power increase
        # Start from idle, ramp up to cruising speed
        motor_whine = self.generate_electric_motor_whine(duration, 250, 850, amplitude=0.16)
        
        # Add progressive motor load (more harmonics as speed increases)
        motor_harmonic = self.generate_sweep(500, 1700, duration, amplitude=0.06)
        motor_harmonic = motor_harmonic * rumble_envelope
        
        # Power inverter sound - stronger at beginning (startup surge)
        inverter_duration = duration * 0.5
        inverter = self.generate_inverter_sound(inverter_duration, amplitude=0.10)
        inverter_envelope = np.exp(-2 * np.linspace(0, 1, len(inverter)))
        inverter = inverter * inverter_envelope
        
        # Add track sounds that increase with speed
        track_noise = self.generate_noise(duration, amplitude=0.07, low_freq=200, high_freq=1500)
        track_noise = track_noise * rumble_envelope
        
        # Add low-speed grinding at the start
        grind_duration = min(1.0, duration * 0.35)
        low_speed_grind = self.generate_low_speed_grinding(grind_duration, amplitude=0.15)
        
        # Occasionally add wheel slip during heavy acceleration (20% chance)
        add_slip = random.random() < 0.2
        if add_slip:
            slip_time = random.uniform(0.3, 0.8)  # Slip occurs early in acceleration
            slip_pos = int(slip_time * self.sample_rate)
            wheel_slip = self.generate_wheel_slip(0.5, amplitude=0.25)
        
        # Combine all sounds
        combined = np.zeros(samples)
        combined += base_rumble[:samples]
        combined += motor_whine[:samples]
        combined += motor_harmonic[:samples]
        combined[:len(inverter)] += inverter
        combined += track_noise[:samples]
        combined[:len(low_speed_grind)] += low_speed_grind
        
        # Add wheel slip if triggered
        if add_slip and slip_pos < samples:
            slip_end = min(slip_pos + len(wheel_slip), samples)
            combined[slip_pos:slip_end] += wheel_slip[:slip_end - slip_pos]
        
        # Smooth fade in at start
        fade_in_samples = int(0.3 * self.sample_rate)
        combined[:fade_in_samples] *= np.linspace(0.5, 1.0, fade_in_samples)
        
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def deceleration(self, duration: float = 2.5):
        """
        Simulate gradual, realistic metro deceleration with regenerative braking and air brakes.
        
        Args:
            duration: Duration in seconds
        """
        print("  🛑💨 Gradually slowing down (regenerative + air brakes)...")
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Gradual amplitude decrease for rumble as speed decreases
        decel_envelope = np.clip(1.0 - (t / duration) * 0.7, 0.3, 1.0)
        decel_rumble = self.generate_noise(duration, amplitude=0.13)
        decel_rumble = decel_rumble * decel_envelope
        
        # Electric motor regenerative braking (falling pitch) - smooth power curve
        motor_whine = self.generate_electric_motor_whine(duration, 850, 200, amplitude=0.14)
        
        # Add motor harmonics that fade out
        motor_harmonic = self.generate_sweep(1700, 400, duration, amplitude=0.05)
        motor_harmonic = motor_harmonic * decel_envelope
        
        # Air brake engagement sound - gradual application
        brake_start = duration * 0.2  # Brakes engage 20% into deceleration
        brake_duration = duration * 0.7
        air_brake = self.generate_compressed_air_release(brake_duration, amplitude=0.18)
        
        # Enhanced brake pad friction sound - increases as brakes are applied
        friction_sound = self.generate_noise(duration, amplitude=0.09, low_freq=100, high_freq=400)
        friction_envelope = np.clip((t / duration) * 1.5, 0.2, 1.0)
        friction_sound = friction_sound * friction_envelope
        
        # Track noise decreasing with speed
        track_noise = self.generate_noise(duration, amplitude=0.06, low_freq=300, high_freq=1200)
        track_noise = track_noise * decel_envelope
        
        # Add low-speed grinding at the end
        grind_start = duration * 0.7  # Grinding becomes more audible at low speed
        grind_duration = duration * 0.3
        low_speed_grind = self.generate_low_speed_grinding(grind_duration, amplitude=0.14)
        
        # Occasionally add brake squeal (25% chance)
        add_squeal = random.random() < 0.25
        if add_squeal:
            squeal_start_time = random.uniform(0.3, 0.6)  # Squeal occurs mid-braking
            squeal_pos = int(squeal_start_time * self.sample_rate)
            brake_squeal_sound = self.generate_brake_squeal(1.0, amplitude=0.20)
        
        # Combine all sounds
        combined = np.zeros(samples)
        combined += decel_rumble[:samples]
        combined += motor_whine[:samples]
        combined += motor_harmonic[:samples]
        
        # Add air brake starting partway through
        brake_start_sample = int(brake_start * self.sample_rate)
        combined[brake_start_sample:brake_start_sample+len(air_brake)] += air_brake
        
        combined += friction_sound[:samples]
        combined += track_noise[:samples]
        
        # Add low-speed grinding at the end
        grind_start_sample = int(grind_start * self.sample_rate)
        grind_end = min(grind_start_sample + len(low_speed_grind), samples)
        combined[grind_start_sample:grind_end] += low_speed_grind[:grind_end - grind_start_sample]
        
        # Add brake squeal if triggered
        if add_squeal and squeal_pos < samples:
            squeal_end = min(squeal_pos + len(brake_squeal_sound), samples)
            combined[squeal_pos:squeal_end] += brake_squeal_sound[:squeal_end - squeal_pos]
        
        # Smooth fade out at end
        fade_out_samples = int(0.5 * self.sample_rate)
        combined[-fade_out_samples:] *= np.linspace(1.0, 0.3, fade_out_samples)
        
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    
    def electric_idle(self, duration: float = 1.0):
        """
        Generate realistic electric system idle sound when stopped at station.
        
        Args:
            duration: Duration in seconds
        """
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Main power supply hum (50/60 Hz and harmonics)
        aux_hum = self.generate_tone(120, duration, amplitude=0.07)  # 120 Hz hum
        aux_hum += self.generate_tone(60, duration, amplitude=0.04)  # 60 Hz base
        aux_hum += self.generate_tone(180, duration, amplitude=0.03)  # 180 Hz harmonic
        
        # Air compressor with realistic cycling (turns on/off)
        compressor_freq = 180
        # Create a pulsing envelope for compressor cycling
        compressor_cycle = 0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t)  # ~3 second cycle
        compressor = self.generate_tone(compressor_freq, duration, amplitude=0.06)
        compressor = compressor * compressor_cycle
        
        # Cooling fans (varies slightly)
        fan_freq = random.uniform(90, 110)
        fan_sound = self.generate_tone(fan_freq, duration, amplitude=0.05)
        fan_noise = self.generate_noise(duration, amplitude=0.03, low_freq=80, high_freq=300)
        
        # High frequency inverter standby with slight modulation
        inverter_idle = self.generate_noise(duration, amplitude=0.035, low_freq=3000, high_freq=5000)
        inverter_modulation = 1 + 0.1 * np.sin(2 * np.pi * 120 * t)
        inverter_idle = inverter_idle * inverter_modulation
        
        # Occasional relay clicks and system sounds
        relay_sound = np.zeros(samples)
        num_relays = random.randint(1, 3)
        for _ in range(num_relays):
            relay_pos = random.randint(0, samples - 1000)
            click = self.generate_tone(800, 0.02, amplitude=0.15)
            relay_sound[relay_pos:relay_pos+len(click)] += click
        
        combined = aux_hum + compressor + fan_sound + fan_noise + inverter_idle + relay_sound
        
        # Smooth transitions
        fade_samples = int(0.2 * self.sample_rate)
        combined[:fade_samples] *= np.linspace(0.5, 1.0, fade_samples)
        combined[-fade_samples:] *= np.linspace(1.0, 0.5, fade_samples)
        
        self.play_sound(combined, blocking=False)
        time.sleep(duration)
    

    
    def continuous_journey_segment(self, duration: float):
        """
        Generate a continuous journey segment with smooth, realistic transitions.
        
        Args:
            duration: Duration of the segment in seconds
        """
        # Continuous cruising with seamless variations
        elapsed = 0
        while elapsed < duration:
            # Longer rumble duration for more continuous feel
            rumble_duration = min(random.uniform(10.0, 18.0), duration - elapsed)
            self.ambient_rumble(rumble_duration)
            elapsed += rumble_duration
            
            # Occasionally add a gentle curve (realistic metro routes have curves)
            if elapsed < duration - 3.0 and random.random() < 0.25:
                turn_duration = random.uniform(2.5, 4.0)
                remaining = duration - elapsed
                if remaining >= turn_duration:
                    self.gentle_curve(turn_duration)
                    elapsed += turn_duration
    
    def station_departure_sequence(self):
        """Execute a complete station departure sequence."""
        print("\n📍 At station - preparing to depart...")
        
        # Doors close
        self.door_closing()
        time.sleep(0.3)
        
        # Gradual acceleration
        print("  🚀⚡ Departing station (gradual acceleration)...")
        self.acceleration(4.0)
    
    def station_arrival_sequence(self):
        """Execute a complete station arrival sequence."""
        print("\n📍 Station ahead - preparing to stop...")
        
        # Gradual deceleration
        self.deceleration(3.5)
        time.sleep(0.3)
        
        # Stop at station with idle sounds
        print("  ⏸️  Arrived at station (electric systems humming)...")
        self.electric_idle(2.0)
    
    def run_simulation(self, duration_minutes: float = 2.0):
        """
        Run a realistic metro sound simulation with continuous, logical sound progression.
        
        Args:
            duration_minutes: How long to run the simulation in minutes
        """
        print("\n" + "="*60)
        print("🚇 REALISTIC METRO JOURNEY SIMULATOR 🚇")
        print("="*60)
        print(f"Starting {duration_minutes}-minute realistic metro journey...\n")
        print("🎵 Continuous ambient sounds with logical transitions\n")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        self.is_running = True
        
        try:
            # Start journey: departure from initial station
            self.station_departure_sequence()
            
            while time.time() < end_time and self.is_running:
                remaining_time = end_time - time.time()
                
                # Need at least 15 seconds for a station stop cycle
                if remaining_time < 15:
                    # Just cruise until time runs out
                    self.continuous_journey_segment(remaining_time)
                    break
                
                # Typical inter-station journey: 25-45 seconds of cruising
                cruise_duration = min(random.uniform(25.0, 45.0), remaining_time - 10)
                
                print(f"\n🚇 Cruising to next station...")
                self.continuous_journey_segment(cruise_duration)
                
                # Check if we have time for station stop
                remaining_time = end_time - time.time()
                if remaining_time >= 10:
                    # Arrive at station
                    self.station_arrival_sequence()
                    
                    # Check if we should depart (need time for departure)
                    remaining_time = end_time - time.time()
                    if remaining_time >= 5:
                        self.station_departure_sequence()
                    else:
                        print("\n🏁 Journey ending at station...")
                        break
        
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
