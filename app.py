from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AIRTABLE_API_KEY = "patELEdV0LAx6Aba3.393bf0e41eb59b4b80de15b94a3d122eab50035c7c34189b53ec561de590dff3"  # Replace with your API Key - store in environment variables for security.
AIRTABLE_BASE_ID = "app5s8zl7DsUaDmtx"  # Replace with your Base ID - store in environment variables for security.
AIRTABLE_TABLE_NAME = "landing_page_details"  # Table Name - store in environment variables for security.
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# 🔹 Function to save email in Airtable
def save_to_airtable(email):
    """Saves the given email to Airtable."""
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "email": email  # Ensure this matches the field name in Airtable
        }
    }
    try:
        response = requests.post(AIRTABLE_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise error if request fails
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

        # Extract email from nested JSON
        email = data.get("data", {}).get("contact", {}).get("email")

        if not email:
            return jsonify({"error": "Email is required"}), 400  

        # Store email in Airtable
        response = save_to_airtable(email)

        return jsonify({"message": "Email saved successfully", "airtable_response": response}), 200  

    except Exception as e:
        print(f"Error processing request: {e}")  
        return jsonify({"error": str(e)}), 500  


if __name__ == '__main__':
    app.run(debug=True)  # ✅ Start Flask in debug mode
