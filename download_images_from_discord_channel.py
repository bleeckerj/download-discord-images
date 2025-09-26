
import discord
import requests
import os
import json
import asyncio
import sys
from datetime import datetime
import logging

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True

client = discord.Client(intents=intents)

# Load config.json
with open('./config.json', 'r') as file:
    config = json.load(file)

# Load channels_last_ids.json
with open('./channels_last_ids.json', 'r') as f:
    channels_info = json.load(f)

MESSAGE_QUANTITY = config["message_quantity"]
DELAY_SECONDS = config["delay_secs"]
LOOP_COUNTER = 50
LOOP_DELAY_SECONDS = config["loop_delay_secs"]
IMAGE_DIR_ROOT = config["image_dir_root"]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


async def process_channel(channel_id, after_id):
    channel = client.get_channel(int(channel_id))
    channel_name = getattr(channel, 'name', f'channel_{channel_id}')
    channel_dir = os.path.join(IMAGE_DIR_ROOT, f'{channel_name}_{channel_id}')
    os.makedirs(channel_dir, exist_ok=True)

    logger.info(f'Processing channel {channel_name} ({channel_id}) starting after {after_id}')

    # Fetch the first message in the channel's history
    first_created_at = None
    async for message in channel.history(limit=1, oldest_first=True):
        first_created_at = message.created_at
        break

    async for last_message in channel.history(limit=1):
        last_message_id = last_message.id if last_message else None

    async for first_message in channel.history(limit=1, oldest_first=True):
        first_message_id = first_message.id if first_message else None

    message_count = 0
    loop_count = 0
    count = 0
    newest_id = after_id
    while True:
        messages_fetched = 0
        history_params = {
            'limit': 100,
            'oldest_first': False
        }
        if after_id:
            history_params['after'] = discord.Object(id=after_id)

        async for message in channel.history(**history_params):
            messages_fetched += 1
            count += 1
            message_count += 1
            timestamp = message.created_at.strftime('%m/%d/%Y @ %H:%M:%S')
            try:
                if hasattr(message, 'to_dict'):
                    logger.info(f"Full message object: {json.dumps(message.to_dict(), indent=2)}")
                else:
                    logger.info(f"Full message object: {str(message)}")
            except Exception as e:
                logger.info(f"Error logging full message object: {e}")

            if not newest_id or int(message.id) > int(newest_id):
                newest_id = message.id

            message_url = f"https://discord.com/channels/{message.guild.id if message.guild else '@me'}/{message.channel.id}/{message.id}"

            if message_count >= MESSAGE_QUANTITY:
                break

            formatted = "{:03d}".format(count)
            fetched_count = "{:03d}".format(messages_fetched)
            difference = first_created_at - message.created_at

            if first_created_at:
                number_of_days = abs(difference.days)
                logger.info(f"Count[{fetched_count}] @ {timestamp} and {difference} days to go...")
            else:
                logger.info(f"Count[{fetched_count}] @ {timestamp} - Processing message {message.id}")

            for attachment in message.attachments:
                logging.debug(f"Attachment Json: {json.dumps(attachment.to_dict(), indent=2)}")
                logging.info(f"Processing attachment: {attachment.filename}")
                logging.debug(f"Attachment URL: {attachment.url}")
                logging.debug(f"Attachment Filename Ends With: {attachment.filename.split('.')[-1]}")
                if any(attachment.filename.lower().endswith(ext) for ext in [
                    'mp4', 'mov', 'avi', 'mkv', 'webm', 'm4v', 'mpg', 'mpeg', 'wmv', 'flv', '3gp',
                    'png', 'jpg', 'jpeg', 'gif', 'webp']):
                    response = requests.get(attachment.url)

                    timestamp = message.created_at.strftime('%Y%m%d_%H%M')
                    year_month = message.created_at.strftime('%Y/%m')
                    formatted_filename = f"{timestamp}_{message.id}_{attachment.filename}"

                    image_subdir = os.path.join(channel_dir, "images", year_month)
                    os.makedirs(image_subdir, exist_ok=True)

                    file_path = os.path.join(image_subdir, formatted_filename)

                    if os.path.exists(file_path):
                        logger.info(f"File {file_path} already exists. Skipping")
                        continue
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    logger.info(f'From {message_url}')
                    logger.info(f"{attachment.filename}")
                    logger.info(f"Downloaded attachment: {attachment.filename} from {attachment.url}")

                    relative_path = os.path.join("images", year_month, formatted_filename)

                    message_details = {
                        "author": str(message.author),
                        "content": message.content,
                        "created_at": str(message.created_at),
                        "id": str(message.id),
                        "channel_id": str(channel.id),
                        "channel_name": str(channel_name),
                        "attachments": [attachment.url for attachment in message.attachments],
                        "message_url": message_url,
                        "downloaded_filename": formatted_filename,
                        "image_path": relative_path,
                        "full_path": file_path
                    }

                    json_year_month = message.created_at.strftime('%Y/%m')
                    json_subdir = os.path.join(channel_dir, "json", json_year_month)
                    os.makedirs(json_subdir, exist_ok=True)

                    json_filename = f"{timestamp}_{message.id}_{attachment.filename}".replace(attachment.filename.split('.')[-1], 'json')

                    new_json_path = os.path.join(json_subdir, json_filename)
                    old_json_path = os.path.join(channel_dir, json_filename)

                    if os.path.exists(old_json_path):
                        logger.info(f"Found JSON in old location: {old_json_path}")
                        if not os.path.exists(new_json_path):
                            os.makedirs(os.path.dirname(new_json_path), exist_ok=True)
                            os.rename(old_json_path, new_json_path)
                            logger.info(f"Moved JSON from {old_json_path} to {new_json_path}")
                        else:
                            logger.info(f"JSON already exists at new location. Skipping move.")

                    message_details["json_path"] = os.path.join("json", json_year_month, json_filename)

                    if os.path.exists(new_json_path):
                        logger.info(f"JSON file {new_json_path} already exists. Updating...")
                        with open(new_json_path, 'w') as json_file:
                            json.dump(message_details, json_file, indent=4)
                        logger.info(f"Updated JSON metadata for {attachment.filename}")
                    else:
                        with open(new_json_path, 'w') as json_file:
                            json.dump(message_details, json_file, indent=4)
                        logger.info(f'Saved message details as JSON for {attachment.filename}')
                else:
                    logger.warning(f"Skipping unsupported attachment type: {attachment.filename}")
                    logger.warning(f"Unsupported attachment with filename extension: {attachment.filename.split('.')[-1]}")
            if message_count >= MESSAGE_QUANTITY:
                break

            if message.id == first_message_id:
                logger.info("Reached the start of the channel. Exiting loop.")
                return

            if message.id == last_message_id:
                logger.info("Reached the newest message in the channel. Exiting loop.")
                return

            earliest_message_id = message.id

        if messages_fetched == 0:
            logger.info("No messages fetched in this batch. Exiting.")
            break

        if newest_id and (after_id is None or newest_id != after_id):
            logger.info(f"Updated after_id to {newest_id} for next batch")
            after_id = newest_id
        else:
            logger.info("No new messages found (IDs not advancing). Exiting.")
            break

        if message_count >= MESSAGE_QUANTITY:
            logger.info(f"Reached message quantity limit of {MESSAGE_QUANTITY}. Exiting.")
            break

        if messages_fetched == 0:
            logger.info("No more messages to fetch. Exiting.")
            break

        if message_count > MESSAGE_QUANTITY * 2:
            logger.info(f"Processed {message_count} messages, which is more than double the requested quantity. Stopping as a safety measure.")
            break

        if loop_count >= LOOP_COUNTER:
            logger.info(f"Pausing for {DELAY_SECONDS} seconds...")
            await asyncio.sleep(DELAY_SECONDS)
            loop_count = 0
        loop_count += 1
        await asyncio.sleep(LOOP_DELAY_SECONDS)


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}')
    for channel in channels_info:
        channel_id = channel['channel_id']
        after_id = channel['last_id']
        await process_channel(channel_id, after_id)
    await client.close()

client.run(config['token'])
