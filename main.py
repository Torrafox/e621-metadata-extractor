import os
import sys
import json
from e621_metadata_extractor.fetcher import get_latest_dump_urls, download_file
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
    
    # Fetch the latest dump URLs
    dump_urls = get_latest_dump_urls()
    if not dump_urls or not dump_urls.get("posts") or not dump_urls.get("tags"):
        print("Could not fetch the latest database dump URL. Exiting.")
        sys.exit(1)
    
    # Construct the full save paths for the files
    posts_dump_file_name = dump_urls.get("posts").split("/")[-1]
    tags_dump_file_name = dump_urls.get("tags").split("/")[-1]
    posts_dump_save_path = posts_dump_file_name # Save in project directory
    tags_dump_save_path = tags_dump_file_name # Save in project directory
    
    # Download the posts dump file; skip if already downloaded
    if os.path.exists(posts_dump_save_path):
        print(f"Database dump already downloaded: {posts_dump_save_path}")
    else:
        print("Starting the download of the latest database dump...")
        download_file(dump_urls.get("posts"), posts_dump_save_path)

    # Download the tags dump file; skip if already downloaded
    if os.path.exists(tags_dump_save_path):
        print(f"Database dump already downloaded: {tags_dump_save_path}")
    else:
        print("Starting the download of the latest database dump...")
        download_file(dump_urls.get("tags"), tags_dump_save_path)

    output_csv_name = "e621_metadata.csv"
    output_csv_path = output_csv_name # Save in project directory
    #output_csv_path = os.path.join(gallery_path, output_csv_name) # Save in gallery directory
    export_json = CONFIG.get("export_json", False)

    process_directory(gallery_path, posts_dump_save_path, tags_dump_save_path, output_csv_path, export_json)

if __name__ == "__main__":
    try:
        CONFIG = load_config()
        main()
    except Exception as e:
        print(f"Error: {e}")
