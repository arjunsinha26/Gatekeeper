# GateKeeper

GateKeeper is a Discord security and verification bot built with `discord.py`.

It protects servers from spam, image flooding, and unauthorized access while providing an automated verification system.

## Features

- CAPTCHA verification system
- Automatic VERIFIED / UNVERIFIED roles
- Auto-created `#welcome` and `#verify` channels
- Custom welcome images
- Anti text spam protection
- Anti image spam protection
- Automatic 30-minute timeouts
- Bulk message deletion command

## Commands

### `/verify`
Verify yourself using CAPTCHA.

### `/flush <amount>`
Delete messages from a channel.

Example:
```text
/flush 50
```

## Requirements

```bash
pip install -r requirements.txt
```

## Run Bot

```bash
python bot.py
```

## Technologies

- Python
- discord.py
- Pillow
