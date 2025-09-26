# 📥 Download Discord Images

This repository contains utilities to download images from one or more Discord channels, organize metadata, and manage download progress across multiple channels.

## 🚀 Multi-Channel Setup & Utilities

### 1️⃣ Find Last IDs for All Channels

Use `find_last_ids_per_channel.py` to scan your images directory and build a summary of all channels and their latest downloaded message IDs. This helps automate and track progress for each channel.

**Usage:**
```bash
python3 find_last_ids_per_channel.py
```
This will create a file called `channels_last_ids.json` containing an array of objects:
```json
[
  { "channel_id": "123456789012345678", "last_id": "987654321098765432" },
  ...
]
```

### 2️⃣ Download Images from Multiple Channels

The main script `download_images_from_discord_channel.py` now supports downloading from multiple channels in one run! It reads `channels_last_ids.json` and processes each channel serially, starting from the last downloaded message for each channel.

**Features:**
- 🔄 Processes all channels listed in `channels_last_ids.json`, in order
- 📝 Extensive logging: tracks which channel is being processed, progress, and status updates
- 🗂️ Organizes images and metadata in per-channel/year/month folders
- 🛡️ Automatically skips already-downloaded files and updates metadata
- ⏱️ Respects rate limits and delays as configured in `config.json`

**Config File (`config.json`)**
Still required for shared settings:
* `token` (Discord bot token)
* `image_dir_root` (root directory for images)
* `message_quantity` (max messages per channel)
* `delay_secs`, `loop_delay_secs` (rate limiting)

**How it works:**
1. Run `find_last_ids_per_channel.py` to generate/update `channels_last_ids.json`.
2. Run `download_images_from_discord_channel.py` to process all channels and download new images/messages.

---

This repository contains a script to download images from a specified Discord channel.

## 🛠️ Setup Instructions

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
       "after_id": "oldest"
   }
   ```

  Replace `YOUR_DISCORD_BOT_TOKEN` with your Discord bot token. The script will use `channels_last_ids.json` for channel IDs and starting points.

4. Ensure your bot has the necessary permissions:

   * Read Message History
   * Read Messages
   * Download Attachments

5. Run the script:

   - To update channel progress:
     ```bash
     python3 find_last_ids_per_channel.py
     ```
   - To download images from all channels:
     ```bash
     python3 download_images_from_discord_channel.py
     ```

## 🗂️ File Organization

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


## Data to Books

Look to the repository `https://github.com/bleeckerj/Files2Book.git` if you want to convert the JSON dumps from this into something useful or at least fun, like a book. In particular `README_preprocess_mj_json.md` in that repo.


## Security Notes

* Keep your Discord token private. Do not share it or commit it to version control.
* Use environment variables or secure vaults for production deployments.

## 💡 Usage Tips

- Use `find_last_ids_per_channel.py` regularly to keep `channels_last_ids.json` up to date.
- The downloader will process all channels in `channels_last_ids.json` in order, starting from the last downloaded message for each.
- Logging will show which channel is being processed and progress for each.

* Adjust `message_quantity` to control how many messages to process.
* Modify `delay_secs` and `loop_delay_secs` to manage rate limiting.
* The script will save images and message details in the specified `image_dir_root`.
* Existing files will be updated or moved to the proper directory structure automatically.
* The `after_id` parameter can be used to start collecting from a specific message ID:
  - Use a specific message ID to start after that message
  - Use `"oldest"` to start from the absolute beginning of the channel
  - Use a numeric ID to start after that specific message

## 🔑 How to Obtain a Discord Bot Token

1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).

2. Click on **"New Application"** and give it a name.

3. Select your application, then go to the **"Bot"** tab on the left sidebar.

4. Click **"Add Bot"** and confirm.

5. Under the **"Token"** section, click **"Copy"** to copy your bot token.

6. **Important:** Keep this token private. Do not share it or commit it to version control.

7. Paste the token into your `config.json` file in place of `"YOUR_DISCORD_BOT_TOKEN"`.

## 🤖 Creating a Discord Bot

A bit beyond the context here to provide instructions for creating a Discord Bot. There are plenty of tutorials out there in the world, cf: https://www.youtube.com/watch?v=YD_N6Ffoojw

## License

This project is licensed under the MIT License.