import discord
import asyncio
import json

# Open the JSON file and load its content
with open('./config.json', 'r') as file:
    config = json.load(file)


client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # Assume we have a user ID to fetch DM messages
    user_id = 123456789012345678  # Replace with the user's ID
    user = await client.fetch_user(user_id)

    # Open a DM channel with the user
    dm_channel = user.dm_channel
    if dm_channel is None:
        dm_channel = await user.create_dm()

    # Fetch messages from the DM channel
    async for message in dm_channel.history(limit=100):
        print(f"{message.created_at}: {message.content}")

client.run('YOUR_BOT_TOKEN')  # Replace with your bot token
