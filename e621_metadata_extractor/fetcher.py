import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_latest_dump_url():
    """
    Fetches the latest CSV dump URL from e621.net/db_export.
    """
    base_url = "https://e621.net/db_export/"
    print("Fetching the latest database dump URL from e621...")
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links matching the required format
        links = soup.find_all('a', href=True)
        dump_links = [
            link['href'] for link in links
            if re.match(r"posts-\d{4}-\d{2}-\d{2}\.csv\.gz", link['href'])
        ]
        
        if not dump_links:
            raise Exception("No database dumps found on the page.")
        
        # Get the most recent dump link (they should already be sorted)
        latest_dump = sorted(dump_links, reverse=True)[0]
        print(f"Latest database dump found: {latest_dump}")
        return base_url + latest_dump
    except Exception as e:
        print(f"Error fetching dump URL: {e}")
        return None

def download_file(url, save_path):
    """
    Downloads a file from a given URL and saves it to the specified path with a progress bar.
    """
    try:
        # Make an initial request to get the file size
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        
        # Start downloading with a progress bar
        with open(save_path, 'wb') as file, tqdm(
            desc="Downloading",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        print(f"File downloaded successfully: {save_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")