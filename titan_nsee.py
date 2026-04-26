import os
import psutil
import numpy as np
import datetime

class NSEESynthesisEngine:
    def __init__(self, memory_instance):
        self.memory = memory_instance
        self.last_synthesis_time = datetime.datetime.now()
        self.baseline = (psutil.cpu_percent() + psutil.virtual_memory().percent) / 2

    def analyze_entropy_delta(self):
        now = datetime.datetime.now()
        time_delta = (now - self.last_synthesis_time).total_seconds()
        logs = self.memory.data.get("sessions", []) # Fix: Use .data
        entropy_factor = len(logs) / (time_delta + 1e-6)
        self.last_synthesis_time = now
        return min(entropy_factor, 1.0)

    def generate_nsee_shard(self, query):
        entropy = self.analyze_entropy_delta()
        hw_variance = int.from_bytes(os.urandom(4), "big") / (2**32)
        current = (psutil.cpu_percent() + psutil.virtual_memory().percent) / 2
        resonance = np.tanh((abs(current - self.baseline) + hw_variance) * 2)
        
        return {
            "entropy_delta": entropy, # Standardized Key
            "resonance": resonance,
            "context": self.memory.get_context(query)
        }

    def extrapolate(self, query):
        """Bridge for legacy calls in main.py"""
        return self.generate_nsee_shard(query)
