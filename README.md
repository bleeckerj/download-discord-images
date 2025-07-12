# Download Discord Images

This repository contains a script to download images from a specified Discord channel.

## Setup Instructions

1. Clone this repository:

   ```bash
   git clone https://github.com/NearFutureLaboratory/download-discord-channel-images.git
   ```

2. Install the required dependencies:

   * If a `requirements.txt` exists, run:

     ```bash
     pip install -r requirements.txt
     ```

   * Otherwise, install dependencies manually as needed.

3. Create a `config.json` file in the root directory with the following structure:

   ```json
   {
       "token": "YOUR_DISCORD_BOT_TOKEN",
       "image_dir_root": "./images",
       "delay_secs": 5,
       "loop_delay_secs": 0.1,
       "channel_id": YOUR_CHANNEL_ID,
       "message_quantity": 10000,
       "after_id": 0
   }
   ```

   Replace `YOUR_DISCORD_BOT_TOKEN` with your Discord bot token, and `YOUR_CHANNEL_ID` with the target channel ID.

4. Ensure your bot has the necessary permissions:

   * Read Message History
   * Read Messages
   * Download Attachments

5. Run the script:

   ```bash
   python3 download_images_from_discord_channel.py
   ```

## File Organization

The script organizes downloaded files in a hierarchical structure:

```
/image_dir_root/
  /channel_name_CHANNEL_ID/
    /images/
      /YEAR/
        /MONTH/
          YYYYMMDD_HHMM_MESSAGE_ID_filename.png
    /json/
      /YEAR/
        /MONTH/
          YYYYMMDD_HHMM_MESSAGE_ID_filename.json
```

This organization helps manage large collections and maintain relationships between JSON metadata and image files.

* **Images**: Stored in year/month subdirectories for easy navigation
* **JSON Files**: Each JSON file contains metadata about the corresponding image, including:
  - Message content
  - Author information
  - Creation date
  - Message URL
  - Relative and absolute paths to the image file

## Security Notes

* Keep your Discord token private. Do not share it or commit it to version control.
* Use environment variables or secure vaults for production deployments.

## Usage Tips

* Adjust `message_quantity` to control how many messages to process.
* Modify `delay_secs` and `loop_delay_secs` to manage rate limiting.
* The script will save images and message details in the specified `image_dir_root`.
* Existing files will be updated or moved to the proper directory structure automatically.
* The `after_id` parameter can be used to start collecting from a specific message ID.

## How to Obtain a Discord Bot Token

1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).

2. Click on **"New Application"** and give it a name.

3. Select your application, then go to the **"Bot"** tab on the left sidebar.

4. Click **"Add Bot"** and confirm.

5. Under the **"Token"** section, click **"Copy"** to copy your bot token.

6. **Important:** Keep this token private. Do not share it or commit it to version control.

7. Paste the token into your `config.json` file in place of `"YOUR_DISCORD_BOT_TOKEN"`.

## License

This project is licensed under the MIT License.