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
