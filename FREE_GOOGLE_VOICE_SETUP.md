# Free SMS to Google Chat Bridge
## Using Google Voice + Gmail + IFTTT (Zero Cost)

This guide walks you through forwarding SMS from a free Google Voice number to your Google Chat room **without paying for Twilio, SMS providers, or serverless hosting**.

**Total cost: $0**

---

## Architecture

```
Google Voice Number
        ↓
   (SMS received)
        ↓
   Gmail inbox
   (as email)
        ↓
   IFTTT / Make / n8n
   (automation trigger)
        ↓
 Google Chat webhook
        ↓
  Your Chat room
```

---

## Step 1: Create a Free Google Voice Number

1. Go to **https://voice.google.com**
2. Sign in with your Google account
3. Click **"Create a Google Voice account"**
4. Choose a free phone number (or port an existing one)
5. Verify your actual phone number (one-time)
6. Your Google Voice number is now active

**Note:** You can use this number to receive SMS. Incoming texts go to your Gmail inbox as email notifications.

---

## Step 2: Configure Google Voice to Forward SMS to Email

1. Go to **voice.google.com** → **Settings** (gear icon, top right)
2. Click **"Forwarding & voicemail"**
3. Under **"Text Messages"**, check the box for **"Receive text messages on this computer"**
4. Save

**Result:** When someone texts your Google Voice number, you receive an email in Gmail.

---

## Step 3: Create a Google Chat Webhook

1. Open your Google Chat room where you want SMS to appear
2. Click the room name at the top → **"Settings"** (or right-click the room)
3. Select **"Manage webhooks"** or **"Webhooks"**
4. Click **"Create new webhook"**
5. Name it: `SMS Bridge`
6. Click **"Save"**
7. Copy the webhook URL (looks like: `https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=...&token=...`)
8. **Save this URL somewhere safe** (you'll need it for IFTTT)

---

## Step 4: Set Up IFTTT (Free Automation)

### Option A: Using IFTTT (Easiest)

1. Go to **https://ifttt.com**
2. Sign up for a free account
3. Click **"Create"** (top right)
4. Click **"If This"** (the trigger)
5. Search for **"Gmail"**
6. Select **"New email in inbox"**
7. Connect your Gmail account
8. Configure the trigger:
   - **From:** `noreply@google.com` (Google Voice sends from this)
   - **Subject contains:** `Google Voice notification` or `You have a new text message`
   - Click **"Create trigger"**

9. Click **"Then That"** (the action)
10. Search for **"Webhooks"**
11. Select **"Make a web request"**
12. Fill in:
    - **URL:** Paste your Google Chat webhook URL
    - **Method:** `POST`
    - **Content Type:** `application/json`
    - **Body:**
      ```json
      {
        "text": "📱 {{Subject}} \n\n {{BodyPlain}}"
      }
      ```
13. Click **"Create action"**
14. Give your applet a name (e.g., "SMS to Chat")
15. Click **"Finish"**

**Done!** Every incoming SMS to your Google Voice number will now post to your Chat room.

---

### Option B: Using Make.com (More Flexible)

1. Go to **https://make.com** (formerly Integromat)
2. Sign up for a free account
3. Click **"Create a new scenario"**
4. Click the empty box to add a module
5. Search for **"Gmail"**
6. Select **"Watch emails"**
7. Connect your Gmail account
8. Configure:
   - **Mailbox:** Inbox
   - **Search criteria:** `from:noreply@google.com subject:"Google Voice"`
   - **Max results:** 10
9. Click **"OK"**

10. Click the **"+"** to add the next step
11. Search for **"HTTP"**
12. Select **"Make a request"**
13. Configure:
    - **URL:** Paste your Google Chat webhook URL
    - **Method:** POST
    - **Header:** 
      - `Content-Type: application/json`
    - **Body:** Raw
      ```json
      {
        "text": "📱 SMS notification\n\n{{2.subject}}\n\n{{2.textPlain}}"
      }
      ```
14. Click **"OK"**
15. Click **"Run once"** to test
16. Click **"Save"** (top left)

**Done!** Make will check Gmail every few minutes and post new SMS to Chat.

---

### Option C: Using n8n (Self-Hosted, Advanced)

If you want to run automation on your own computer (no cloud provider):

1. Install n8n: `npm install -g n8n`
2. Run: `n8n start`
3. Go to `http://localhost:5678`
4. Create a new workflow
5. Add a **Gmail trigger** (watch emails)
6. Add an **HTTP request node** (POST to your Chat webhook)
7. Connect them and deploy

This runs on your machine and costs $0.

---

## Step 5: Test It

1. Text your Google Voice number from any phone
2. Within 30 seconds (or a few minutes for IFTTT), the message should appear in your Google Chat room
3. It should look like:
   ```
   📱 Google Voice notification
   
   You have a new text message from +1-555-1234: "Hey there!"
   ```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| SMS not appearing in Gmail | Check Google Voice settings → "Receive text messages on this computer" is enabled |
| IFTTT not triggering | Check Gmail for the notification email; IFTTT needs the email to exist |
| Chat webhook returns 404 | Make sure the webhook URL is correct; copy it again from Chat settings |
| Slow updates (5-10 min delay) | IFTTT checks every few minutes; Make.com is faster; n8n is real-time |
| Old AT&T number won't work | Google Voice is a new number; old carrier numbers need porting (paid) |

---

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Google Voice | FREE |
| Gmail | FREE |
| IFTTT | FREE (pro tier $2.99/mo optional) |
| Make.com | FREE (up to 1,000 ops/mo) |
| n8n self-hosted | FREE |
| Google Chat | FREE |
| **Total** | **$0** |

---

## Limitations of This Free Setup

✅ **What works:**
- Receive SMS and see in Chat
- Free Google Voice number
- No paid SMS infrastructure
- Easy to set up

❌ **What doesn't work:**
- Keep your exact old AT&T number (717-330-5531) without paying for porting
- Reply from Chat back to SMS (one-way only; use Twilio for bidirectional)
- High volume (IFTTT has rate limits)
- Real-time SMS (5-10 min delay typical)

---

## Next Steps

If you need:
- **Bidirectional SMS** (Chat → SMS reply) → Use Twilio ($1-5/mo)
- **Keep old number** → Port to Twilio or carrier ($25-50 one-time)
- **Real-time** → Use n8n self-hosted or paid serverless
- **High volume** → Use Make.com paid tier or serverless

---

## Advanced: Port Your Old Number to Google Voice

If you want to use your old AT&T number instead of a new Google Voice number:

1. Google Voice supports porting for **$20 one-time**
2. Go to **voice.google.com** → **Settings** → **"Linked phone"**
3. Scroll down and find **"Port your number"**
4. Enter your AT&T number and follow the process
5. After 24-48 hours, your old number works with Google Voice

**Cost:** $20 one-time + $0/month

---

## Summary

**Free SMS to Chat:**
1. Create Google Voice number (free)
2. Google sends SMS as Gmail emails (free)
3. IFTTT watches Gmail and posts to Chat (free)
4. Done!

**Time to set up:** ~10 minutes

**Total cost:** $0 (or $20 if you port your old number)
