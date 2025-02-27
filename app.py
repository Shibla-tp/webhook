from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Airtable Credentials (Move to environment variables for security)
AIRTABLE_API_KEY = "patELEdV0LAx6Aba3.393bf0e41eb59b4b80de15b94a3d122eab50035c7c34189b53ec561de590dff3"
AIRTABLE_BASE_ID = "app5s8zl7DsUaDmtx"
AIRTABLE_TABLE_NAME = "landing_page_details"
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# 🔹 Function to save form data in Airtable
def save_to_airtable(email, name, phone):
    """Saves email, first name, and phone number to Airtable."""
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "email": email,
            "name": name,  # Make sure this matches the Airtable field name
            "phone": phone       # Make sure this matches the Airtable field name
        }
    }
    try:
        response = requests.post(AIRTABLE_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Airtable API error: {e}")
        return {"error": str(e)}

# 🔹 API Route to Receive Form Data
@app.route("/submit", methods=["POST"])
def receive_form_data():
    try:
        print(f"Request method: {request.method}")  
        print(f"Request headers: {request.headers}")  
        print(f"Raw request data: {request.data}")  

        # Ensure JSON is received correctly
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        # Extract email, first name, and phone from nested JSON
        contact_info = data.get("data", {}).get("contact", {})
        email = contact_info.get("email")
        name = contact_info.get("surname")  # Assuming the key is "first_name"
        phone = contact_info.get("phone_number")  # Assuming the key is "phone"

        # Validate required fields
        if not email or not name or not phone:
            return jsonify({"error": "Email, First Name, and Phone are required"}), 400  

        # Store data in Airtable
        response = save_to_airtable(email, name, phone)

        return jsonify({"message": "Data saved successfully", "airtable_response": response}), 200  

    except Exception as e:
        print(f"Error processing request: {e}")  
        return jsonify({"error": str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)  # ✅ Start Flask in debug mode
