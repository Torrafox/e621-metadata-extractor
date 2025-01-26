# e621 Metadata Fetcher and Extractor

## Overview

**e621 Metadata Fetcher and Extractor** is a tool for downloading and processing metadata dumps from [e621](https://e621.net). It matches local files against the e621 metadata dump and generates a clean CSV file containing the relevant metadata.

This tool is useful for managing local galleries by providing metadata such as tags, ratings, descriptions, and more.


## Features

- Fetch the latest metadata dump from e621.
- Process local files in a directory by matching their MD5 checksums against the dump.
- Extract relevant metadata (e.g., tags, ratings, URLs) into a CSV and JSON file.


# Installation

## Prerequisites

- Python 3.8 or later
- Stable internet connection

## One-liner Installation Command:

For **Linux/macOS**:
```bash
git clone https://github.com/Torrafox/e621-metadata-extractor.git && cd e621-metadata-extractor && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

For **Windows**:
```bash
git clone https://github.com/Torrafox/e621-metadata-extractor.git && cd e621-metadata-extractor && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```

<details>

<summary>

## Manual Steps (Optional):

</summary>

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Torrafox/e621-metadata-extractor.git
   cd e621-metadata-extractor
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - For **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - For **Windows**:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

</details>

# Configuration
   Edit `config.json` in the project directory:
   ```json
   {
     "data_directory": "/path/to/your/e621/media/folder",
     "export_json": false
   }
   ```
   - `data_directory`: Path to the local gallery directory to process.
   - `export_json`: Whether to export the extracted metadata to a JSON file (in addition to CSV).


# Usage

## Standalone Execution

You can run the tool directly to fetch and process metadata:

```bash
python main.py
```

By default, the script:

1. Downloads the latest metadata dump from e621.
2. Processes a specified directory of files.
3. Outputs the extracted metadata to e621_metadata.csv.

## As a Library

The repository can also be used as a library in other Python projects. Import the necessary functions:

```python
from e621_metadata_extractor.fetcher import get_latest_dump_url, download_file
from e621_metadata_extractor.extractor import process_directory

# Example usage
dump_url = get_latest_dump_url()
download_file(dump_url, "posts_dump.csv.gz")
process_directory("/path/to/e621/media/folder", "posts_dump.csv.gz", "output.csv")
```


# Troubleshooting

- **Missing Dependencies**: Ensure all dependencies from `requirements.txt` are installed.
- **Gallery Not Found**: Ensure the `data_directory` in `config.json` points to the correct folder.


## Limitations

- **Site-Specific**: This tool only works with metadata from [e621.net](https://e621.net) and cannot process files from other sites.
- **Large Files**: The e621 metadata dump is approximately 1.4 GB, so ensure you have sufficient disk space and a stable internet connection.


# License

This project is licensed under the MIT License.