# Midjourney Discord Channel Bot Example

This script demonstrates how to use the Discord API (via the `discord.py` library) to connect a bot to Discord, fetch direct messages (DMs) from a specific user, and print their contents. It is intended as a starting point for building bots that interact with Midjourney or similar channels.

## Features

- Connects to Discord using a bot token.
- Fetches and prints the latest 100 direct messages from a specified user.
- Loads configuration from `config.json`.

## Setup

1. **Install dependencies:**
	```bash
	pip install discord.py
	```

2. **Configure your bot:**
	- Edit `config.json` and add your bot token and any other required fields.
	- Replace the placeholder user ID in the script with the actual Discord user ID you want to fetch messages from.

3. **Run the bot:**
	```bash
	python exampleOfAMidjourneyChannelBot.py
	```

## Configuration

The bot expects a `config.json` file in the root directory. Example:
```json
{
	 "token": "YOUR_DISCORD_BOT_TOKEN",
	 "image_dir_root": "./images",
	 "delay_secs": 5,
	 "loop_delay_secs": 0.2,
	 "channel_id": 123456789012345678,
	 "message_quantity": 100,
	 "after_id": "0"
}
```

## Notes

- Make sure your bot has permission to read messages and access DMs.
- Never share your Discord bot token publicly.
- This script is a minimal example and can be extended to download images, process messages, or interact with channels.
# Example: Midjourney Channel Bot

This README describes the purpose and functionality of `exampleOfAMidjourneyChannelBot.py`.

## Purpose

This script demonstrates how to connect a Discord bot to a specific channel (such as one used for Midjourney image generation) and process messages, including downloading media attachments.

## What It Does

- Connects to Discord using a bot token
- Monitors a specified channel for new messages
- Downloads attachments (images, videos, etc.) from messages
- Logs message and attachment details for inspection
- Can be adapted to archive or process Midjourney-generated content

## Features

- Handles common image and video formats (png, jpg, jpeg, gif, webp, mp4, mov, avi, mkv, webm, m4v, mpg, mpeg, wmv, flv, 3gp)
- Uses Python logging for detailed output
- Example structure for building more advanced Discord bots

## Usage

1. Set up a Discord bot and obtain a bot token
2. Configure the script with your channel ID and bot token
3. Run the script with Python 3
4. Check logs and output directories for downloaded media

## Requirements

- Python 3.7+
- `discord.py` library
- `requests` library

## Security Notes

- Keep your Discord bot token private
- Do not share or commit your token to public repositories

## License

MIT License
