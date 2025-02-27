from flask import Flask, request, jsonify
import requests
import os
import json  # Added for manual decoding if needed

app = Flask(__name__)

# ✅ Airtable Credentials
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "patELEdV0LAx6Aba3.393bf0e41eb59b4b80de15b94a3d122eab50035c7c34189b53ec561de590dff3")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "app5s8zl7DsUaDmtx")
AIRTABLE_TABLE_NAME = "booking_records"  # Ensure this matches the Airtable table name
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# ✅ Function to Save Data to Airtable
def save_to_airtable(name, email, phone):
    """Saves name, email, and phone number to Airtable."""
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "full_name": name,  # Ensure this matches your Airtable column names
            "email": email,
            "phone_number": phone
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

        # ✅ Extract name, email, and phone correctly
        contact_info = data.get("data", {}).get("contact", {})
        fields = contact_info.get("fields", {})

        email = contact_info.get("email")  # Extract email
        name = fields.get("surname", "")  # Extract surname as name
        phone = fields.get("phone_number", "")  # Extract phone number

        if not name or not email or not phone:
            return jsonify({"error": "Name, Email, and Phone are required"}), 400  

        # ✅ Save to Airtable
        airtable_response = save_to_airtable(name, email, phone)

        return jsonify({"message": "Booking saved successfully", "airtable_response": airtable_response}), 200  

    except Exception as e:
        print(f"Error processing request: {e}")  
        return jsonify({"error": str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)  # ✅ Start Flask in debug mode
