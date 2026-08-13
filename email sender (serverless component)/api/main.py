import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BREVO_URL = "https://api.brevo.com/v3/smtp/email"

@app.route('/', methods=['POST'])
@app.route('/api/main', methods=['POST'])
def send_email():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request"}), 400

    email = data.get("email")
    name = data.get("name")
    status = data.get("status")

    email_payload = {
        "sender": {
            "name": "FlySo Recruitment",
            "email": os.getenv("SENDER_EMAIL")
        },
        "to": [
            {
                "email": email,
                "name": name
            }
        ],
        "subject": "FlySo Cadet Application Update",
        "htmlContent": f"""
                <h2>Dear {name},</h2>

                <p>
                Your application status has been updated.
                </p>

                <p>
                Status:
                <strong>{status}</strong>
                </p>

                <p>
                FlySo Recruitment Team
                </p>
            """
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": os.getenv("BREVO_API_KEY")
    }
    
    response = requests.post(BREVO_URL, json=email_payload, headers=headers)
    
    return jsonify(response.json()), response.status_code

# Fallback for local testing
if __name__ == "__main__":
    app.run()