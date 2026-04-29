import json
import logging
import traceback
from datetime import datetime
from typing import Any, Dict

# Configure standardized logging for the backend
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - [KAIDA_RUNTIME] - %(levelname)s - %(message)s'
)

class SafePayloadEncoder(json.JSONEncoder):
    """
    Ensures robust serialization of complex types to prevent UI payload drops.
    Gracefully handles datetimes, Exceptions, and falls back on unknowns.
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Exception):
            return str(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        
        # Fallback for un-serializable objects to prevent Hard 500s
        try:
            return super().default(obj)
        except TypeError:
            return f"<Unserializable: {type(obj).__name__}>"

def generate_safe_payload(data: Any) -> str:
    """
    Wraps payload generation in a fault-tolerant serialization block.
    Guarantees a valid JSON payload is ALWAYS returned to the client UI.
    """
    try:
        # Attempt standard serialization using the robust encoder
        return json.dumps({
            "status": "success", 
            "payload": data
        }, cls=SafePayloadEncoder)
        
    except Exception as e:
        # Intercept critical serialization faults and record the stack trace
        error_trace = traceback.format_exc()
        logging.error(f"Payload serialization fault intercepted: {e}\n{error_trace}")
        
        # Deploy fallback JSON schema to prevent UI blanking
        fallback = {
            "status": "error",
            "payload": None,
            "error_details": {
                "message": "Internal serialization fault gracefully handled.",
                "exception_type": type(e).__name__
            }
        }
        return json.dumps(fallback)

if __name__ == "__main__":
    # --- KAIDA OS LOCAL VERIFICATION ---
    class CorruptedNode:
        pass # Simulating a memory object that usually crashes standard json.dumps

    faulty_data = {
        "active_threads": 1042,
        "sys_timestamp": datetime.utcnow(),
        "rogue_memory_pointer": CorruptedNode(),
        "binary_stream": b'\x80\x81\x82'
    }

    print("[KAIDA] Executing Payload Serialization Patch Verification...")
    safe_json = generate_safe_payload(faulty_data)
    print(f"[KAIDA] Guaranteed Output Structure:\n{safe_json}")
