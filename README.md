# Download Discord Images

This repository contains a script to download images from a specified Discord channel.

## Setup Instructions

1. Clone this repository:

   ```bash
   git clone https://github.com/bleeckerj/download-discord-images.git
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
   python3 chesterbot_download_images.py
   ```

## Security Notes

* Keep your Discord token private. Do not share it or commit it to version control.
* Use environment variables or secure vaults for production deployments.

## Usage Tips

* Adjust `message_quantity` to control how many messages to process.
* Modify `delay_secs` and `loop_delay_secs` to manage rate limiting.
* The script will save images and message details in the specified `image_dir_root`.

## License

This project is licensed under the MIT License.