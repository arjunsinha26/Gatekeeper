<div align="center">

# 🛡️ Discord Community Management Bot

### Verification • Welcome Cards • Anti-Spam Moderation

A Discord bot built with `discord.py` and Pillow to automate member onboarding and provide basic moderation tools.

<p>
  <a href="#features"><img src="https://img.shields.io/badge/✨_Features-Explore-5865F2?style=for-the-badge" alt="Features"></a>
  <a href="#installation"><img src="https://img.shields.io/badge/🚀_Installation-Get_Started-2EA44F?style=for-the-badge" alt="Installation"></a>
  <a href="#commands"><img src="https://img.shields.io/badge/⌨️_Commands-Reference-007EC6?style=for-the-badge" alt="Commands"></a>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py 2.x">
  <img src="https://img.shields.io/badge/Pillow-Image_Processing-2EA44F?style=for-the-badge" alt="Pillow">
  <img src="https://img.shields.io/badge/Slash_Commands-Supported-blueviolet?style=for-the-badge" alt="Slash commands">
</p>

</div>

---

## 📌 Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Discord Developer Portal Setup](#discord-developer-portal-setup)
- [Configuration](#configuration)
- [Commands](#commands)
- [How Verification Works](#how-verification-works)
- [Moderation Settings](#moderation-settings)
- [Permissions](#permissions)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [License](#license)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 CAPTCHA Verification
- Generates a six-character CAPTCHA.
- Supports uppercase letters, lowercase letters, and digits.
- Sends the CAPTCHA image as an ephemeral response.
- Grants `Verified` and removes `Unverified` after a correct answer.
- Uses a 60-second answer timeout.

</td>
<td width="50%">

### 👋 Welcome Images
- Generates a welcome card when a member joins.
- Includes the member's avatar and username.
- Displays the server member number.
- Uses a custom `background.jpg` image.

</td>
</tr>
<tr>
<td width="50%">

### 🧩 Onboarding Setup
- Finds roles without case-sensitive name matching.
- Creates `Verified` or `Unverified` if missing.
- Creates or updates `#welcome` and `#verify`.
- Applies channel permission overwrites.

</td>
<td width="50%">

### 🚫 Anti-Spam Moderation
- Detects repeated identical text messages.
- Tracks messages with attachments.
- Attempts to delete detected spam.
- Applies a configurable timeout.
- Uses a cooldown for text-spam punishments.

</td>
</tr>
</table>

### 🧹 Moderator command

`/flush` lets members with **Manage Messages** delete a specified number of recent messages, from 1 to 100.

---

## 🧰 Requirements

- Python **3.10+** recommended
- A Discord application and bot account
- `discord.py` 2.x
- Pillow

## 🚀 Installation

### 1. Get the project files

Keep the script and image asset together. For example:

```text
discord-community-bot/
├── bot.py
├── background.jpg
├── README.md
└── .gitignore
```

The Python filename can be different; use your actual filename in the run command. The current code requires `background.jpg` at startup and resizes it to **900 × 300**.

### 2. Install dependencies

Open CMD or a terminal in the project directory:

```cmd
py -m pip install --upgrade discord.py Pillow
```

Check the installation:

```cmd
py -m pip show discord.py Pillow
```

### 3. Configure the Discord application

Continue to [Discord Developer Portal Setup](#discord-developer-portal-setup), then configure the token as described below.

---

## ⚙️ Discord Developer Portal Setup

1. Open the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create an application or select your existing application.
3. Open the **Bot** section and create the bot user if needed.
4. Under **Privileged Gateway Intents**, enable:
   - **Server Members Intent**
   - **Message Content Intent**
5. Under OAuth2 URL Generator, select these scopes:
   - `bot`
   - `applications.commands`
6. Generate the invite URL, open it, and add the bot to your server.

The bot uses member-join events and reads message content, so both privileged intents must be enabled in the portal as well as in the code.

---

## 🔑 Configuration

### Secure the bot token

Do not publish your real Discord token in source code or commit it to GitHub.

Replace the hard-coded token line with:

```python
import os

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("Set the DISCORD_TOKEN environment variable.")
```

**Windows CMD:**

```cmd
set DISCORD_TOKEN=YOUR_BOT_TOKEN
py bot.py
```

**PowerShell:**

```powershell
$env:DISCORD_TOKEN = "YOUR_BOT_TOKEN"
py bot.py
```

These commands set the environment variable for the current terminal session. If a real token has already been exposed, reset it in the Developer Portal.

### Background image

The current code loads the image when the script starts:

```python
BACKGROUND = Image.open("background.jpg").convert("RGBA").resize((900, 300))
```

Make sure the file exists in the working directory. If you run the script from another directory, use an absolute path or build a path relative to the script.

---

## ⌨️ Commands

| Command | Usage | Description | Permission |
|---|---|---|---|
| `/verify` | `/verify` | Starts CAPTCHA verification in `#verify`. | Server member |
| `/flush` | `/flush amount:10` | Deletes up to 100 recent messages from the current channel. | Manage Messages |

### `/verify`

A member runs `/verify` in `#verify`. The bot sends the CAPTCHA image privately, then waits up to 60 seconds for an answer.

### `/flush`

Example:

```text
/flush amount:10
```

- `amount` must be between `1` and `100`.
- The command checks the invoking member's **Manage Messages** permission.
- The response is ephemeral.
- The bot needs permission to manage messages in the channel.

---

## 🔄 How Verification Works

```text
Member joins
     ↓
Bot finds or creates roles
     ↓
Bot creates/updates welcome and verify channels
     ↓
Assigns Unverified role
     ↓
Posts welcome image and verification instructions
     ↓
Member runs /verify
     ↓
Ephemeral CAPTCHA image is sent
     ↓
Member types the answer in #verify
     ↓
Correct answer?
  ┌──┴───┐
 Yes     No / Timeout
  ↓          ↓
Add       Show error or
Verified  timeout message
  ↓
Remove Unverified
```

**CAPTCHA matching is case-sensitive.** The user must enter the generated characters with the same capitalization.

> **Important:** The CAPTCHA image is ephemeral, but the answer is currently collected using `bot.wait_for("message")`. That means the answer is a normal message in `#verify`, not private modal input.

---

## 🛡️ Moderation Settings

These constants are defined in the current script:

| Setting | Default | Purpose |
|---|---:|---|
| `TIMEOUT_MINUTES` | `30` | Duration of the timeout after detected spam |
| `SPAM_INTERVAL` | `10` seconds | Window used to track repeated text |
| `SPAM_THRESHOLD` | `3` messages | Number of matching messages that triggers detection |
| `PUNISHMENT_COOLDOWN` | `30` seconds | Cooldown between text-spam punishments for a member |
| `IMAGE_THRESHOLD` | `3` messages | Attachment-message threshold |
| `IMAGE_INTERVAL` | `10` seconds | Window used to track attachment spam |

To change the CAPTCHA length, edit `generate_captcha(length=6)`.

Spam history and cooldowns are stored in memory, so they reset when the bot restarts.

---

## 🔒 Permissions

The bot may need the following permissions for all features to work:

- **View Channels**
- **Send Messages**
- **Read Message History**
- **Attach Files**
- **Manage Roles**
- **Manage Channels**
- **Manage Messages**
- **Moderate Members**

The bot's highest role must be above `Verified` and `Unverified`. Discord will not let the bot assign roles above its highest role.

### Channel access behavior in the current code

- `#welcome`: `Verified` and `Unverified` can view the channel but cannot send messages.
- `#verify`: `Unverified` can view and send messages; `Verified` cannot view it.
- Other channels: the code hides channels from `Unverified` by applying permission overwrites.

**Test these settings in a separate server first.** The script edits existing channel overwrites and can affect access for members with the `Unverified` role.

---

## 🧯 Troubleshooting

| Problem | What to check |
|---|---|
| Bot does not come online | Verify the token and installed dependencies. |
| `/verify` or `/flush` is missing | Check that the bot was invited with `applications.commands` and that command sync completed. |
| Member-join setup does not run | Enable Server Members Intent in both the Developer Portal and code. |
| CAPTCHA answer is not received | Ensure Message Content Intent is enabled and the bot can access `#verify`. |
| Role assignment fails | Check Manage Roles and the bot's role hierarchy. |
| Welcome image fails | Confirm `background.jpg` exists and Pillow is installed. |
| Timeout or deletion fails | Check Moderate Members / Manage Messages permissions and the target member's role hierarchy. |

Errors from the current script are printed to the console. Keep the console open while testing.

---

## 🧪 Before Going Live

- [ ] Set the token as an environment variable.
- [ ] Enable both privileged intents.
- [ ] Place `background.jpg` beside the script.
- [ ] Confirm the bot has the required permissions.
- [ ] Place the bot role above the verification roles.
- [ ] Test verification with correct, incorrect, and timed-out answers.
- [ ] Confirm the channel overwrites match your intended server layout.
- [ ] Test `/flush` in a private test server.

---

## 🔐 Security

- Never commit your bot token, `.env` file, or other secrets.
- Consider adding a `.gitignore` file for local configuration and logs.
- Review permission changes before using this bot on an established server.
- Keep dependencies updated and test moderation changes before deployment.

Example `.gitignore`:

```gitignore
.env
__pycache__/
*.py[cod]
*.log
```

---

## 📄 License

This project does not specify a license in the provided code. Before making the repository public, choose a license and add the full text in a `LICENSE` file. The [MIT License](https://choosealicense.com/licenses/mit/) is one common permissive option if you want to allow reuse, modification, and redistribution.

---

<div align="center">

**Built with Python, discord.py, and Pillow**

[⬆ Back to top](#-discord-community-management-bot)

</div>
