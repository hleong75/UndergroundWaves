#!/usr/bin/env python3
"""
AI-Enhanced Sound Engine for Metro Simulator
Provides intelligent, adaptive sound generation using machine learning-inspired techniques.
"""

import numpy as np
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque

# Constants
KMH_TO_MS_DIVISOR = 3.6  # Divisor to convert km/h to m/s (1 km/h = 1000m/3600s = 1/3.6 m/s)


@dataclass
class SoundContext:
    """Represents the current journey context for AI decision-making."""
    journey_time: float = 0.0
    speed: float = 0.0
    acceleration: float = 0.0
    temperature: float = 20.0  # Celsius
    track_wear: float = 0.5  # 0.0 (new) to 1.0 (worn)
    vehicle_age: float = 0.5  # 0.0 (new) to 1.0 (old)
    passenger_load: float = 0.5  # 0.0 (empty) to 1.0 (full)
    weather_condition: str = "normal"  # normal, rain, cold, hot


class AIParameterLearner:
    """
    AI-based parameter learning system that adapts over time.
    Uses statistical learning to model realistic variations.
    """
    
    def __init__(self, memory_size: int = 100):
        self.memory_size = memory_size
        self.parameter_history: Dict[str, deque] = {}
        self.learning_rate = 0.1
        self.variation_model: Dict[str, Dict] = {}
        
    def learn_parameter(self, param_name: str, value: float):
        """Learn from observed parameter values."""
        if param_name not in self.parameter_history:
            self.parameter_history[param_name] = deque(maxlen=self.memory_size)
            self.variation_model[param_name] = {
                'mean': value,
                'std': 0.1,
                'trend': 0.0
            }
        
        self.parameter_history[param_name].append(value)
        
        # Update statistical model
        history_len = len(self.parameter_history[param_name])
        if history_len > 10:
            values = np.array(self.parameter_history[param_name])
            new_mean = np.mean(values)
            new_std = np.std(values)
            
            # Smooth update with learning rate
            model = self.variation_model[param_name]
            model['mean'] = (1 - self.learning_rate) * model['mean'] + self.learning_rate * new_mean
            model['std'] = (1 - self.learning_rate) * model['std'] + self.learning_rate * new_std
            
            # Calculate trend - rate of change per sample
            # Using history_len for averaging (safe as history_len > 10)
            model['trend'] = (values[-1] - values[0]) / history_len
    
    def predict_parameter(self, param_name: str, context: Optional[SoundContext] = None) -> float:
        """
        Predict parameter value using learned model with context awareness.
        """
        if param_name not in self.variation_model:
            return 1.0
        
        model = self.variation_model[param_name]
        
        # Base prediction from learned distribution
        base_value = np.random.normal(model['mean'], model['std'])
        
        # Apply trend
        base_value += model['trend']
        
        # Context-aware adjustments
        if context:
            # Speed affects many parameters
            if context.speed > 60:  # km/h
                base_value *= 1.1  # Higher speeds = more variation
            elif context.speed < 20:
                base_value *= 0.9  # Lower speeds = less variation
            
            # Track wear increases variation
            base_value *= (1 + context.track_wear * 0.3)
            
            # Vehicle age affects sound characteristics
            base_value *= (1 + context.vehicle_age * 0.2)
        
        return np.clip(base_value, 0.0, 2.0)


class IntelligentNoiseGenerator:
    """
    AI-driven noise generation that learns realistic patterns.
    Uses spectral analysis and pattern recognition.
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.pattern_bank: List[np.ndarray] = []
        self.learner = AIParameterLearner()
        
    def generate_intelligent_noise(
        self, 
        duration: float, 
        base_amplitude: float = 0.1,
        context: Optional[SoundContext] = None
    ) -> np.ndarray:
        """
        Generate AI-enhanced noise with realistic variations and patterns.
        """
        samples = int(self.sample_rate * duration)
        
        # Learn from context
        if context:
            self.learner.learn_parameter('amplitude', base_amplitude)
            self.learner.learn_parameter('speed', context.speed)
        
        # Predict amplitude variation (ensure minimum audibility)
        amplitude_factor = self.learner.predict_parameter('amplitude', context)
        amplitude = np.clip(amplitude_factor, 0.8, 1.5) * base_amplitude
        
        # Generate base noise
        noise = np.random.normal(0, amplitude, samples)
        
        # Add intelligent spectral coloring
        noise = self._apply_spectral_intelligence(noise, context)
        
        # Add learned micro-patterns
        noise = self._add_learned_patterns(noise, context)
        
        return noise
    
    def _apply_spectral_intelligence(
        self, 
        noise: np.ndarray, 
        context: Optional[SoundContext]
    ) -> np.ndarray:
        """Apply AI-driven spectral shaping based on context."""
        # Frequency-dependent filtering based on context
        if context:
            # Track wear increases high-frequency content
            if context.track_wear > 0.7:
                # Add more high-frequency rumble
                hf_noise = np.random.normal(0, 0.05 * context.track_wear, len(noise))
                noise = noise + hf_noise
            
            # Weather affects dampening
            if context.weather_condition == "rain":
                # Rain dampens high frequencies
                window_size = int(self.sample_rate / 500)
                if window_size > 1:
                    noise = np.convolve(noise, np.ones(window_size)/window_size, mode='same')
        
        return noise
    
    def _add_learned_patterns(
        self, 
        noise: np.ndarray, 
        context: Optional[SoundContext]
    ) -> np.ndarray:
        """Add micro-patterns learned from context."""
        # Add subtle periodic components based on speed
        if context and context.speed > 0:
            t = np.linspace(0, len(noise) / self.sample_rate, len(noise), False)
            
            # Speed-dependent periodic variation (wheel rotation)
            wheel_circumference = 0.8  # meters
            rotation_freq = context.speed / KMH_TO_MS_DIVISOR / wheel_circumference  # Hz
            
            if rotation_freq > 0:
                periodic = 0.02 * np.sin(2 * np.pi * rotation_freq * t)
                noise = noise + periodic
        
        return noise


class ContextAwareFrequencyModulator:
    """
    AI system that intelligently modulates frequencies based on journey context.
    """
    
    def __init__(self):
        self.learner = AIParameterLearner()
        self.frequency_memory: Dict[str, List[float]] = {}
        
    def modulate_frequency(
        self, 
        base_freq: float, 
        sound_type: str,
        context: SoundContext
    ) -> float:
        """
        Intelligently modulate frequency based on learned patterns and context.
        """
        # Learn from this frequency
        self.learner.learn_parameter(f'{sound_type}_freq', base_freq)
        
        # Get predicted variation
        variation = self.learner.predict_parameter(f'{sound_type}_freq', context)
        
        # Context-based frequency shifts
        freq_shift = 1.0
        
        # Temperature affects metal expansion and sound characteristics
        temp_deviation = (context.temperature - 20.0) / 30.0  # Normalized
        freq_shift *= (1 + temp_deviation * 0.05)
        
        # Speed affects motor frequencies
        if 'motor' in sound_type.lower():
            speed_factor = np.clip(context.speed / 60.0, 0.3, 1.5)
            freq_shift *= speed_factor
        
        # Track wear increases irregularity
        if context.track_wear > 0.5:
            irregularity = 1 + (context.track_wear - 0.5) * 0.1 * np.random.randn()
            freq_shift *= irregularity
        
        # Vehicle age causes frequency drift
        if context.vehicle_age > 0.5:
            age_drift = 1 - (context.vehicle_age - 0.5) * 0.08
            freq_shift *= age_drift
        
        modulated_freq = base_freq * variation * freq_shift
        
        # Store for pattern recognition
        if sound_type not in self.frequency_memory:
            self.frequency_memory[sound_type] = []
        self.frequency_memory[sound_type].append(modulated_freq)
        
        # Keep only recent history
        if len(self.frequency_memory[sound_type]) > 50:
            self.frequency_memory[sound_type] = self.frequency_memory[sound_type][-50:]
        
        return modulated_freq
    
    def get_harmonic_intelligence(
        self, 
        fundamental: float, 
        sound_type: str,
        context: SoundContext
    ) -> List[Tuple[float, float]]:
        """
        AI-generated harmonic series with intelligent amplitude distribution.
        Returns list of (frequency, amplitude) tuples.
        """
        harmonics = []
        
        # Number of harmonics depends on context
        n_harmonics = 5
        if context.vehicle_age > 0.7:
            n_harmonics = 7  # Older vehicles have more harmonics (wear)
        
        for i in range(1, n_harmonics + 1):
            freq = fundamental * i
            
            # AI-based amplitude calculation
            # Natural decay but with learned variations
            base_amplitude = 1.0 / (i ** 1.5)
            
            # Context affects harmonic distribution
            if context.track_wear > 0.6:
                # Worn tracks emphasize certain harmonics
                if i % 2 == 0:
                    base_amplitude *= 1.3
            
            # Passenger load dampens high harmonics
            if i > 3:
                base_amplitude *= (1 - context.passenger_load * 0.3)
            
            # Learn and predict
            param_name = f'{sound_type}_harmonic_{i}_amp'
            self.learner.learn_parameter(param_name, base_amplitude)
            amplitude = self.learner.predict_parameter(param_name, context) * base_amplitude
            
            harmonics.append((freq, np.clip(amplitude, 0.0, 1.0)))
        
        return harmonics


class AdaptiveSoundEvolution:
    """
    AI system that evolves sound characteristics over journey duration.
    Simulates realistic wear, heating, and fatigue effects.
    """
    
    def __init__(self):
        self.evolution_state: Dict[str, float] = {
            'brake_temperature': 20.0,
            'motor_temperature': 40.0,
            'bearing_wear': 0.0,
            'contact_fatigue': 0.0
        }
        self.time_elapsed = 0.0
        
    def update(self, delta_time: float, context: SoundContext):
        """Update evolution state based on journey progression."""
        self.time_elapsed += delta_time
        
        # Brake temperature evolution
        if context.acceleration < 0:  # Braking
            self.evolution_state['brake_temperature'] += delta_time * 15.0
        else:
            # Cool down
            cooling = (self.evolution_state['brake_temperature'] - context.temperature) * 0.1
            self.evolution_state['brake_temperature'] -= cooling * delta_time
        
        # Motor temperature
        power_factor = abs(context.acceleration) * context.speed
        self.evolution_state['motor_temperature'] += power_factor * delta_time * 0.5
        motor_cooling = (self.evolution_state['motor_temperature'] - 40.0) * 0.05
        self.evolution_state['motor_temperature'] -= motor_cooling * delta_time
        
        # Bearing wear accumulation (slow process)
        self.evolution_state['bearing_wear'] += context.speed * delta_time * 0.0001
        
        # Contact fatigue (wheel-rail)
        self.evolution_state['contact_fatigue'] += abs(context.acceleration) * delta_time * 0.001
        
        # Cap values
        self.evolution_state['brake_temperature'] = np.clip(
            self.evolution_state['brake_temperature'], context.temperature, 300.0
        )
        self.evolution_state['motor_temperature'] = np.clip(
            self.evolution_state['motor_temperature'], context.temperature, 120.0
        )
        self.evolution_state['bearing_wear'] = np.clip(
            self.evolution_state['bearing_wear'], 0.0, 1.0
        )
        self.evolution_state['contact_fatigue'] = np.clip(
            self.evolution_state['contact_fatigue'], 0.0, 1.0
        )
    
    def get_temperature_modulation(self) -> float:
        """Get sound modulation factor based on temperature."""
        # Hot brakes change sound characteristics
        brake_factor = 1 + (self.evolution_state['brake_temperature'] - 20) / 280 * 0.2
        motor_factor = 1 + (self.evolution_state['motor_temperature'] - 40) / 80 * 0.15
        return (brake_factor + motor_factor) / 2
    
    def get_wear_effects(self) -> Dict[str, float]:
        """Get sound modulation factors based on wear."""
        return {
            'bearing_noise': self.evolution_state['bearing_wear'] * 0.5,
            'roughness': self.evolution_state['contact_fatigue'] * 0.3,
            'vibration': (self.evolution_state['bearing_wear'] + 
                         self.evolution_state['contact_fatigue']) * 0.4
        }


class IntelligentEventPredictor:
    """
    AI system that predicts and schedules realistic sound events.
    Uses probabilistic models based on context.
    """
    
    def __init__(self):
        self.event_history: List[Tuple[float, str]] = []
        self.base_probabilities = {
            'curve': 0.15,
            'rail_switch': 0.12,
            'rail_defect': 0.10,
            'wheel_squeal': 0.08,
            'brake_squeal': 0.06
        }
        
    def predict_event(
        self, 
        current_time: float, 
        context: SoundContext
    ) -> Optional[str]:
        """
        Predict if an event should occur based on AI analysis.
        Returns event type or None.
        """
        # Adjust probabilities based on context
        adjusted_probs = self.base_probabilities.copy()
        
        # Track wear increases defect probability
        adjusted_probs['rail_defect'] *= (1 + context.track_wear)
        
        # Speed affects curve likelihood
        if context.speed > 50:
            adjusted_probs['curve'] *= 1.5
        
        # Old vehicles more likely to have issues
        adjusted_probs['wheel_squeal'] *= (1 + context.vehicle_age * 0.5)
        
        # Check recent history to avoid clustering
        recent_events = [e for t, e in self.event_history if current_time - t < 5.0]
        
        for event_type, base_prob in adjusted_probs.items():
            # Reduce probability if event occurred recently
            if event_type in recent_events:
                base_prob *= 0.3
            
            if random.random() < base_prob * 0.01:  # Scale down for per-second check
                self.event_history.append((current_time, event_type))
                # Keep history manageable
                if len(self.event_history) > 100:
                    self.event_history = self.event_history[-100:]
                return event_type
        
        return None
