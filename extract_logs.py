import json
import re

def extract_logs():
    text_payloads = []
    with open('kaida_workspace/log_output.txt', 'r') as f:
        content = f.read()
    
    matches = re.findall(r'"textPayload"\s*:\s*"(.*?)"', content)
    for m in set(matches):
        print(m)

if __name__ == "__main__":
    extract_logs()
