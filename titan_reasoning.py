import json
import pymc as pm
import numpy as np

class ReasoningEngine:
    def __init__(self, brain_instance):
        self.brain = brain_instance
        self.consensus_threshold = 0.88

    def verify_logic_gate(self, scores):
        """Bayesian Consensus: Calculates the probability of truth given auditor scores."""
        try:
            with pm.Model() as consensus_model:
                # Prior: We expect Kaida to be accurate (Beta distribution)
                mu = pm.Beta('mu', alpha=8, beta=2)
                # Likelihood: Scores provided by the 3 internal paths
                obs = pm.Normal('obs', mu=mu, sigma=0.1, observed=scores)
                map_estimate = pm.find_MAP(progressbar=False)
                return map_estimate['mu']
        except:
            return np.mean(scores)

    def get_tot_response(self, user_input, search_context=None):
        """Advanced 3-Path Internal Audit."""
        context_data = "\n".join([f"[SHARD {i}]: {s.get('summary')}" for i, s in enumerate(search_context[:3])])

        audit_prompt = f"""
        [KAIDA PROTOCOL: AUDIT PHASE]
        Live Data: {context_data}
        User Query: {user_input}

        TASK: Generate 3 independent logical paths:
        Path A: Fact Extraction.
        Path B: Contradiction Detection.
        Path C: Contextual Relevance.

        Return ONLY a JSON:
        {{
          "path_a_score": 0.0-1.0,
          "path_b_score": 0.0-1.0,
          "path_c_score": 0.0-1.0,
          "synthesis": "Final technical response"
        }}
        """
        
        raw = self.brain.think(audit_prompt, use_tools=False)
        try:
            # Clean and parse
            clean = raw.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean)
            
            scores = [data['path_a_score'], data['path_b_score'], data['path_c_score']]
            confidence = self.verify_logic_gate(scores)

            if confidence >= self.consensus_threshold:
                return f"{data['synthesis']}\n\n[CONFIDENCE: {confidence:.2f}][BALTIMORE_VERIFIED]"
            else:
                return "CRITICAL: Logic conflict detected in shards. Confidence below Baltimore threshold."
        except:
            return raw
