# backend/main.py

import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# --- Initialize FastAPI and Twilio Client ---
app = FastAPI()
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# --- In-memory store for OTPs ---
# In a real application, use a database like Redis for this.
otp_store = {}

# --- CORS Middleware ---
# This allows our frontend (running on a different port) to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# --- Pydantic Models for Request Bodies ---
class PhoneRequest(BaseModel):
    phone: str # Expects phone number in E.164 format, e.g., +919876543210

class VerifyRequest(BaseModel):
    phone: str
    otp: str


# --- API Endpoints ---

@app.post("/send-otp")
def send_otp(request: PhoneRequest):
    """
    Generates a 6-digit OTP, stores it, and sends it to the user's phone.
    """
    phone_number = request.phone
    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Store the OTP with the phone number
    otp_store[phone_number] = otp
    
    print(f"Generated OTP for {phone_number}: {otp}") # For debugging

    try:
        # Send the OTP via Twilio SMS
        message = twilio_client.messages.create(
            body=f"Your verification code is: {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return {"status": "success", "message": "OTP sent successfully", "sid": message.sid}
    except Exception as e:
        # If Twilio fails, return an error
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/verify-otp")
def verify_otp(request: VerifyRequest):
    """
    Verifies the OTP submitted by the user.
    """
    phone_number = request.phone
    user_otp = request.otp

    # Check if the phone number and OTP match what's in our store
    if phone_number in otp_store and otp_store[phone_number] == user_otp:
        # OTP is correct, remove it from the store (one-time use)
        del otp_store[phone_number]
        return {"status": "success", "message": "OTP verified successfully"}
    else:
        # OTP is incorrect or expired
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")