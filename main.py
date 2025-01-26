import os
import sys
import json
from e621_metadata_extractor.fetcher import get_latest_dump_url, download_file
from e621_metadata_extractor.extractor import process_directory

def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as config_file:
        return json.load(config_file)

def main():
    # Get data directory from config
    gallery_path = CONFIG.get("data_directory")

    # Check if the path is valid
    if not gallery_path or not os.path.isdir(gallery_path):
        print(f"Error: Data directory '{gallery_path}' not found or invalid.")
        sys.exit(1)

    print(f"Data directory validated: {gallery_path}")
    
    # Fetch the latest dump URL
    dump_url = get_latest_dump_url()
    if not dump_url:
        print("Could not fetch the latest database dump URL. Exiting.")
        sys.exit(1)
    
    # Construct the full save path for the file
    file_name = dump_url.split('/')[-1]
    save_path = file_name # Save in project directory
    #save_path = os.path.join(gallery_path, file_name) # Save in gallery directory
    
    # Download the file; skip if already downloaded
    if os.path.exists(save_path):
        print(f"Database dump already downloaded: {save_path}")
    else:
        print("Starting the download of the latest database dump...")
        download_file(dump_url, save_path)

    output_csv_name = "e621_metadata.csv"
    output_csv_path = output_csv_name # Save in project directory
    #output_csv_path = os.path.join(gallery_path, output_csv_name) # Save in gallery directory
    export_json = CONFIG.get("export_json", False)

    process_directory(gallery_path, save_path, output_csv_path, export_json)

if __name__ == "__main__":
    try:
        CONFIG = load_config()
        main()
    except Exception as e:
        print(f"Error: {e}")
