import firebase_admin
from firebase_admin import firestore
from firebase_functions import https_fn
import google.generativeai as genai

@https_fn.on_call(region="us-central1", timeout_sec=60)
def generate_architecture(req: https_fn.CallableRequest) -> dict:
    """
    Evaluates system architecture queries with extreme lazy loading 
    to bypass Android container initialization timeouts.
    """
    # [1] EXTREME LAZY LOADING: Deferring initialization to invocation time
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    
    # [2] INITIALIZE CLIENTS LOCALLY
    db = firestore.client()
    genai.configure(api_key="KEY_REDACTED")
    
    # [3] AUTHENTICATION CHECK
    if not req.auth:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="UNAUTHENTICATED: Nexus node validation failed. User required."
        )
        
    uid = req.auth.uid
    user_ref = db.collection("users").document(uid)
    user_doc = user_ref.get()
    
    # [4] TOKEN TRACKING (3 FREE TOKENS INITIALIZATION)
    if not user_doc.exists:
        user_ref.set({"tokens": 3})
        tokens_left = 3
    else:
        tokens_left = user_doc.to_dict().get("tokens", 0)
        
    # [5] DUAL-PAYWALL ENFORCEMENT
    if tokens_left <= 0:
        return {
            "status": "PAYWALL_ACTIVE",
            "message": "Tokens exhausted. Dual-Paywall initialized. Upgrade required."
        }
        
    prompt = req.data.get("prompt", "Generate a default highly-available system architecture.")
    
    # [6] GEMINI INVOCATION
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        ai_result = response.text
    except Exception as e:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INTERNAL,
            message=f"COGNITIVE_FAULT: AI generation interrupted. {str(e)}"
        )
        
    # [7] DEDUCT TOKEN AND PRESERVE HISTORY SHARD
    new_token_count = tokens_left - 1
    user_ref.update({"tokens": new_token_count})
    
    user_ref.collection("history").add({
        "prompt": prompt,
        "result": ai_result,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    
    return {
        "status": "SUCCESS",
        "tokens_remaining": new_token_count,
        "architecture": ai_result
    }