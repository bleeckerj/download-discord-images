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
        #break  # Break after the first message
    
    
    
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
    after_id = config["after_id"]
    loop_count = 0
    count = 0
    while True:
        messages_fetched = 0

        async for message in channel.history(limit=100, after=discord.Object(id=after_id) if after_id else None):               
            messages_fetched += 1
            count += 1
            timestamp = message.created_at.strftime('%m/%d/%Y @ %H:%M:%S')
            #print(f"{timestamp}")
            
            # Construct the URL to the message
            message_url = f"https://discord.com/channels/{message.guild.id if message.guild else '@me'}/{message.channel.id}/{message.id}"

            
            if message_count >= MESSAGE_QUANTITY:
                break
            
            formatted = "{:03d}".format(count)
            fetched_count = "{:03d}".format(messages_fetched)
            difference = first_created_at - message.created_at

            # Get the number of days from the difference
            number_of_days = abs(difference.days)  # Use abs to get the absolute value
            print(f"Count[{fetched_count}] @ {timestamp} and {difference} days to go...")

            for attachment in message.attachments:
                if any(attachment.filename.endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']):
                    response = requests.get(attachment.url)
                    
                    timestamp = message.created_at.strftime('%Y%m%d_%H%M')
                    formatted_filename = f"{timestamp}_{message.id}_{attachment.filename}"


                    file_path = os.path.join(channel_dir, formatted_filename)  # Replace with your save path
                    
                    if os.path.exists(file_path):
                        print(f"File {file_path} already exists. Skipping")
                        continue
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f'From {message_url}')
                    print(f"{attachment.filename}")
                    # Save message details in a JSON file
                    message_details = {
                        "author": str(message.author),
                        "content": message.content,
                        "created_at": str(message.created_at),
                        "id": str(message.id),
                        "channel_id": str(channel.id),
                        "channel_name": str(channel_name),
                        "attachments": [attachment.url for attachment in message.attachments],
                        "message_url" : message_url
                    }
                    json_file_path = os.path.join(channel_dir, f"{timestamp}_{message.id}_{attachment.filename}".replace(attachment.filename.split('.')[-1], 'json'))
                    
                    if os.path.exists(json_file_path):
                        print(f"File {json_file_path} already exists. Skipping")
                        # response = input(f"File {json_file_path} already exists. Do you want to overwrite it? (yes/no): ")
                        # if response.lower() != 'yes':
                        #     print("Operation aborted.")
                        #     sys.exit(None)
                        # Halt the program, exit or handle the situation as per your requirement
                        # For example, you can raise an exception to halt the program:
                        # raise FileExistsError(f"File {json_file_path} already exists.")
                    else:
                        with open(json_file_path, 'w') as json_file:
                            json.dump(message_details, json_file, indent=4)
                        print(f'Saved message details as JSON for {attachment.filename}')                    
                        
            if message_count >= MESSAGE_QUANTITY:
                break
            
            if message.id == first_message_id:
                print("Reached the start of the channel. Exiting loop.")
                return  # Use return to exit the on_ready function, thus breaking the loop

            # if message.id == last_message_id:
            #     print("End of the channel!")
            #     return

            earliest_message_id = message.id

            # if messages_fetched < 100:
            # # Break the loop if there were less than 100 messages in the last fetch,
            # # indicating we have reached the beginning of the channel history
            #     break

            # Delay after every 100 loops
            if loop_count >= LOOP_COUNTER:
                print(f"Pausing for {DELAY_SECONDS} seconds...")
                await asyncio.sleep(DELAY_SECONDS)
                loop_count = 0  # Reset the loop counter
            await asyncio.sleep(LOOP_DELAY_SECONDS)


client.run(config['token'])  # Replace with your bot token
