import random
import string

class Node:
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.is_end_of_word = False

class Trie:
    """Kaida's Linguistic Shard Map."""
    def __init__(self):
        self.root = Node(None)

    def insert(self, word):
        """Injects a user string into the memory tree."""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = Node(char)
            current = current.children[char]
        current.is_end_of_word = True

    def get_reconstructed_path(self, max_length=15):
        """Reconstructs a linguistic path from stored shards."""
        word = ''
        current = self.root
        for _ in range(max_length):
            if current.children:
                char = random.choice(list(current.children.keys()))
                word += char
                current = current.children[char]
                if current.is_end_of_word and random.random() > 0.3:
                    break
            else:
                break
        return word if word else "NULL_PATH"

def get_shard_weight(text):
    """Calculates the weight of the linguistic shard."""
    return sum(len(word) for word in text.split())
