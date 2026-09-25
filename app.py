import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")

@app.route("/", methods=["GET"])
def home():
    return "Mazoon WhatsApp AI is running", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403
def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v26.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code, response.text)


@app.route("/webhook", methods=["POST"])
def receive_webhook():
    data = request.get_json(silent=True) or {}
    print(data)

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" in value:
            message = value["messages"][0]
            customer_number = message["from"]

            if message.get("type") == "text":
                customer_text = message["text"]["body"]

                reply = f"مرحباً بك في موزون 🌿\nاستلمنا رسالتك: {customer_text}"

                send_whatsapp_message(customer_number, reply)

    except Exception as e:
        print("Webhook error:", e)

    return "EVENT_RECEIVED", 200return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
