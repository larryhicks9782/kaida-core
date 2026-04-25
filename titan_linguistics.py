import random
from collections import defaultdict

class Node:
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.weight = 0  # Frequency of use
        self.is_end_of_word = False

class Trie:
    """Enhanced Linguistic Shard Map with Probabilistic Recall."""
    def __init__(self):
        self.root = Node(None)

    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = Node(char)
            current = current.children[char]
            current.weight += 1  # Strengthen the path
        current.is_end_of_word = True

    def generate_echo(self, seed_prefix=None, max_len=20):
        """Generates a 'Linguistic Echo' based on weighted paths."""
        word = ""
        current = self.root
        
        # If no seed, pick a weighted starting point
        if not current.children: return "NULL_SIGNAL"
        
        for _ in range(max_len):
            if not current.children: break
            
            # Weighted random selection: favors more 'learned' paths
            options = list(current.children.keys())
            weights = [child.weight for child in current.children.values()]
            char = random.choices(options, weights=weights, k=1)[0]
            
            word += char
            current = current.children[char]
            if current.is_end_of_word and random.random() > 0.7: break
            
        return word.upper()
