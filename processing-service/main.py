import requests
from flask import Flask, request, jsonify
import os 
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/process-application", methods=["POST"])
def process():
    serverless_component_url = os.getenv("SERVERLESS_COMPONENT_URL")
    data = request.get_json()
    received_email = data["email"]
    received_name = data["name"]
    received_status = data["status"]
    
    payload = {
        "email": received_email,
        "name": received_name,
        "status": received_status
    }   

    try:
        response = requests.post(serverless_component_url, json=payload, timeout=5)
    except Exception as e:
        return jsonify({"message": f"Error occured: {e}."}), 500 

    return jsonify({"message": "success", "response": response.text}), 200




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)