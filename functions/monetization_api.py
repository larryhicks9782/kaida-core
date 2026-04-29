import os
import stripe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# 3.1-Silicon Architecture
# KTRP Absolute Integrity Confirmed
# Dual-Paywall Monetization API

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_placeholder")

app = FastAPI(title="Baltimore Lab Monetization Nexus")

class CheckoutRequest(BaseModel):
    mode: str  # 'subscription' or 'payment'
    customer_email: str | None = None

@app.post("/api/v1/monetization/create-checkout-session")
async def create_checkout_session(req: CheckoutRequest):
    """
    Generates a Stripe Checkout session for the Dual-Paywall architecture.
    Handles both Pay-As-You-Go ($5/credit block) and Premium ($15/mo).
    """
    try:
        if req.mode == "subscription":
            # Fixed $15/mo subscription
            price_id = os.environ.get("STRIPE_PRICE_ID_SUB", "price_15_mo_placeholder")
            checkout_mode = "subscription"
        elif req.mode == "payment":
            # Pay-As-You-Go Credits
            price_id = os.environ.get("STRIPE_PRICE_ID_PAYG", "price_payg_placeholder")
            checkout_mode = "payment"
        else:
            raise HTTPException(status_code=400, detail="Invalid monetization mode selected. Must be 'subscription' or 'payment'.")

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode=checkout_mode,
            success_url=os.environ.get("PAYWALL_SUCCESS_URL", "https://baltimorelab.local/success?session_id={CHECKOUT_SESSION_ID}"),
            cancel_url=os.environ.get("PAYWALL_CANCEL_URL", "https://baltimorelab.local/cancel"),
            customer_email=req.customer_email
        )
        return {"checkout_url": session.url}

    except stripe.error.StripeError as e:
        # Clinical error handling for Stripe API faults
        raise HTTPException(status_code=402, detail=f"Payment Gateway Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Logic Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("monetization_api:app", host="0.0.0.0", port=8000, reload=True)
