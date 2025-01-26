import os
import time
import pandas as pd
from tqdm import tqdm
from e621_metadata_extractor.utils import calculate_md5

def process_directory(directory, csv_dump_path, output_csv_path, export_json=False):
    """
    Processes files in a directory, matches them with e621 metadata, and writes to a CSV.
    Optionally exports the results to a JSON file if export_json is True.
    """
    # Load the CSV dump into a pandas DataFrame
    print("Loading the CSV dump (this can take a minute)...")
    try:
        csv_data = pd.read_csv(csv_dump_path, compression="gzip")
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
            # Calculate MD5 checksum for the current file
            file_md5 = calculate_md5(file_path)
            if not file_md5:
                progress_bar.update(1)
                continue

            # Search for the file's MD5 in the CSV dump
            matching_row = csv_data.loc[csv_data['md5'] == file_md5]
            if not matching_row.empty:
                # Convert the entire matching row into a dictionary
                row = matching_row.iloc[0].to_dict()

                # Add the "post_url" column dynamically
                row["post_url"] = f"https://e621.net/posts/{row['id']}"

                # Append the entire row (with the new column) to the results
                results.append(row)

                # Extract the required columns
                # row = matching_row.iloc[0]
                # extracted_data = {
                #     "id": row["id"],
                #     "created_at": row["created_at"],
                #     "md5": row["md5"],
                #     "file_ext": row["file_ext"],
                #     "source": row["source"],
                #     "rating": row["rating"],
                #     "tag_string": row["tag_string"],
                #     "description": row["description"],
                #     "post_url": f"https://e621.net/posts/{row['id']}"
                # }
                # results.append(extracted_data)

            # Update the progress bar
            progress_bar.update(1)

    # Save results to a new CSV file
    elapsed_time = time.time() - start_time
    if results:
        print(f"\nWriting results to {output_csv_path}...")
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_csv_path, index=False)
        print(f"Processing complete! Results saved to {output_csv_path}.")

        # Optionally save results to a JSON file
        if export_json:
            output_json_path = output_csv_path.replace(".csv", ".json")
            print(f"Writing results to {output_json_path}...")
            results_df.to_json(output_json_path, orient='records', lines=True)
            print(f"Results also saved to {output_json_path}.")
    else:
        print("\nNo matching files found.")

    print(f"Total time elapsed: {elapsed_time:.2f} seconds")