# GateKeeper

GateKeeper is an advanced Discord security and verification bot built with `discord.py`.

It is designed to protect servers from:
- spam
- raid accounts
- image flooding
- unauthorized access

while also providing a clean automated onboarding experience for new members.

---

# Features

## CAPTCHA Verification System

New members must complete a CAPTCHA verification before accessing the server.

### Verification Flow
- User joins server
- Receives `UNVERIFIED` role
- Gains access only to:
  - `#welcome`
  - `#verify`
- Uses `/verify`
- Completes CAPTCHA
- Receives `VERIFIED` role automatically

---

## Automatic Channel & Role Setup

GateKeeper automatically creates:

### Roles
- `VERIFIED`
- `UNVERIFIED`

### Channels
- `#welcome`
- `#verify`

It also configures permissions automatically.

---

## Welcome System

Generates custom welcome cards featuring:
- member avatar
- username
- member count
- custom background image

Uses:
```text
background.jpg
```

---

## Anti-Spam Protection

### Text Spam Detection
Detects:
- repeated messages
- rapid duplicate spam

Actions:
- deletes spam messages
- bulk deletes duplicates
- automatically timeouts offenders

---

## Anti-Image Spam

Detects:
- image flooding
- repeated attachment spam

Actions:
- deletes image spam
- automatically timeouts offenders

---

## Automatic Timeout System

Spam offenders are automatically:
- timed out for 30 minutes
- rate-limited safely
- handled using cooldown protection

---

## Slash Moderation Commands

### `/verify`
Start CAPTCHA verification.

### `/flush`
Bulk delete messages in a channel.

Example:
```text
/flush 50
```

---

# Technologies Used

- Python
- discord.py
- Pillow (PIL)

---

# Installation

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Add Background Image

Place:
```text
background.jpg
```

in the project root folder.

---

## Configure Token

Replace:
```python
TOKEN = "YOUR_TOKEN"
```

with:
```python
import os

TOKEN = os.getenv("DISCORD_TOKEN")
```

---

# Run Bot

```bash
python bot.py
```

---

# Required Bot Permissions

- Manage Roles
- Manage Channels
- Manage Messages
- Moderate Members
- Send Messages
- Attach Files
- Read Message History

---

# Required OAuth2 Scopes

- bot
- applications.commands

---

# Notes

- Slash commands may take time to sync globally.
- Guild sync is recommended during development.
- Never expose your Discord token publicly.
