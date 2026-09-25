# Paid SMS to Google Chat Bridge
## Using Twilio + Serverless (Recommended for Production)

This guide walks you through using Twilio to receive SMS and forward to Google Chat.

**Total cost: ~$1-3/month + usage (~$0.007 per SMS)**

---

## When to Use Twilio

✅ **Use Twilio if you need:**
- Bidirectional SMS (Chat → SMS reply)
- Real-time SMS delivery (instant, not 5-10 min delay)
- Keep an existing phone number
- Production-grade reliability
- Higher SMS volume

❌ **Use free Google Voice if you only need:**
- One-way SMS → Chat
- Free tier
- Occasional use

---

## Architecture

```
Your Phone Number (or Twilio number)
        ↓
   (SMS received)
        ↓
   Twilio Webhook
        ↓
  Serverless Function
  (Cloud Run / Lambda)
        ↓
  Google Chat webhook
        ↓
   Your Chat room
```

---

## Step 1: Set Up Twilio Account

1. Go to **https://www.twilio.com**
2. Sign up for a free trial account (includes $15 credit)
3. Verify your email and phone number
4. You get a free Twilio number

**Free tier includes:**
- 1 free phone number for 30 days
- ~$15 credit (enough for ~2,000 incoming SMS)

---

## Step 2: Buy or Port a Phone Number

### Option A: Use Free Twilio Trial Number
1. Twilio gives you a free number during trial
2. This is the fastest way to test
3. After trial ends, number costs ~$1/month

### Option B: Port Your Old AT&T Number
1. In Twilio Console → **Phone Numbers** → **Manage** → **Active Numbers**
2. Click **"Port a Number"**
3. Enter your AT&T number and follow the process
4. Cost: ~$75 one-time for number porting + ~$1/month

---

## Step 3: Create a Google Chat Webhook

1. Open your Google Chat room
2. Click room name → **Settings** → **Manage webhooks**
3. Click **"Create new webhook"**
4. Name it: `SMS Bridge`
5. Copy the webhook URL
6. Save it in a safe place

---

## Step 4: Deploy the Python App

### Option A: Google Cloud Run (Easiest)

1. Clone this repo:
   ```bash
   git clone https://github.com/vexdzphone911-max/sms-to-chat-bridge
   cd sms-to-chat-bridge
   ```

2. Create a `.env` file with your Chat webhook:
   ```bash
   cp .env.example .env
   # Edit .env and paste your Chat webhook URL
   ```

3. Create a `Dockerfile` (if not present):
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY app.py .
   CMD ["python", "app.py"]
   ```

4. Deploy to Google Cloud Run:
   ```bash
   gcloud run deploy sms-to-chat \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars CHAT_WEBHOOK_URL="your_webhook_url_here"
   ```

5. Copy the deployment URL (looks like: `https://sms-to-chat-xxxxx.run.app`)

### Option B: Render (Free Tier)

1. Go to **https://render.com**
2. Sign up for a free account
3. Click **"New"** → **"Web Service"**
4. Connect your GitHub repo (fork this one first)
5. Fill in:
   - **Name:** `sms-to-chat`
   - **Environment:** `Python 3`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python app.py`
6. Add environment variable:
   - **CHAT_WEBHOOK_URL:** Paste your webhook URL
7. Click **"Create Web Service"**
8. Copy the deployment URL (looks like: `https://sms-to-chat.onrender.com`)

### Option C: Railway (Free Tier)

1. Go to **https://railway.app**
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select this repo
5. Add environment variable: `CHAT_WEBHOOK_URL=your_webhook_url`
6. Railway auto-deploys; copy the public URL

---

## Step 5: Connect Twilio to Your App

1. In Twilio Console, go to **Phone Numbers** → **Manage** → **Active Numbers**
2. Click your phone number
3. Under **Messaging** → **A Message Comes In:**
   - Set to **Webhook**
   - Paste your deployment URL: `https://your-deployment-url.run.app/sms-to-chat`
   - Method: `POST`
4. Click **"Save"**

---

## Step 6: Test

1. Text your Twilio number from any phone
2. Within 1-2 seconds, message should appear in Google Chat
3. You should see:
   ```
   📱 SMS from +1-555-1234
   
   Hello from Twilio!
   ```

---

## Cost Breakdown

| Item | Cost |
|------|------|
| Twilio phone number | $1/month |
| Incoming SMS | $0.0075 per SMS |
| Google Cloud Run | ~$0.25/month (free tier covers most) |
| Render free tier | FREE |
| Google Chat webhook | FREE |
| **Monthly (low volume)** | **~$1.50** |
| **Monthly (100 SMS/mo)** | **~$2.00** |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Webhook returned 404" | Check your deployment URL is correct; test with `curl` |
| SMS not appearing in Chat | Check `CHAT_WEBHOOK_URL` env var is set correctly |
| Twilio says "connection refused" | Make sure your deployment is running (check status in Cloud Run / Render) |
| No SMS at all | Check Twilio console **Logs** tab for errors |

---

## Next Steps

- **Add bidirectional replies** (Chat → SMS back): See `app.py` for extension points
- **Store SMS history** in a database: Add a simple SQLite or Cloud Firestore integration
- **Filter by sender** or keywords: Add logic in the webhook handler
- **Add rate limiting** for high volume: Use Redis or Twilio's rate limiting

---

## Summary

**Paid SMS to Chat (Twilio):**
1. Create Twilio account (~$1/mo)
2. Buy or port a number ($0-75)
3. Deploy Python app to serverless (free tier)
4. Connect Twilio webhook
5. Done!

**Time to set up:** ~15 minutes

**Total cost:** ~$1-3/month
