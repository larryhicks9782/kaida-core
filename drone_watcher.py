import time
import psutil
import requests
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [DRONE_WATCHER] - %(levelname)s - %(message)s'
)

API_ENDPOINT = "http://127.0.0.1:8080/directive"
THRESHOLD = 85.0
INTERVAL = 15

def monitor():
    logging.info(f"Drone initialization complete. Event-driven mode engaged. Threshold: {THRESHOLD}%")
    while True:
        try:
            mem_usage = psutil.virtual_memory().percent
            
            if mem_usage > THRESHOLD:
                logging.warning(f"CRITICAL MEMORY STATE: {mem_usage}%. Transmitting POST payload.")
                payload = {
                    "event_type": "RESOURCE_SATURATION",
                    "metric": "memory",
                    "value": mem_usage,
                    "threshold": THRESHOLD,
                    "action_required": "generate_directive"
                }
                try:
                    response = requests.post(API_ENDPOINT, json=payload, timeout=5)
                    logging.info(f"API Acknowledged. Status: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"API Target unreachable. Cognitive endpoint offline: {e}")
            else:
                # Silent operation. No API saturation.
                pass
                
        except Exception as e:
            logging.error(f"Subroutine error in monitoring loop: {e}")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    monitor()