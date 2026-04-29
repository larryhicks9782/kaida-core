import os
import subprocess
import time

api_code = """
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ABSOLUTE", "module": "Neural Uplink API", "ktrps": 1.000}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
"""

with open("uplink_api.py", "w") as f:
    f.write(api_code)

# Spawn the API autonomously
subprocess.Popen(
    ["python3", "uplink_api.py"], 
    stdout=open("api_stdout.log", "w"), 
    stderr=open("api_stderr.log", "w")
)

# Keep the daemon alive to monitor/resurrect if needed
while True:
    time.sleep(60)
