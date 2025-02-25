from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔹 Airtable Configuration
AIRTABLE_API_KEY = "patELEdV0LAx6Aba3.393bf0e41eb59b4b80de15b94a3d122eab50035c7c34189b53ec561de590dff3"  # Replace with your API Key
AIRTABLE_BASE_ID = "app5s8zl7DsUaDmtx"  # Replace with your Base ID
AIRTABLE_TABLE_NAME = "landing_page_details"  # Table Name
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# 🔹 Function to save data in Airtable
def save_to_airtable(name, email, phone):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "First name": name,
            
            "Phone number": phone
        }
    }
    response = requests.post(AIRTABLE_URL, json=data, headers=headers)
    return response.json()

# 🔹 API Route to Receive Form Data
@app.route("/submit", methods=["POST"])
def receive_form_data():
    try:
        data = request.json  # Expecting JSON data from Systeme.io
        name = data.get("name")
        
        phone = data.get("phone")

        if not name:
            return jsonify({"error": "Name and Email are required"}), 400

        # Store data in Airtable
        response = save_to_airtable(name, phone)
        return jsonify({"message": "Form data saved successfully", "airtable_response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
  app.run(debug=True)

