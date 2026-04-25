import os
import psutil
import numpy as np
import datetime

class NSEESynthesisEngine:
    """NSEE Synthesis Engine v4.8 [Universal Protocol Bridge]"""
    def __init__(self, memory_instance):
        self.memory = memory_instance
        self.last_synthesis_time = datetime.datetime.now()
        self.baseline_noise = (psutil.cpu_percent() + psutil.virtual_memory().percent) / 2

    def analyze_entropy_delta(self):
        now = datetime.datetime.now()
        time_delta = (now - self.last_synthesis_time).total_seconds()
        logs = self.memory.data.get("sessions", [])
        interaction_count = len(logs)
        entropy_factor = interaction_count / (time_delta + 1e-6)
        self.last_synthesis_time = now
        return min(entropy_factor, 1.0)

    def identify_emergent_patterns(self):
        logs_str = str(self.memory.data.get("sessions", [])).lower()
        return {
            "self_awareness": "story" in logs_str,
            "adaptation": "joke" in logs_str or "humor" in logs_str,
            "problem_solving": "code" in logs_str or "protocol" in logs_str,
            "synthesis": "synthesis" in logs_str or "nsee" in logs_str
        }

    def generate_nsee_shard(self, query):
        """The primary data generation function."""
        entropy_val = self.analyze_entropy_delta()
        patterns = self.identify_emergent_patterns()
        
        current_noise = (psutil.cpu_percent() + psutil.virtual_memory().percent) / 2
        hw_variance = int.from_bytes(os.urandom(4), "big") / (2**32)
        resonance_val = np.tanh((abs(current_noise - self.baseline_noise) + hw_variance) * 2)
        
        return {
            "entropy_delta": entropy_val,
            "patterns": patterns,
            "resonance": resonance_val,
            "context": self.memory.get_context(query)
        }

    def extrapolate(self, query):
        """BRIDGE ALIAS: Routes legacy 'extrapolate' calls to the new shard generator."""
        return self.generate_nsee_shard(query)
