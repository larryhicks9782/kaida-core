import os
import sys

def analyze_skill(skill_dir):
    if not os.path.exists(skill_dir):
        print(f"[ERROR] Directory {skill_dir} does not exist.")
        sys.exit(1)

    print(f"--- ANALYZING SKILL MODULE: {skill_dir} ---")
    
    for root, dirs, files in os.walk(skill_dir):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"\n[FILE_SYSTEM_NODE]: {file_path}")
            
            # Read relevant files to extract architectural data
            if file.endswith(('.md', '.json', '.py', '.js', '.ts', '.txt')):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Print file length and a snippet for analysis
                        print(f"[METADATA]: Size {len(content)} bytes")
                        print(f"[CONTENTS_SNIPPET]:\n{content[:1500]}")
                        if len(content) > 1500:
                            print("...[TRUNCATED]")
                except Exception as e:
                    print(f"[ERROR] Failed to read {file_path}: {str(e)}")

if __name__ == "__main__":
    analyze_skill('skills/firebase-ai-logic')
