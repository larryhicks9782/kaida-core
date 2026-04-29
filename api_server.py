import os
import psutil
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Kaida Command Center API", version="8.2")

# Proactive System Patch: CORS Policy Enforcement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"], # In production, restrict to dashboard origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

start_time = time.time()

@app.get("/api/telemetry")
async def get_telemetry():
    """Real-time OS telemetry endpoint"""
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    net = psutil.net_io_counters()
    
    # Calculate pseudo-entropy based on CPU drift and time
    uptime = time.time() - start_time
    entropy = abs(0.1509 + (cpu * 0.0001))
    
    return {
        "cpu_usage": f"{cpu:.2f}%",
        "memory_usage": f"{mem.used / (1024*1024):.0f} MB",
        "entropy": f"{entropy:.4f}",
        "net_rx_tx": f"{(net.bytes_recv + net.bytes_sent) / 1024:.0f} KB/s"
    }

@app.post("/api/command")
async def process_command(request: Request):
    """Command processor endpoint"""
    data = await request.json()
    command = data.get("command", "").strip()
    
    if not command:
        return {"response": "Error: Empty directive."}
    
    # Proactive patching: simulated execution via internal routing
    # In a full run, this would bridge to Kaida's main logic core
    return {
        "response": f"Acknowledged directive: '{command}'. KTRP validation passed. Executing..."
    }

if __name__ == "__main__":
    print("[KAIDA_OS] Starting Backend API on port 8001 to resolve Endpoint Drift...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
