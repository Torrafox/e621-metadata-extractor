import os
import time
import polars as pl
from tqdm import tqdm
from e621_metadata_extractor.utils import calculate_md5

def process_directory(directory, posts_dump_path, tags_dump_path, output_csv_path, export_json=False):
    """
    Processes files in a directory, matches them with e621 metadata, and writes to a CSV.
    Optionally exports the results to a JSON file if export_json is True.
    """
    # Load the CSV dump into a pandas DataFrame
    print("Loading the CSV dump (this can take a minute)...")
    try:
        posts_csv_data = pl.read_csv(posts_dump_path)
        md5_to_row_map = {row["md5"]: row for row in posts_csv_data.to_dicts()} # Create a dictionary for fast lookups

        tags_csv_data = pl.read_csv(tags_dump_path)
        tags_csv_data_filtered = tags_csv_data.filter(pl.col("category") == 1) # Filter out non-artist tags
        tag_names_set = set(tags_csv_data_filtered["name"].to_list()) # Create a set for fast lookups
    except Exception as e:
        print(f"Error loading CSV dump: {e}")
        return

    # Create a list to store matching file data
    results = []

    # Collect all file paths from the directory for progress tracking
    print(f"Scanning directory: {directory}...")
    all_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if os.path.isfile(os.path.join(root, file))
    ]

    # Start the timer
    start_time = time.time()

    # Process files with tqdm for a single-line progress bar
    with tqdm(total=len(all_files), desc="Processing files", unit="file") as progress_bar:
        for file_path in all_files:
            file_md5 = calculate_md5(file_path)
            if not file_md5:
                progress_bar.update(1)
                continue

            row = md5_to_row_map.get(file_md5, None)
            if not row:
                progress_bar.update(1)
                continue

            # Add a "post_url" column dynamically
            row["post_url"] = f"https://e621.net/posts/{row['id']}"

            # Split the tags string into individual tags
            tags_list = row["tag_string"].split()

            # Use list comprehension to filter matching tags, excluding specific tags
            excluded_tags = {
                "avoid_posting",
                "conditional_dnp",
                "epilepsy_warning",
                "jumpscare_warning",
                "motion_sickness_warning",
                "sound_warning",
                "third-party_edit",
                "unknown_artist"
            }

            artist_tags = [
                tag.replace("_(artist)", "")  # Remove the suffix _(artist)
                for tag in tags_list
                if tag in tag_names_set and tag not in excluded_tags
            ]

            # Join the artist tags back into a space-separated string
            artist_string = " ".join(artist_tags)

            # Add a "artist_string" column to the row
            row["artist_string"] = artist_string

            # Append the entire row (with the new column) to the results
            results.append(row)

            # Extract the required columns
            # extracted_data = {
            #     "id": row["id"],
            #     "created_at": row["created_at"],
            #     "md5": row["md5"],
            #     "file_ext": row["file_ext"],
            #     "source": row["source"],
            #     "rating": row["rating"],
            #     "tag_string": row["tag_string"],
            #     "description": row["description"],
            #     "post_url": f"https://e621.net/posts/{row['id']}",
            #     "artist_string": artist_string
            # }
            # results.append(extracted_data)

            progress_bar.update(1)

    # Save results to a new CSV file
    elapsed_time = time.time() - start_time
    if results:
        print(f"\nWriting results to {output_csv_path}...")
        results_df = pl.DataFrame(results)
        results_df = results_df.sort("id")
        results_df.write_csv(output_csv_path)
        print(f"Processing complete! Results saved to {output_csv_path}.")

        # Optionally save results to a JSON file
        if export_json:
            output_json_path = output_csv_path.replace(".csv", ".json")
            print(f"Writing results to {output_json_path}...")
            results_df.write_json(output_json_path)
            print(f"Results also saved to {output_json_path}.")
    else:
        print("\nNo matching files found.")

    print(f"Total time elapsed: {elapsed_time:.2f} seconds")