from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


REAL_WEBHOOK_URL = "https://discord.com/api/webhooks/1401667672453939263/DhzZntY-woLUCaopyMBY9op2liUL7Bocc6iQ2AgFzpCYZHJeMsw6Kj16zq7tuvlFjQ0E"

@app.route("/send", methods=["POST"])
def send_protected_message():
    data = request.json
    if not data or "content" not in data:
        return jsonify({"error": "Missing 'content' field"}), 400
    
    message = data["content"]

    if "@everyone" in message or "@here" in message:
        return jsonify({"error": "Mentions @everyone or @here are not allowed."}), 403
    
    response = requests.post(REAL_WEBHOOK_URL, json={"content": message})

    if response.status_code == 204:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Failed to send message"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
