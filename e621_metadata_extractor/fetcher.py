import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_latest_dump_urls():
    """
    Fetches the latest CSV dump URLs for posts and tags from e621.net/db_export.
    """
    base_url = "https://e621.net/db_export/"
    print("Fetching the latest database export URLs from e621...")
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links matching the required formats
        links = soup.find_all('a', href=True)
        posts_links = [
            link['href'] for link in links
            if re.match(r"posts-\d{4}-\d{2}-\d{2}\.csv\.gz", link['href'])
        ]
        tags_links = [
            link['href'] for link in links
            if re.match(r"tags-\d{4}-\d{2}-\d{2}\.csv\.gz", link['href'])
        ]
        pools_links = [
            link['href'] for link in links
            if re.match(r"pools-\d{4}-\d{2}-\d{2}\.csv\.gz", link['href'])
        ]
        tag_aliases_links = [
            link['href'] for link in links
            if re.match(r"tag_aliases-\d{4}-\d{2}-\d{2}\.csv\.gz", link['href'])
        ]
        tag_implications_links = [
            link['href'] for link in links
            if re.match(r"tag_implications-\d{4}-\d{2}-\d{2}\.csv\.gz", link['href'])
        ]
        wiki_pages_links = [
            link['href'] for link in links
            if re.match(r"wiki_pages-\d{4}-\d{2}-\d{2}\.csv\.gz", link['href'])
        ]
        
        if not posts_links or not tags_links:
            raise Exception("No posts or tags data exports found on the page.")
        
        # Get the most recent dump links (they should already be sorted)
        latest_posts_dump = sorted(posts_links, reverse=True)[0]
        latest_tags_dump = sorted(tags_links, reverse=True)[0]
        latest_pools_dump = sorted(pools_links, reverse=True)[0]
        latest_tag_aliases_dump = sorted(tag_aliases_links, reverse=True)[0]
        latest_tag_implications_dump = sorted(tag_implications_links, reverse=True)[0]
        latest_wiki_pages_dump = sorted(wiki_pages_links, reverse=True)[0]
        
        print(f"Latest posts data export found: {latest_posts_dump}")
        print(f"Latest tags data export found: {latest_tags_dump}")
        
        return {
            "posts": base_url + latest_posts_dump,
            "tags": base_url + latest_tags_dump,
            "pools": base_url + latest_pools_dump,
            "tag_aliases": base_url + latest_tag_aliases_dump,
            "tag_implications": base_url + latest_tag_implications_dump,
            "wiki_pages": base_url + latest_wiki_pages_dump
        }
    except Exception as e:
        print(f"Error fetching dump URLs: {e}")
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