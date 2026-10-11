<div align="center">

<div align="center">

# 🛡️ Discord Community Management Bot

### Verification, Welcome Cards & Automated Moderation

**Secure your community. Welcome new members. Moderate spam automatically with discord.py.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Generation-009688?style=for-the-badge)
![CAPTCHA](https://img.shields.io/badge/CAPTCHA-Verification-22A06B?style=for-the-badge)
![Moderation](https://img.shields.io/badge/Anti--Spam-Automated-D97706?style=for-the-badge)

[Features](#-features) · [How It Works](#-how-it-works) · [Installation](#-installation) · [Configuration](#️-configuration) · [Commands](#-commands) · [Limitations](#️-limitations)

</div>

---

## ✨ Features

### 🔐 CAPTCHA verification

-   Generates a six-character CAPTCHA using uppercase letters, lowercase
    letters, and digits.
-   Renders the CAPTCHA as a PNG image.
-   Provides a `/verify` slash command.
-   Adds the **Verified** role after a correct answer and removes
    **Unverified**.
-   Uses a 60-second response timeout.

> **Privacy note:** In the current implementation, the CAPTCHA image is
> sent ephemerally, but the answer is collected with
> `bot.wait_for("message")` in the `#verify` channel. The member's typed
> answer is therefore a normal channel message, not an ephemeral
> response.

### 👋 Welcome cards

-   Creates a welcome image when a member joins.
-   Includes the member's avatar, username, and server member number.
-   Posts the generated image in `#welcome`.

### 🧩 Automatic role and channel setup

When a member joins, the bot looks for `Verified` and `Unverified` roles
(case-insensitively), creates either role if missing, and creates or
updates the `#welcome` and `#verify` text channels.

The current code also applies an overwrite to hide other channels from
the **Unverified** role. Review this behavior carefully before using the
bot in an existing server.

### 🚫 Anti-spam moderation

-   Detects repeated identical text messages.
-   Detects repeated messages containing attachments.
-   Deletes detected spam where possible.
-   Applies a **30-minute timeout** after a detected spam burst.
-   Uses a cooldown to avoid repeatedly punishing the same member too
    quickly.
-   Sends a short-lived moderation notice.

### 🧹 `/flush`

-   Deletes a specified number of recent messages in the current
    channel.
-   Restricted to members with **Manage Messages** permission.
-   Accepts values from **1 to 100**.
-   Responds privately with the number of messages deleted or an error.

------------------------------------------------------------------------

## 🔄 How It Works

**Join → Unverified role → Welcome image → `/verify` CAPTCHA → Verified role**

Repeated messages or attachment spam trigger cleanup and a temporary timeout.

## 📦 Installation

### Requirements

-   Python **3.10 or newer** recommended
-   A Discord application and bot account
-   `discord.py` 2.x
-   Pillow

Install the Python dependencies:

``` bash
py -m pip install -U discord.py Pillow
```

------------------------------------------------------------------------

## 📁 Project structure

Keep the Python script and background image together:

``` text
discord-bot/
├── bot.py
├── background.jpg
├── README.md
└── .gitignore
```

You can name the Python file differently; use that filename in the
commands below.

`background.jpg` is required by the current code. It is resized to **900
× 300** when the script starts.

------------------------------------------------------------------------

## ⚙️ Discord Developer Portal setup

1.  Open the [Discord Developer
    Portal](https://discord.com/developers/applications) and select your
    application.
2.  Open **Bot** and create the bot user if you have not already.
3.  Under **Privileged Gateway Intents**, enable:
    -   **Server Members Intent**
    -   **Message Content Intent**
4.  Invite the bot to your server with the required OAuth2 scopes:
    -   `bot`
    -   `applications.commands`

### Recommended bot permissions

Grant only the permissions the bot needs:

-   View Channels
-   Send Messages
-   Read Message History
-   Attach Files
-   Manage Roles
-   Manage Channels
-   Manage Messages
-   Moderate Members

The bot's highest role must be **above** the `Verified` and `Unverified`
roles in **Server Settings → Roles**. Otherwise, role assignment may
fail.

------------------------------------------------------------------------

## 🔑 Configure the bot token

Do **not** commit your bot token to GitHub. In the script, replace the
hard-coded token with an environment variable:

``` python
import os

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Set the DISCORD_TOKEN environment variable.")
```

Then, in Windows Command Prompt, set the token for the current terminal
session and run the script:

``` cmd
set DISCORD_TOKEN=YOUR_BOT_TOKEN
py bot.py
```

In PowerShell:

``` powershell
$env:DISCORD_TOKEN = "YOUR_BOT_TOKEN"
py bot.py
```

If a real token has already been published, reset it in the Developer
Portal before continuing.

------------------------------------------------------------------------

## 🚀 Run the bot

From the project directory:

``` cmd
py bot.py
```

On startup, the bot logs in and synchronizes its application (slash)
commands. After the bot is online, the commands should become available
in Discord.

------------------------------------------------------------------------

## 📖 Commands

  --------------------------------------------------------------------------
  Command                    Description             Access
  -------------------------- ----------------------- -----------------------
  `/verify`                  Starts CAPTCHA          Server members
                             verification in         
                             `#verify`.              

  `/flush amount:<number>`   Deletes 1--100 recent   Members with Manage
                             messages from the       Messages
                             current channel.        
  --------------------------------------------------------------------------

### Verification flow

1.  A member joins the server.
2.  The bot assigns the `Unverified` role and posts a welcome card.
3.  The bot directs the member to `#verify`.
4.  The member runs `/verify` and receives a CAPTCHA image privately.
5.  The member types the CAPTCHA answer in `#verify`.
6.  If the answer matches exactly, the bot adds `Verified` and removes
    `Unverified`.

The CAPTCHA comparison is **case-sensitive**.

------------------------------------------------------------------------

## 🛠️ Configuration

The following constants in the script control anti-spam behavior:

  --------------------------------------------------------------------------
  Setting                                      Default Meaning
  ----------------------- ---------------------------- ---------------------
  `TIMEOUT_MINUTES`                               `30` Timeout duration
                                                       after detected spam

  `SPAM_INTERVAL`                         `10` seconds Window for repeated
                                                       identical text

  `SPAM_THRESHOLD`                        `3` messages Repeated-text
                                                       threshold

  `PUNISHMENT_COOLDOWN`                   `30` seconds Minimum interval
                                                       between text-spam
                                                       punishments per
                                                       member

  `IMAGE_THRESHOLD`                       `3` messages Attachment-message
                                                       threshold

  `IMAGE_INTERVAL`                        `10` seconds Window for attachment
                                                       spam
  --------------------------------------------------------------------------

The CAPTCHA length is set in `generate_captcha(length=6)`. The
welcome-card background is loaded from `background.jpg`.

------------------------------------------------------------------------

## ⚠️ Limitations

### Important implementation notes

-   **Channel permissions:** On member join, the script edits or creates
    `#welcome` and `#verify`, and applies permission overwrites. It also
    hides every other channel from `Unverified`. Test this on a private
    test server first; these changes may affect an existing server's
    channel access.
-   **CAPTCHA input:** Although the CAPTCHA image and response messages
    are ephemeral, the answer is collected as a normal message in
    `#verify`. A modal would be needed for private text input.
-   **Spam detection:** The counters are stored in memory, so they reset
    whenever the bot restarts. Tune thresholds to suit your server.
-   **Permissions and hierarchy:** The bot cannot grant roles above its
    own highest role, and moderation actions can fail if the bot lacks
    permissions.
-   **Font fallback:** The script attempts to load `arial.ttf`; if
    unavailable, it falls back to Pillow's default font.
-   **Error logging:** Runtime errors are printed to the console. Keep
    the console or a log capture open while testing.

------------------------------------------------------------------------

## 🧪 Suggested first-run checklist

-   [ ] Set `DISCORD_TOKEN` securely.
-   [ ] Enable Server Members Intent and Message Content Intent.
-   [ ] Put `background.jpg` beside the script.
-   [ ] Place the bot's role above `Verified` and `Unverified`.
-   [ ] Confirm the bot has the required channel and moderation
    permissions.
-   [ ] Test role assignment and channel visibility in a test server.
-   [ ] Test `/verify` with both correct and incorrect CAPTCHA answers.
-   [ ] Test `/flush` with a moderator account.

------------------------------------------------------------------------

## 📄 License

Choose a license before publishing the repository. If you want others to
use, modify, and redistribute the project, the **MIT License** is a
common permissive option. Add a `LICENSE` file with the full license
text before claiming the repository is MIT-licensed.

------------------------------------------------------------------------

## 🤝 Contributing

Suggestions and improvements are welcome. Before submitting changes,
test verification, permission overwrites, and moderation behavior in a
separate Discord server.

## 💬 Disclaimer

Use moderation features responsibly. Review all permission changes and
test the bot in a development server before deploying it to a live
community.
