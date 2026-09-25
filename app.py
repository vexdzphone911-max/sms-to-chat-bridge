import os
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CHAT_WEBHOOK_URL = os.getenv("CHAT_WEBHOOK_URL")


@app.get("/health")
def health_check():
    return {"status": "ok"}, 200


@app.post("/sms-to-chat")
def sms_to_chat():
    if not CHAT_WEBHOOK_URL:
        logger.error("CHAT_WEBHOOK_URL is not configured")
        resp = MessagingResponse()
        resp.message("Chat webhook not configured")
        return str(resp), 500

    from_number = request.form.get("From", "unknown")
    body = request.form.get("Body", "")

    logger.info("Received SMS from %s: %s", from_number, body)

    chat_message = {
        "text": f"📱 *SMS from {from_number}*\n\n{body}"
    }

    try:
        response = requests.post(
            CHAT_WEBHOOK_URL,
            json=chat_message,
            timeout=10,
        )
        response.raise_for_status()
        logger.info("SMS forwarded to Google Chat successfully")
    except Exception as exc:  # pragma: no cover - logging path
        logger.exception("Failed to forward SMS to Google Chat: %s", exc)
        resp = MessagingResponse()
        resp.message("Error forwarding message")
        return str(resp), 500

    twilio_response = MessagingResponse()
    twilio_response.message("Message received and forwarded to Chat")
    return str(twilio_response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=False)
