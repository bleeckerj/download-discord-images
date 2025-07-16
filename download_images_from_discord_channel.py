import discord
import requests
import os
import json
import asyncio
import sys
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True  # Enables receiving messages
intents.dm_messages = True  # Enables receiving DM messages

client = discord.Client(intents=intents)

# Open the JSON file and load its content
with open('./config.json', 'r') as file:
    config = json.load(file)
# Configuration
#YOUR_CHANNEL_ID = 980108517929283604
#YOUR_CHANNEL_ID = 1089358474426712224  # Replace with your channel ID
YOUR_CHANNEL_ID = config["channel_id"]
START_MESSAGE_ID = 0  # Set to 0 to start from the beginning, or specific message ID to start from that message
MESSAGE_QUANTITY = config["message_quantity"] # Number of messages to examine
DELAY_SECONDS = config["delay_secs"]
LOOP_COUNTER = 50  # Number of loops after which to introduce a delay
LOOP_DELAY_SECONDS = config["loop_delay_secs"]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(YOUR_CHANNEL_ID)
    channel_name = getattr(channel, 'name', 'midjourney_g')
    image_dir_root = config['image_dir_root']
    channel_dir = image_dir_root+'/'+channel_name+"_"+str(YOUR_CHANNEL_ID)+"/"
    # Ensure the directory to save images exists
    os.makedirs(channel_dir, exist_ok=True)  # Replace with your save path

    # Fetch the first message in the channel's history
    first_created_at = None
    async for message in channel.history(limit=1, oldest_first=True):
        # Convert message to a dictionary and then to a JSON string
        message_details = {
            "author": str(message.author),
            "content": message.content,
            "created_at": str(message.created_at),
            "id": str(message.id),
            "attachments": [attachment.url for attachment in message.attachments]
        }
        message_json = json.dumps(message_details, indent=4)
        print(message_json)
        print(f"First message created at {message.created_at}")
        first_created_at = message.created_at
        break  # Break after the first message to ensure we get only one
    
    
    
    # Fetch the most recent message ID
    async for last_message in channel.history(limit=1):
        last_message_id = last_message.id if last_message else None

    first_message_id = 0
    # Fetch the earliest message ID
    async for first_message in channel.history(limit=1, oldest_first=True):
        first_message_id = first_message.id if first_message else None

    print(f"First message ID in the channel: {first_message_id}")
    print(f"Last message ID in the channel: {last_message_id}")
    # Start processing messages
    reached_start = START_MESSAGE_ID == 0
    message_count = 0
    
    # Set after_id based on config or command line arguments
    # If after_id is set to "oldest", we'll start from the beginning
    start_from_oldest = False
    if "after_id" in config and config["after_id"] == "oldest":
        after_id = None  # None means start from the beginning
        start_from_oldest = True
        print("Starting from the oldest message in the channel")
    else:
        after_id = config["after_id"]
        print(f"Starting after message ID: {after_id}")
        
    loop_count = 0
    count = 0
    while True:
        messages_fetched = 0
        newest_id = after_id  # Track the newest message ID in this batch

        # Configure history parameters based on our mode
        if start_from_oldest:
            # When starting from oldest, use oldest_first=True for first batch
            # For subsequent batches, use after=newest_id to continue in chronological order
            history_params = {
                'limit': 100,
                'oldest_first': True if after_id is None else False
            }
            
            # After the first batch, use the after_id parameter to continue from where we left off
            if after_id is not None:
                history_params['after'] = discord.Object(id=after_id)
                # Turn off oldest_first after first batch
                history_params['oldest_first'] = False
        else:
            # Normal mode: fetch messages after the given ID
            history_params = {
                'limit': 100,
                'oldest_first': False
            }
            if after_id:
                history_params['after'] = discord.Object(id=after_id)
            
        async for message in channel.history(**history_params):               
            messages_fetched += 1
            count += 1
            message_count += 1  # Increment message_count to track progress toward MESSAGE_QUANTITY
            timestamp = message.created_at.strftime('%m/%d/%Y @ %H:%M:%S')
            #print(f"{timestamp}")
            
            # Keep track of the newest message ID we've seen
            if not newest_id or int(message.id) > int(newest_id):
                newest_id = message.id
            
            # Construct the URL to the message
            message_url = f"https://discord.com/channels/{message.guild.id if message.guild else '@me'}/{message.channel.id}/{message.id}"
            
            if message_count >= MESSAGE_QUANTITY:
                break
            
            formatted = "{:03d}".format(count)
            fetched_count = "{:03d}".format(messages_fetched)
            difference = first_created_at - message.created_at

            # Get the number of days from the difference (if first_created_at is available)
            if first_created_at:
                number_of_days = abs(difference.days)  # Use abs to get the absolute value
                print(f"Count[{fetched_count}] @ {timestamp} and {difference} days to go...")
            else:
                print(f"Count[{fetched_count}] @ {timestamp} - Processing message {message.id}")

            for attachment in message.attachments:
                if any(attachment.filename.endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']):
                    response = requests.get(attachment.url)
                    
                    timestamp = message.created_at.strftime('%Y%m%d_%H%M')
                    year_month = message.created_at.strftime('%Y/%m')
                    formatted_filename = f"{timestamp}_{message.id}_{attachment.filename}"

                    # Create year/month directory structure
                    image_subdir = os.path.join(channel_dir, "images", year_month)
                    os.makedirs(image_subdir, exist_ok=True)
                    
                    # Update file path to include the year/month structure
                    file_path = os.path.join(image_subdir, formatted_filename)
                    
                    if os.path.exists(file_path):
                        print(f"File {file_path} already exists. Skipping")
                        continue
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f'From {message_url}')
                    print(f"{attachment.filename}")
                    
                    # Maintain the relative path for referencing
                    relative_path = os.path.join("images", year_month, formatted_filename)
                    
                    # Save message details in a JSON file
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
                    
                    # Create JSON year/month directory structure (similar to images)
                    json_year_month = message.created_at.strftime('%Y/%m')
                    json_subdir = os.path.join(channel_dir, "json", json_year_month)
                    os.makedirs(json_subdir, exist_ok=True)
                    
                    # Create JSON filename
                    json_filename = f"{timestamp}_{message.id}_{attachment.filename}".replace(attachment.filename.split('.')[-1], 'json')
                    
                    # New path for JSON in the organized directory structure
                    new_json_path = os.path.join(json_subdir, json_filename)
                    
                    # Old path (where JSON might already exist)
                    old_json_path = os.path.join(channel_dir, json_filename)
                    
                    # Check if JSON exists in old location
                    if os.path.exists(old_json_path):
                        print(f"Found JSON in old location: {old_json_path}")
                        # Move JSON to new location
                        if not os.path.exists(new_json_path):
                            os.makedirs(os.path.dirname(new_json_path), exist_ok=True)
                            os.rename(old_json_path, new_json_path)
                            print(f"Moved JSON from {old_json_path} to {new_json_path}")
                        else:
                            print(f"JSON already exists at new location. Skipping move.")
                    
                    # Update message_details with the new JSON path
                    message_details["json_path"] = os.path.join("json", json_year_month, json_filename)
                    
                    # Check if JSON exists in new location
                    if os.path.exists(new_json_path):
                        print(f"JSON file {new_json_path} already exists. Updating...")
                        # Update the JSON file
                        with open(new_json_path, 'w') as json_file:
                            json.dump(message_details, json_file, indent=4)
                        print(f"Updated JSON metadata for {attachment.filename}")
                    else:
                        # Create new JSON file
                        with open(new_json_path, 'w') as json_file:
                            json.dump(message_details, json_file, indent=4)
                        print(f'Saved message details as JSON for {attachment.filename}')
                        
            if message_count >= MESSAGE_QUANTITY:
                break
            
            # Only check for reaching the start when NOT starting from oldest
            if not start_from_oldest and message.id == first_message_id:
                print("Reached the start of the channel. Exiting loop.")
                return  # Use return to exit the on_ready function, thus breaking the loop

            # When starting from oldest, check if we've reached the newest message
            if start_from_oldest and message.id == last_message_id:
                print("Reached the newest message in the channel. Exiting loop.")
                return  # Exit function

            earliest_message_id = message.id

            # if messages_fetched < 100:
            # # Break the loop if there were less than 100 messages in the last fetch,
            # # indicating we have reached the beginning of the channel history
            #     break

        # Check if we actually processed any messages in this batch
        if messages_fetched == 0:
            print("No messages fetched in this batch. Exiting.")
            break
            
        # Update the after_id to the newest message ID in this batch
        if newest_id and (after_id is None or newest_id != after_id):
            # When using oldest_first=True, we need to use the newest ID to continue in chronological order
            if start_from_oldest:
                print(f"Processed batch of {messages_fetched} messages, continuing from ID {newest_id}")
                after_id = newest_id
            else:
                print(f"Updated after_id to {newest_id} for next batch")
                after_id = newest_id
        else:
            # If the newest ID is the same as our after_id, we're not progressing
            print("No new messages found (IDs not advancing). Exiting.")
            break
            
        # If we've reached the message quantity limit, exit
        if message_count >= MESSAGE_QUANTITY:
            print(f"Reached message quantity limit of {MESSAGE_QUANTITY}. Exiting.")
            break
            
        # This is redundant now since we check at the top of the loop
        # but keeping it for clarity
        if messages_fetched == 0:
            print("No more messages to fetch. Exiting.")
            break
            
        # Add a counter to prevent infinite loops
        # If we've processed more than double the MESSAGE_QUANTITY, something is wrong
        if message_count > MESSAGE_QUANTITY * 2:
            print(f"Processed {message_count} messages, which is more than double the requested quantity. Stopping as a safety measure.")
            break
            
        # Delay after every LOOP_COUNTER loops
        if loop_count >= LOOP_COUNTER:
            print(f"Pausing for {DELAY_SECONDS} seconds...")
            await asyncio.sleep(DELAY_SECONDS)
            loop_count = 0  # Reset the loop counter
        loop_count += 1  # Don't forget to increment the loop counter
        await asyncio.sleep(LOOP_DELAY_SECONDS)


client.run(config['token'])  # Replace with your bot token
