from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔹 Airtable Configuration
AIRTABLE_API_KEY = "patELEdV0LAx6Aba3.393bf0e41eb59b4b80de15b94a3d122eab50035c7c34189b53ec561de590dff3"  # Replace with your API Key - store in environment variables for security.
AIRTABLE_BASE_ID = "app5s8zl7DsUaDmtx"  # Replace with your Base ID - store in environment variables for security.
AIRTABLE_TABLE_NAME = "landing_page_details"  # Table Name - store in environment variables for security.
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# 🔹 Function to save email in Airtable
def save_to_airtable(email):
    """Saves the given email to the Airtable table."""
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}", # Use the Airtable API key.
        "Content-Type": "application/json" # Indicate that we are sending JSON data.
    }
    data = {
        "fields": {
            "Email": email  # The field in Airtable to store the email.  Make sure this matches your Airtable column name exactly.
        }
    }
    try:
        response = requests.post(AIRTABLE_URL, json=data, headers=headers) # Post the data to Airtable.
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx).
        return response.json() # Return the JSON response from Airtable.
    except requests.exceptions.RequestException as e:
        print(f"Airtable API error: {e}")
        return {"error": str(e)}

# 🔹 API Route to Receive Form Data
@app.route("/submit", methods=["POST"])
def receive_form_data():
    """Receives form data from Systeme.io, extracts the email, and saves it to Airtable."""
    try:
        data = request.get_json()  # Get the JSON data sent from Systeme.io.
        email = data.get("email")  # Extract only the email field from the JSON data. Adjust the 'email' key based on Systeme.io's data structure.

        if not email:
            return jsonify({"error": "Email is required"}), 400 # If the email is missing, return a 400 error.

        # Store email in Airtable
        response = save_to_airtable(email)
        
        if "error" in response:
            return jsonify({"error": f"Failed to save email to Airtable: {response['error']}"}), 500

        return jsonify({"message": "Email saved successfully", "airtable_response": response}), 200 # Return a success message with the Airtable response.

    except Exception as e:
        print(f"Error processing webhook: {e}") #Log error to debug
        return jsonify({"error": str(e)}), 500 # Return a 500 error with the exception message.

if __name__ == '__main__':
    app.run(debug=True) #Start the Flask app in debug mode.  Do not use debug mode in production.
