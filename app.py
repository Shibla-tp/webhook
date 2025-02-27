from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ✅ Secure Airtable Credentials (Move to environment variables for security)
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "patELEdV0LAx6Aba3.393bf0e41eb59b4b80de15b94a3d122eab50035c7c34189b53ec561de590dff3")  # Store API key in env
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "app5s8zl7DsUaDmtx")  # Store Base ID in env
AIRTABLE_TABLE_NAME = "booking_records"  # Airtable table for appointments
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# 🔹 Function to Save Booking Data in Airtable
def save_to_airtable(name, email):
    """Saves name and email to the 'booking_record' Airtable table."""
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "full_name": name,    # Ensure this matches your Airtable column
            "email": email   # Ensure this matches your Airtable column
        }
    }
    try:
        response = requests.post(AIRTABLE_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise HTTP errors if any
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Airtable API error: {e}")
        return {"error": str(e)}

# 🔹 API Route to Receive Appointment Data
@app.route("/appointment", methods=["POST"])
def receive_appointment_data():
    """Receives appointment data from Systeme.io and saves to Airtable."""
    try:
        print(f"Request method: {request.method}")  
        print(f"Request headers: {request.headers}")  
        print(f"Raw request data: {request.data.decode('utf-8')}")  # Decode raw data for debugging

        # Parse JSON payload
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Extract name & email from Systeme.io payload
        contact_info = data.get("data", {}).get("contact", {})  # Get contact details
        name = contact_info.get("first_name", "")  # Use "first_name" from Systeme.io
        email = contact_info.get("email", "")

        # Validate required fields
        if not name or not email:
            return jsonify({"error": "Name and Email are required"}), 400  

        # Store data in Airtable
        response = save_to_airtable(name, email)

        return jsonify({"message": "Booking saved successfully", "airtable_response": response}), 200  

    except Exception as e:
        print(f"Error processing request: {e}")  
        return jsonify({"error": str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)  # ✅ Start Flask in debug mode
