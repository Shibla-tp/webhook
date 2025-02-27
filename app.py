from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

# ✅ Airtable Credentials
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "patELEdV0LAx6Aba3.393bf0e41eb59b4b80de15b94a3d122eab50035c7c34189b53ec561de590dff3")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "app5s8zl7DsUaDmtx")
AIRTABLE_TABLE_NAME = "booking_records"
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# ✅ Function to Save Data to Airtable
def save_to_airtable(name, email, phone, scheduled_date, scheduled_time):
    """Saves name, email, phone, and appointment date & time to Airtable."""
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "full_name": name, 
            "email": email,
            "phone_number": phone,
            "scheduled_date": scheduled_date,  # Add scheduled date
            "scheduled_time": scheduled_time   # Add scheduled time
        }
    }
    
    try:
        response = requests.post(AIRTABLE_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise HTTP error if request fails
        print("Airtable Response:", response.text)  # Debugging Airtable response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Airtable API error: {e}")
        return {"error": str(e)}

# ✅ API Route to Handle Systeme.io Webhook
@app.route("/appointment", methods=["POST"])
def receive_appointment_data():
    try:
        print(f"Request headers: {request.headers}")  
        print(f"Raw request data: {request.data.decode('utf-8')}")  # Debugging input data

        # Detect JSON format and parse
        if request.is_json:
            data = request.get_json()
        else:
            data = json.loads(request.data.decode("utf-8"))  # Manually parse JSON if needed

        if not data:
            return jsonify({"error": "No data received"}), 400

        # ✅ Extract name, email, phone, scheduled date, and scheduled time
        contact_info = data.get("data", {}).get("contact", {})
        fields = contact_info.get("fields", {})

        email = contact_info.get("email")  
        name = fields.get("surname", "")  
        phone = fields.get("phone_number", "")  
        scheduled_date = fields.get("scheduled_date", "")  # Extract date
        scheduled_time = fields.get("scheduled_time", "")  # Extract time

        if not name or not email or not phone or not scheduled_date or not scheduled_time:
            return jsonify({"error": "Name, Email, Phone, Scheduled Date, and Scheduled Time are required"}), 400  

        # ✅ Save to Airtable
        airtable_response = save_to_airtable(name, email, phone, scheduled_date, scheduled_time)

        return jsonify({"message": "Booking saved successfully", "airtable_response": airtable_response}), 200  

    except Exception as e:
        print(f"Error processing request: {e}")  
        return jsonify({"error": str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)
