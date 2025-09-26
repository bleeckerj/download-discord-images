import os
import json

# Set this to your images root directory (e.g., './images')
IMAGES_ROOT = './images'
# Output file
OUTPUT_FILE = 'channels_last_ids.json'

def find_json_files(root_dir):
    """Recursively find all JSON files under root_dir."""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.json'):
                yield os.path.join(dirpath, filename)

def get_channel_and_id(json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        channel_id = str(data.get('channel_id'))
        message_id = int(data.get('id'))
        return channel_id, message_id
    except Exception as e:
        print(f"Error reading {json_path}: {e}")
        return None, None

def main():
    channel_last_ids = {}
    for json_file in find_json_files(IMAGES_ROOT):
        channel_id, message_id = get_channel_and_id(json_file)
        if channel_id and message_id:
            if channel_id not in channel_last_ids or message_id > channel_last_ids[channel_id]:
                channel_last_ids[channel_id] = message_id
    # Prepare output as array of objects
    output = [
        {"channel_id": cid, "last_id": str(last_id)}
        for cid, last_id in channel_last_ids.items()
    ]
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=4)
    print(f"Wrote {len(output)} channels to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
