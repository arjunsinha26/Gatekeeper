::: {align="center"}
# 🛡️ Discord Community Management Bot

**CAPTCHA verification · Welcome cards · Anti-spam moderation**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-2EA44F?style=for-the-badge)

[Features](#features) · [Setup](#setup) · [Commands](#commands) ·
[Configuration](#configuration) · [Notes](#implementation-notes)
:::

------------------------------------------------------------------------

A Discord bot built with **discord.py** and **Pillow** to help manage
member onboarding and basic server moderation. It generates CAPTCHA
images, creates personalized welcome cards, configures verification
channels and roles, detects repeated spam, and provides a
message-cleanup command.

## Features

-   **CAPTCHA verification** --- Generates a six-character,
    case-sensitive CAPTCHA image for the `/verify` flow.
-   **Personalized welcome cards** --- Creates a graphic with a new
    member's avatar, username, and server member count.
-   **Automatic onboarding setup** --- Finds or creates the `Verified`
    and `Unverified` roles and creates or updates `#welcome` and
    `#verify`.
-   **Text anti-spam** --- Detects repeated identical messages within a
    configurable time window.
-   **Attachment spam detection** --- Tracks repeated messages
    containing attachments.
-   **Timeout moderation** --- Attempts to delete detected spam and
    apply a 30-minute timeout.
-   **Message cleanup** --- `/flush` deletes a chosen number of recent
    messages for moderators.

## Setup

### Requirements

-   Python 3.10 or newer recommended
-   A Discord application and bot account
-   `discord.py` 2.x
-   Pillow

Install dependencies:

``` bash
py -m pip install -U discord.py Pillow
```

### Files

Place the bot script and its background image in the same folder:

``` text
discord-bot/
├── bot.py
├── background.jpg
├── README.md
└── .gitignore
```

The current script loads `background.jpg` at startup and resizes it to
900 × 300 pixels. Keep this file beside the script.

### Discord application settings

1.  Create or select your application in the [Discord Developer
    Portal](https://discord.com/developers/applications).
2.  In **Bot → Privileged Gateway Intents**, enable **Server Members
    Intent** and **Message Content Intent**.
3.  Invite the bot using the OAuth2 scopes `bot` and
    `applications.commands`.

The bot may need these server permissions, depending on the features you
use:

-   View Channels, Send Messages, and Read Message History
-   Attach Files
-   Manage Roles and Manage Channels
-   Manage Messages
-   Moderate Members

Move the bot's highest role above `Verified` and `Unverified` in the
server role list. Discord role hierarchy can otherwise prevent role
assignment.

## Configuration

### Keep the token out of source control

Replace the hard-coded token assignment with an environment variable:

``` python
import os

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Set the DISCORD_TOKEN environment variable.")
```

In Windows Command Prompt:

``` cmd
set DISCORD_TOKEN=YOUR_BOT_TOKEN
py bot.py
```

In PowerShell:

``` powershell
$env:DISCORD_TOKEN = "YOUR_BOT_TOKEN"
py bot.py
```

These examples set the variable for the current terminal session. Do not
commit a real token to GitHub. If a token has already been exposed,
reset it in the Developer Portal.

### Run

From the project folder:

``` cmd
py bot.py
```

On startup, the bot logs in and synchronizes its application commands.

## Commands

  --------------------------------------------------------------------------
  Command                    Purpose                 Permission
  -------------------------- ----------------------- -----------------------
  `/verify`                  Starts the CAPTCHA      Server member
                             verification process in 
                             `#verify`.              

  `/flush amount:<number>`   Deletes between 1 and   Manage Messages
                             100 recent messages in  
                             the current channel.    
  --------------------------------------------------------------------------

### Verification flow

1.  A member joins and receives the `Unverified` role.
2.  The bot posts a welcome image and directs the member to `#verify`.
3.  The member runs `/verify` and receives a CAPTCHA image ephemerally.
4.  The member types the answer in `#verify`.
5.  If the answer matches exactly, `Verified` is added and `Unverified`
    is removed.

## Configuration reference

These constants control the moderation thresholds in the current script:

  --------------------------------------------------------------------------
  Constant                                     Default Meaning
  ----------------------- ---------------------------- ---------------------
  `TIMEOUT_MINUTES`                               `30` Timeout duration
                                                       after detected spam

  `SPAM_INTERVAL`                         `10` seconds Time window for
                                                       repeated text

  `SPAM_THRESHOLD`                        `3` messages Repeated-text
                                                       threshold

  `PUNISHMENT_COOLDOWN`                   `30` seconds Cooldown between
                                                       text-spam punishments
                                                       for a member

  `IMAGE_THRESHOLD`                       `3` messages Attachment-message
                                                       threshold

  `IMAGE_INTERVAL`                        `10` seconds Time window for
                                                       attachment spam
  --------------------------------------------------------------------------

Change these values in the script to tune moderation. CAPTCHA length is
set by `generate_captcha(length=6)`.

## Implementation notes

-   **CAPTCHA input is not ephemeral.** The image and bot replies are
    ephemeral, but `bot.wait_for("message")` collects the answer as a
    regular message in `#verify`.
-   **Channel permissions are changed on member join.** The current code
    creates or edits `#welcome` and `#verify`, and hides other channels
    from `Unverified`. Test this behavior in a separate server before
    using it in an existing community.
-   **Spam history is stored in memory.** Counts and cooldown state
    reset when the bot restarts.
-   **Moderation can fail without permissions.** The bot needs suitable
    permissions and role hierarchy; errors are printed to the console.
-   **Font fallback is included.** The code attempts to load `arial.ttf`
    and falls back to Pillow's default font if unavailable.

## First-run checklist

-   [ ] Set `DISCORD_TOKEN` as an environment variable.
-   [ ] Enable both privileged intents in the Developer Portal.
-   [ ] Put `background.jpg` beside the script.
-   [ ] Place the bot role above `Verified` and `Unverified`.
-   [ ] Test verification and channel visibility in a test server.
-   [ ] Test `/flush` using an account with Manage Messages permission.

## License

No license is specified by the code itself. Before publishing, choose a
license and add its full text in a `LICENSE` file. The MIT License is
one common option if you want to allow reuse, modification, and
redistribution.
