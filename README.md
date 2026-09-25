# SMS to Google Chat Relay

This project receives incoming SMS messages from a number behind a telecom provider (such as Twilio or a ported number) and forwards each message to a Google Chat room using an incoming webhook.

Why this project exists:
- You want text messages from an old number to be visible in a team chat.
- You want a lightweight serverless or web-service bridge.
- You want a simple Python app that can run on any platform that supports Flask.

Important note on cost:
- If you need to keep the exact old phone number and keep it active, your carrier or a number provider will usually charge something, or require a porting process.
- If you only want a free relay, the cheapest real option is Google Voice + Gmail + a free automation tool (IFTTT, Make, or n8n) that posts to Google Chat.
- This repo is the technical bridge for the case where your number already routes through Twilio or a similar provider.

## Architecture

```text
Old number / Twilio webhook
        |
        v
    Flask app
        |
        v
Google Chat webhook
```

## Features
- Accepts SMS from Twilio webhooks
- Reads From and Body values from the incoming POST request
- Posts a formatted message to Google Chat
- Returns TwiML so Twilio accepts the message
- Minimal dependencies and easy deployment

## Quick start

1. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example environment file:

```bash
cp .env.example .env
```

4. Set your Chat webhook URL in `.env`:

```bash
CHAT_WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/XXXXXXXX/messages?key=...&token=..."
```

5. Run the app:

```bash
python app.py
```

6. Expose it with a public URL (for example via Cloud Run, Render, Railway, or a tunnel tool), then configure your Twilio number to call that URL as the incoming SMS webhook.

## Example webhook payload

Twilio sends data like this:

```text
From=+15551234567
Body=Hello from the old number
```

The app sends a Google Chat message like:

```text
📱 SMS from +15551234567

Hello from the old number
```

## Production deployment ideas

- Google Cloud Run
- Azure Container Apps
- Render
- Railway
- Fly.io
- AWS Lambda or App Runner

## Free path (recommended)

If you want zero paid SMS infrastructure, use this route instead:

1. Create a free Google Voice number
2. Route SMS to Gmail
3. Use IFTTT, Make, or n8n to trigger a Google Chat webhook
4. Post the message to your Chat room

That avoids the need to pay per text or port an old number.

## Files
- `app.py` — Flask webhook server
- `requirements.txt` — Python dependencies
- `.env.example` — environment variable template
- `.gitignore` — ignore local env files and caches

## License

MIT
